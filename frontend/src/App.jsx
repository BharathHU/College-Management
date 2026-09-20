import { lazy, Suspense, useEffect, useState } from 'react'
import {
  BarChart3,
  BookOpen,
  CalendarDays,
  ClipboardCheck,
  FileText,
  GraduationCap,
  LayoutDashboard,
  LogOut,
  Megaphone,
  Search,
  Users,
  X
} from 'lucide-react'
import './App.css'

const DashboardChart = lazy(() => import('./components/DashboardChart.jsx'))

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

async function api(path, options = {}) {
  const token = sessionStorage.getItem('college_token')

  const controller = options.signal ? null : new AbortController()
  const timeout = setTimeout(() => controller?.abort(), 15000)

  try {
    const response = await fetch(`${API_URL}${path}`, {
      ...options,
      signal: options.signal || controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...(options.headers || {})
      }
    })

    const body = await response.json().catch(() => ({}))

    if (!response.ok) {
      throw new Error(body.detail || 'Request failed')
    }

    return body.data
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('Request timed out or was cancelled')
    }

    throw error
  } finally {
    clearTimeout(timeout)
  }
}

const navItems = {
  STUDENT: [
    ['dashboard', 'Dashboard', LayoutDashboard],
    ['profile', 'Profile', GraduationCap],
    ['subjects', 'Subjects', BookOpen],
    ['attendance', 'Attendance', ClipboardCheck],
    ['marks', 'Marks & grades', BarChart3],
    ['assignments', 'Assignments', FileText],
    ['timetable', 'Timetable', CalendarDays],
    ['announcements', 'Announcements', Megaphone]
  ],

  TEACHER: [
    ['dashboard', 'Dashboard', LayoutDashboard],
    ['profile', 'Profile', GraduationCap],
    ['subjects', 'Assigned subjects', BookOpen],
    ['students', 'Students', Users],
    ['attendance', 'Attendance', ClipboardCheck],
    ['marks', 'Marks & grades', BarChart3],
    ['assignments', 'Assignments', FileText],
    ['timetable', 'Timetable', CalendarDays],
    ['announcements', 'Announcements', Megaphone]
  ]
}

function App() {
  const [user, setUser] = useState(() =>
    JSON.parse(sessionStorage.getItem('college_user') || 'null')
  )

  const [view, setView] = useState('dashboard')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function login(username, password) {
    setLoading(true)
    setError('')

    try {
      const data = await api('/auth/login', {
        method: 'POST',
        body: JSON.stringify({
          username,
          password
        })
      })

      // Store authentication separately for each browser tab
      sessionStorage.setItem('college_token', data.access_token)
      sessionStorage.setItem('college_user', JSON.stringify(data.user))

      setUser(data.user)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function logout() {
    // Remove only this tab's authentication data
    sessionStorage.removeItem('college_token')
    sessionStorage.removeItem('college_user')

    setUser(null)
  }

  if (!user) {
    return (
      <Login
        onLogin={login}
        error={error}
        loading={loading}
      />
    )
  }

  const items = navItems[user.role] || navItems.STUDENT

  return (
    <div className="app-shell">
      <Sidebar
        user={user}
        items={items}
        view={view}
        setView={setView}
        logout={logout}
      />

      <main className="main">
        <header className="topbar">
          <div>
            <p className="eyebrow">COLLEGE MANAGEMENT SYSTEM</p>

            <h1>
              {items.find(([key]) => key === view)?.[1] || 'Portal'}
            </h1>
          </div>

          <div className="user-chip">
            <span className="avatar">
              {user.username?.[0]?.toUpperCase()}
            </span>

            <span>
              <strong>{user.username}</strong>

              <small>
                {user.role === 'STUDENT'
                  ? 'Student portal'
                  : 'Faculty portal'}
              </small>
            </span>
          </div>
        </header>

        <Page
          view={view}
          role={user.role}
          setView={setView}
        />
      </main>
    </div>
  )
}

function Login({ onLogin, error, loading }) {
  const [username, setUsername] = useState('student@example.com')
  const [password, setPassword] = useState('student123')

  return (
    <div className="login-page">
      <div className="login-art">
        <div className="brand-mark">
          <GraduationCap size={24} />
          Northstar College
        </div>

        <div className="art-copy">
          <p className="eyebrow">ACADEMIC OPERATIONS</p>

          <h1>
            Everything your campus needs, in one clear view.
          </h1>

          <p>
            Track progress, coordinate teaching, and keep every academic
            moment moving forward.
          </p>
        </div>

        <div className="art-footer">
          Spring term · 2026
        </div>
      </div>

      <form
        className="login-card"
        onSubmit={(event) => {
          event.preventDefault()
          onLogin(username, password)
        }}
      >
        <div className="brand-mark dark">
          <GraduationCap size={24} />
          Northstar
        </div>

        <p className="eyebrow">WELCOME BACK</p>

        <h2>Sign in to your portal</h2>

        <p className="muted">
          Use your college account to continue.
        </p>

        <label>
          Email or username

          <input
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          />
        </label>

        <label>
          Password

          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>

        {error && (
          <div className="error-box">
            {error}
          </div>
        )}

        <button
          className="primary-button"
          disabled={loading}
        >
          {loading ? 'Signing in...' : 'Sign in'}
          <span>↗</span>
        </button>

        <p className="demo-hint">
          Demo: student@example.com / student123
          <br />
          Teacher: teacher@example.com / teacher123
        </p>
      </form>
    </div>
  )
}

function Sidebar({
  user,
  items,
  view,
  setView,
  logout
}) {
  return (
    <aside className="sidebar">
      <div className="brand-mark">
        <GraduationCap size={24} />
        <span>Namma</span> <span style={{color:'blue'}}>College</span>
      </div>

      <div className="side-context">
        <span className="context-dot" />

        {user.role === 'STUDENT'
          ? 'Student workspace'
          : 'Faculty workspace'}
      </div>

      <nav>
        {items.map(([key, label, Icon]) => (
          <button
            key={key}
            className={
              view === key
                ? 'nav-item active'
                : 'nav-item'
            }
            onClick={() => setView(key)}
          >
            <Icon size={18} />
            <span>{label}</span>
          </button>
        ))}
      </nav>

      <button
        className="logout"
        onClick={logout}
      >
        <LogOut size={17} />
        <span>Sign out</span>
      </button>
    </aside>
  )
}

function Page({ view, role, setView }) {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [refresh, setRefresh] = useState(0)

  const [filters, setFilters] = useState({
    q: '',
    status: '',
    subject_id: '',
    page: 1,
    limit: 10
  })

  const root =
    role === 'STUDENT'
      ? '/students'
      : '/teachers'

  const updateFilter = (name, value) => {
    setFilters(current => ({
      ...current,
      [name]: value,
      page: name === 'page' ? value : 1
    }))
  }

  useEffect(() => {
    const controller = new AbortController()

    let active = true

    setLoading(true)
    setError('')
    setData(null)

    const paths = {
      dashboard: `/dashboard/${role.toLowerCase()}`,
      profile: `${root}/me`,
      subjects: `${root}/subjects`,

      attendance:
        role === 'STUDENT'
          ? `${root}/attendance`
          : null,

      marks:
        role === 'STUDENT'
          ? `${root}/marks`
          : `${root}/performance`,

      assignments:
        role === 'STUDENT'
          ? '/assignments/student'
          : '/assignments/teacher',

      timetable:
        role === 'STUDENT'
          ? `${root}/timetable`
          : '/timetable',

      announcements:
        role === 'STUDENT'
          ? `${root}/announcements`
          : '/announcements',

      students: '/teachers/students'
    }

    const query = new URLSearchParams()

    if (
      filters.q &&
      [
        'subjects',
        'attendance',
        'marks',
        'assignments',
        'students'
      ].includes(view)
    ) {
      query.set('q', filters.q)
    }

    if (
      filters.status &&
      view === 'assignments'
    ) {
      query.set('status', filters.status)
    }

    if (
      filters.subject_id &&
      view === 'students'
    ) {
      query.set(
        'subject_id',
        filters.subject_id
      )
    }

    if (
      ['subjects', 'assignments', 'students']
        .includes(view)
    ) {
      query.set('page', filters.page)
      query.set('limit', filters.limit)
    }

    const suffix = query.toString()
      ? `?${query}`
      : ''

    if (!paths[view]) {
      setLoading(false)

      return () => controller.abort()
    }

    api(`${paths[view]}${suffix}`, {
      signal: controller.signal
    })
      .then(value => {
        if (active) {
          setData(value)
        }
      })
      .catch(err => {
        if (
          active &&
          err.name !== 'AbortError'
        ) {
          setError(err.message)
        }
      })
      .finally(() => {
        if (active) {
          setLoading(false)
        }
      })

    return () => {
      active = false
      controller.abort()
    }
  }, [
    view,
    role,
    root,
    filters,
    refresh
  ])

  if (loading) {
    return <Loading />
  }

  if (error) {
    return <ErrorState message={error} />
  }

  const reload = () =>
    setRefresh(value => value + 1)

  if (view === 'dashboard') {
    return (
      <Dashboard
        data={data}
        role={role}
        setView={setView}
      />
    )
  }

  if (view === 'profile') {
    return (
      <Profile
        data={data}
        role={role}
      />
    )
  }

  if (view === 'subjects') {
    return (
      <Subjects
        data={data}
        role={role}
        filters={filters}
        updateFilter={updateFilter}
      />
    )
  }

  if (view === 'attendance') {
    return role === 'STUDENT'
      ? (
        <Attendance
          data={data}
          filters={filters}
          updateFilter={updateFilter}
        />
      )
      : (
        <TeacherAttendance
          onSaved={reload}
        />
      )
  }

  if (view === 'marks') {
    return role === 'STUDENT'
      ? (
        <Marks
          data={data}
          filters={filters}
          updateFilter={updateFilter}
        />
      )
      : (
        <TeacherMarks
          onSaved={reload}
        />
      )
  }

  if (view === 'assignments') {
    return (
      <Assignments
        data={data}
        role={role}
        filters={filters}
        updateFilter={updateFilter}
        onSaved={reload}
      />
    )
  }

  if (view === 'timetable') {
    return <Timetable data={data} />
  }

  if (view === 'announcements') {
    return (
      <Announcements
        data={data}
        role={role}
        onSaved={reload}
      />
    )
  }

  return (
    <Students
      data={data}
      filters={filters}
      updateFilter={updateFilter}
    />
  )
}

function Loading() {
  return (
    <div className="state">
      <div className="spinner" />
      <p>
        Loading your academic workspace...
      </p>
    </div>
  )
}

function ErrorState({ message }) {
  return (
    <div className="state error-state">
      <X size={30} />
      <h3>Could not load this view</h3>
      <p>{message}</p>
    </div>
  )
}

function Empty({
  text = 'Nothing to show yet.'
}) {
  return (
    <div className="empty">
      <span>—</span>
      <p>{text}</p>
    </div>
  )
}

function PanelTitle({
  eyebrow,
  title
}) {
  return (
    <div className="panel-heading">
      <div>
        <p className="eyebrow">{eyebrow}</p>
        <h2>{title}</h2>
      </div>
    </div>
  )
}

function Dashboard({
  data = {},
  role,
  setView
}) {
  const stats = data.stats || {}

  return (
    <>
      <div className="welcome-row">
        <div>
          <p className="eyebrow">
            {role === 'STUDENT'
              ? 'YOUR ACADEMIC SNAPSHOT'
              : 'TODAY AT A GLANCE'}
          </p>

          <h2>
            {data.welcome || 'Welcome back'}
          </h2>

          <p className="muted">
            Here is the latest picture of your
            college workspace.
          </p>
        </div>

        <button
          className="secondary-button"
          onClick={() =>
            setView('announcements')
          }
        >
          View announcements ↗
        </button>
      </div>

      <div className="stat-grid">
        {Object.entries(stats)
          .slice(0, 4)
          .map(([key, value]) => (
            <div
              className="stat-card"
              key={key}
            >
              <span>
                {key.replaceAll('_', ' ')}
              </span>

              <strong>
                {typeof value === 'number' &&
                key.includes('attendance')
                  ? `${value}%`
                  : value}
              </strong>

              <small>
                {role === 'STUDENT'
                  ? 'Current term'
                  : 'Across your classes'}
              </small>
            </div>
          ))}
      </div>

      <div className="content-grid">
        <section className="panel chart-panel">
          <PanelTitle
            eyebrow="PERFORMANCE SIGNAL"
            title={
              role === 'STUDENT'
                ? 'Attendance by subject'
                : 'Class performance'
            }
          />

          {(
            data.attendance?.length ||
            data.performance?.length
          ) ? (
            <Suspense fallback={<Loading />}>
              <DashboardChart
                data={
                  data.attendance ||
                  data.performance
                }
                role={role}
              />
            </Suspense>
          ) : (
            <Empty text="Performance data will appear here." />
          )}
        </section>

        <section className="panel">
          <PanelTitle
            eyebrow="LATEST"
            title="Announcements"
          />

          {data.announcements?.length ? (
            data.announcements.map(item => (
              <div
                className="feed-item"
                key={`${item.title}-${item.created_at}`}
              >
                <strong>{item.title}</strong>

                <p>{item.message}</p>

                <small>
                  {new Date(
                    item.created_at
                  ).toLocaleDateString()}
                </small>
              </div>
            ))
          ) : (
            <Empty />
          )}
        </section>
      </div>
    </>
  )
}

function Profile({ data, role }) {
  return (
    <section className="panel profile-panel">
      <p className="eyebrow">
        PERSONAL RECORD
      </p>

      <div className="profile-hero">
        <span className="large-avatar">
          {data.first_name?.[0]}
          {data.last_name?.[0]}
        </span>

        <div>
          <h2>
            {data.first_name} {data.last_name}
          </h2>

          <p className="muted">
            {role === 'STUDENT'
              ? data.student_id
              : data.teacher_id}
            {' · '}
            {data.department}
          </p>
        </div>
      </div>

      <div className="detail-grid">
        {Object.entries(data)
          .filter(
            ([key]) =>
              ![
                'id',
                'first_name',
                'last_name'
              ].includes(key)
          )
          .map(([key, value]) => (
            <div key={key}>
              <span>
                {key.replaceAll('_', ' ')}
              </span>

              <strong>
                {String(
                  value ?? 'Not provided'
                )}
              </strong>
            </div>
          ))}
      </div>
    </section>
  )
}

function Subjects({
  data,
  role,
  filters,
  updateFilter
}) {
  const items = Array.isArray(data)
    ? data
    : data?.items || []

  return (
    <section className="panel">
      <PanelTitle
        eyebrow={
          role === 'STUDENT'
            ? 'YOUR CURRICULUM'
            : 'TEACHING LOAD'
        }
        title={
          role === 'STUDENT'
            ? 'Subjects and courses'
            : 'Assigned subjects'
        }
      />

      <Toolbar
        filters={filters}
        updateFilter={updateFilter}
      />

      <Table
        headers={[
          'Subject',
          'Code',
          'Semester',
          role === 'STUDENT'
            ? 'Teacher'
            : 'Students'
        ]}
        rows={items.map(item => [
          <strong key={item.id}>
            {item.name}
          </strong>,
          item.code,
          `Semester ${item.semester}`,
          role === 'STUDENT'
            ? item.teacher
            : item.student_count
        ])}
        empty="No subjects found."
      />

      <Pagination
        data={data}
        updateFilter={updateFilter}
      />
    </section>
  )
}

function Attendance({
  data,
  filters,
  updateFilter
}) {
  const items = Array.isArray(data)
    ? data
    : data?.items || []

  return (
    <section className="panel">
      <PanelTitle
        eyebrow="ATTENDANCE RECORD"
        title="Attendance by subject"
      />

      <Toolbar
        filters={filters}
        updateFilter={updateFilter}
      />

      <Table
        headers={[
          'Subject',
          'Classes',
          'Present',
          'Absent',
          'Rate'
        ]}
        rows={items.map(item => [
          <strong key={item.subject}>
            {item.subject}
          </strong>,
          item.total_classes,
          item.present,
          item.absent,
          <span
            key={`${item.subject}-rate`}
            className="status good"
          >
            {item.percentage}%
          </span>
        ])}
        empty="No attendance records yet."
      />
    </section>
  )
}

function Marks({
  data,
  filters,
  updateFilter
}) {
  const items = Array.isArray(data)
    ? data
    : data?.items || []

  return (
    <section className="panel">
      <PanelTitle
        eyebrow="ACADEMIC RESULTS"
        title="Marks and grades"
      />

      <Toolbar
        filters={filters}
        updateFilter={updateFilter}
      />

      <Table
        headers={[
          'Subject',
          'Internal',
          'Assignments',
          'Exam',
          'Total',
          'Grade'
        ]}
        rows={items.map(item => [
          <strong key={item.subject}>
            {item.subject}
          </strong>,
          item.internal_marks,
          item.assignment_marks,
          item.exam_marks,
          item.total,
          <span
            key={`${item.subject}-grade`}
            className="status accent"
          >
            {item.grade}
          </span>
        ])}
        empty="No marks published yet."
      />
    </section>
  )
}

function Assignments({
  data,
  role,
  filters,
  updateFilter,
  onSaved
}) {
  const items = Array.isArray(data)
    ? data
    : data?.items || []

  return role === 'STUDENT'
    ? (
      <StudentAssignments
        data={items}
        pageData={data}
        filters={filters}
        updateFilter={updateFilter}
        onSaved={onSaved}
      />
    )
    : (
      <TeacherAssignments
        data={items}
        pageData={data}
        filters={filters}
        updateFilter={updateFilter}
        onSaved={onSaved}
      />
    )
}

function StudentAssignments({
  data,
  pageData,
  filters,
  updateFilter,
  onSaved
}) {
  return (
    <section className="panel">
      <PanelTitle
        eyebrow="WORK TO COMPLETE"
        title="Assignments"
      />

      <Toolbar
        filters={filters}
        updateFilter={updateFilter}
        assignment
      />

      <div className="assignment-list">
        {data.length ? (
          data.map((item, index) => (
            <StudentAssignment
              key={
                item.id ??
                `${item.title}-${index}`
              }
              item={item}
              onSaved={onSaved}
            />
          ))
        ) : (
          <Empty text="No assignments match your filters." />
        )}
      </div>

      <Pagination
        data={pageData}
        updateFilter={updateFilter}
      />
    </section>
  )
}

function StudentAssignment({
  item,
  onSaved
}) {
  const [open, setOpen] = useState(false)
  const [content, setContent] = useState(
    item.submission || ''
  )
  const [message, setMessage] = useState('')
  const [saving, setSaving] = useState(false)

  async function submit(event) {
    event.preventDefault()

    setSaving(true)
    setMessage('')

    try {
      await api(
        `/assignments/${item.id}/submit`,
        {
          method: 'POST',
          body: JSON.stringify({ content })
        }
      )

      setMessage('Submission saved.')
      onSaved()
    } catch (error) {
      setMessage(error.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <article className="assignment-card">
      <div>
        <p className="eyebrow">
          {item.subject}
        </p>

        <h3>{item.title}</h3>

        <p className="assignment-description">
          {item.description}
        </p>

        <small>
          Due{' '}
          {new Date(
            item.due_date
          ).toLocaleString()}
          {' · '}
          {item.submission_date
            ? `Submitted ${new Date(
                item.submission_date
              ).toLocaleString()}`
            : 'Not submitted'}
        </small>
      </div>

      <div>
        <span
          key={`${item.id}-status`}
          className={`status ${
            item.status === 'Submitted'
              ? 'good'
              : 'warn'
          }`}
        >
          {item.status}
        </span>

        <button
          className="secondary-button"
          onClick={() => setOpen(!open)}
        >
          {open ? 'Close' : 'Submit'}
        </button>
      </div>

      {open && (
        <form
          className="submission-form"
          onSubmit={submit}
        >
          <label>
            Submission content

            <textarea
              value={content}
              onChange={event =>
                setContent(event.target.value)
              }
              required
              maxLength={2000}
            />
          </label>

          <button
            className="primary-button"
            disabled={saving}
          >
            {saving
              ? 'Submitting...'
              : 'Submit assignment'}
          </button>

          {message && (
            <p className="form-message">
              {message}
            </p>
          )}
        </form>
      )}
    </article>
  )
}

function TeacherAssignments({
  data,
  pageData,
  filters,
  updateFilter,
  onSaved
}) {
  const [selected, setSelected] =
    useState(null)

  return (
    <section className="panel">
      <PanelTitle
        eyebrow="CLASSWORK"
        title="Assignment management"
      />

      <TeacherAssignmentForm
        onSaved={onSaved}
      />

      <Toolbar
        filters={filters}
        updateFilter={updateFilter}
        assignment
      />

      <Table
        headers={[
          'Title',
          'Subject',
          'Due date',
          'Submissions',
          'Review'
        ]}
        rows={data.map(item => [
          <strong key={item.id}>
            {item.title}
          </strong>,
          item.subject,
          new Date(
            item.due_date
          ).toLocaleDateString(),
          item.submission_count,
          <button
            key={`${item.id}-review`}
            className="table-action"
            onClick={() => setSelected(item)}
          >
            Review
          </button>
        ])}
        empty="No assignments found."
      />

      <Pagination
        data={pageData}
        updateFilter={updateFilter}
      />

      {selected && (
        <SubmissionReview
          assignment={selected}
          close={() => setSelected(null)}
        />
      )}
    </section>
  )
}

function SubmissionReview({
  assignment,
  close
}) {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(null)

  useEffect(() => {
    api(
      `/assignments/${assignment.id}/submissions`
    )
      .then(setData)
      .catch(error =>
        setError(error.message)
      )
  }, [assignment.id])

  async function updateStatus(
    item,
    status
  ) {
    setSaving(item.id)
    setError('')

    try {
      await api(
        `/assignments/${assignment.id}/submissions/${item.id}`,
        {
          method: 'PATCH',
          body: JSON.stringify({ status })
        }
      )

      setData(
        data.map(row =>
          row.id === item.id
            ? { ...row, status }
            : row
        )
      )
    } catch (updateError) {
      setError(updateError.message)
    } finally {
      setSaving(null)
    }
  }

  return (
    <div className="review-panel">
      <div className="panel-heading">
        <h3>
          {assignment.title} submissions
        </h3>

        <button
          className="table-action"
          onClick={close}
        >
          Close
        </button>
      </div>

      {error && (
        <p className="form-message">
          {error}
        </p>
      )}

      {data ? (
        <Table
          headers={[
            'Student',
            'Status',
            'Submitted',
            'Timing',
            'Content'
          ]}
          rows={data.map(item => [
            <strong key={item.id}>
              {item.student_name}
            </strong>,

            <select
              key={`${item.id}-status`}
              disabled={saving === item.id}
              value={item.status}
              onChange={event =>
                updateStatus(
                  item,
                  event.target.value
                )
              }
            >
              <option value="submitted">
                Submitted
              </option>

              <option value="graded">
                Graded
              </option>

              <option value="missing">
                Missing
              </option>
            </select>,

            new Date(
              item.submitted_at
            ).toLocaleString(),

            item.is_late ? (
              <span
                key={`${item.id}-late`}
                className="status warn"
              >
                Late
              </span>
            ) : (
              <span
                key={`${item.id}-ontime`}
                className="status good"
              >
                On time
              </span>
            ),

            item.content
          ])}
          empty="No submissions yet."
        />
      ) : (
        <Loading />
      )}
    </div>
  )
}

function Timetable({ data }) {
  const items = Array.isArray(data)
    ? data
    : data?.items || []

  return (
    <section className="panel">
      <PanelTitle
        eyebrow="WEEKLY RHYTHM"
        title="Timetable"
      />

      <Table
        headers={[
          'Day',
          'Time',
          'Subject',
          'Teacher',
          'Room'
        ]}
        rows={items.map(item => [
          <strong
            key={item.id || item.day}
          >
            {item.day}
          </strong>,

          `${item.start_time} – ${item.end_time}`,

          item.subject,
          item.teacher,
          item.room
        ])}
        empty="No classes scheduled."
      />
    </section>
  )
}

function Announcements({
  data,
  role,
  onSaved
}) {
  return (
    <section className="panel">
      <PanelTitle
        eyebrow="CAMPUS BULLETIN"
        title="Announcements"
      />

      {role === 'TEACHER' && (
        <TeacherAnnouncementForm
          onSaved={onSaved}
        />
      )}

      {data?.length ? (
        <div className="announcement-list">
          {data.map(item => (
            <article
              className="announcement"
              key={item.id}
            >
              <div className="announcement-date">
                {new Date(
                  item.date ||
                  item.created_at
                ).toLocaleDateString(
                  undefined,
                  {
                    month: 'short',
                    day: 'numeric'
                  }
                )}
              </div>

              <div>
                <h3>{item.title}</h3>

                <p>
                  {item.description ||
                    item.message}
                </p>

                <small>
                  {item.subject ||
                    'College-wide'}
                  {' · '}
                  {item.teacher ||
                    'Academic office'}
                </small>
              </div>
            </article>
          ))}
        </div>
      ) : (
        <Empty text="No announcements have been posted." />
      )}
    </section>
  )
}

function Students({
  data,
  filters,
  updateFilter
}) {
  const items = data?.items || []
  const { subjects } =
    useTeacherSubjects()

  return (
    <section className="panel">
      <PanelTitle
        eyebrow="ROSTER"
        title="Students by subject"
      />

      <Toolbar
        filters={filters}
        updateFilter={updateFilter}
        roster
        subjects={subjects}
      />

      <Table
        headers={[
          'Student',
          'ID',
          'Email',
          'Attendance',
          'Performance'
        ]}
        rows={items.map(item => [
          <strong key={item.id}>
            {item.name}
          </strong>,

          item.student_id,
          item.email,

          item.attendance === null
            ? 'N/A'
            : `${item.attendance}%`,

          item.performance === null
            ? 'N/A'
            : `${item.performance}%`
        ])}
        empty="No students match your filters."
      />

      <Pagination
        data={data}
        updateFilter={updateFilter}
      />
    </section>
  )
}

function TeacherAttendance({
  onSaved
}) {
  return (
    <section className="panel">
      <PanelTitle
        eyebrow="FACULTY TOOL"
        title="Attendance management"
      />

      <TeacherAcademicForm
        endpoint="/attendance/mark"
        title="Record attendance"
        fields={['date', 'status']}
        onSaved={onSaved}
      />
    </section>
  )
}

function TeacherMarks({
  onSaved
}) {
  return (
    <section className="panel">
      <PanelTitle
        eyebrow="FACULTY TOOL"
        title="Marks management"
      />

      <TeacherAcademicForm
        endpoint="/marks/upsert"
        title="Publish marks"
        fields={[
          'internal_marks',
          'assignment_marks',
          'exam_marks'
        ]}
        onSaved={onSaved}
      />
    </section>
  )
}

function useTeacherSubjects() {
  const [subjects, setSubjects] =
    useState([])

  const [error, setError] =
    useState('')

  useEffect(() => {
    api(
      '/teachers/subjects?page=1&limit=100'
    )
      .then(data =>
        setSubjects(data.items || [])
      )
      .catch(err =>
        setError(err.message)
      )
  }, [])

  return {
    subjects,
    error
  }
}

function TeacherSubjectSelect({
  value,
  onChange,
  subjects
}) {
  return (
    <label>
      Subject

      <select
        value={value}
        onChange={event =>
          onChange(event.target.value)
        }
        required
      >
        <option value="">
          Select an assigned subject
        </option>

        {subjects.map(subject => (
          <option
            key={subject.id}
            value={subject.id}
          >
            {subject.code} · {subject.name}
          </option>
        ))}
      </select>
    </label>
  )
}

function TeacherStudentSelect({
  subjectId,
  value,
  onChange
}) {
  const [students, setStudents] =
    useState([])

  const [loading, setLoading] =
    useState(false)

  useEffect(() => {
    if (!subjectId) {
      setStudents([])
      return
    }

    setLoading(true)

    api(
      `/teachers/students?subject_id=${subjectId}&page=1&limit=100`
    )
      .then(data =>
        setStudents(data.items || [])
      )
      .catch(() =>
        setStudents([])
      )
      .finally(() =>
        setLoading(false)
      )
  }, [subjectId])

  return (
    <label>
      Student

      <select
        value={value}
        onChange={event =>
          onChange(event.target.value)
        }
        required
        disabled={!subjectId || loading}
      >
        <option value="">
          {loading
            ? 'Loading students...'
            : 'Select an enrolled student'}
        </option>

        {students.map(student => (
          <option
            key={student.id}
            value={student.id}
          >
            {student.student_id} · {student.name}
          </option>
        ))}
      </select>
    </label>
  )
}

function TeacherAcademicForm({
  endpoint,
  title,
  fields,
  onSaved
}) {
  const {
    subjects,
    error: subjectError
  } = useTeacherSubjects()

  const [values, setValues] =
    useState({})

  const [message, setMessage] =
    useState('')

  const [saving, setSaving] =
    useState(false)

  async function submit(event) {
    event.preventDefault()

    setSaving(true)
    setMessage('')

    const payload = {
      ...values,
      subject_id: Number(
        values.subject_id
      ),
      student_id: Number(
        values.student_id
      )
    }

    for (
      const field of [
        'internal_marks',
        'assignment_marks',
        'exam_marks'
      ]
    ) {
      if (field in payload) {
        payload[field] = Number(
          payload[field]
        )
      }
    }

    try {
      await api(endpoint, {
        method: 'POST',
        body: JSON.stringify(payload)
      })

      setMessage(
        'Saved successfully.'
      )

      setValues({})
      onSaved?.()
    } catch (error) {
      setMessage(error.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <form
      className="mutation-form"
      onSubmit={submit}
    >
      <h3>{title}</h3>

      {subjectError && (
        <p className="form-message">
          {subjectError}
        </p>
      )}

      <div className="mutation-grid">
        <TeacherSubjectSelect
          value={values.subject_id || ''}
          onChange={subject_id =>
            setValues({
              ...values,
              subject_id,
              student_id: ''
            })
          }
          subjects={subjects}
        />

        <TeacherStudentSelect
          subjectId={values.subject_id}
          value={values.student_id || ''}
          onChange={student_id =>
            setValues({
              ...values,
              student_id
            })
          }
        />

        {fields.map(field =>
          field === 'date' ? (
            <label key={field}>
              Date

              <input
                type="date"
                value={values[field] || ''}
                onChange={event =>
                  setValues({
                    ...values,
                    [field]:
                      event.target.value
                  })
                }
                required
              />
            </label>
          ) : field === 'status' ? (
            <label key={field}>
              Status

              <select
                value={values[field] || ''}
                onChange={event =>
                  setValues({
                    ...values,
                    [field]:
                      event.target.value
                  })
                }
                required
              >
                <option value="">
                  Select status
                </option>

                <option value="present">
                  Present
                </option>

                <option value="absent">
                  Absent
                </option>
              </select>
            </label>
          ) : (
            <label key={field}>
              {field.replaceAll(
                '_',
                ' '
              )}

              <input
                type="number"
                min="0"
                max={
                  field ===
                  'internal_marks'
                    ? 30
                    : field ===
                      'assignment_marks'
                    ? 20
                    : 50
                }
                value={
                  values[field] || ''
                }
                onChange={event =>
                  setValues({
                    ...values,
                    [field]:
                      event.target.value
                  })
                }
                required
              />
            </label>
          )
        )}
      </div>

      <button
        className="primary-button"
        disabled={
          saving || !subjects.length
        }
      >
        {saving
          ? 'Saving...'
          : 'Save changes'}
      </button>

      {message && (
        <p className="form-message">
          {message}
        </p>
      )}
    </form>
  )
}

function TeacherAssignmentForm({
  onSaved
}) {
  const {
    subjects,
    error: subjectError
  } = useTeacherSubjects()

  const [values, setValues] =
    useState({})

  const [message, setMessage] =
    useState('')

  const [saving, setSaving] =
    useState(false)

  async function submit(event) {
    event.preventDefault()

    setSaving(true)
    setMessage('')

    try {
      await api(
        '/assignments/create',
        {
          method: 'POST',
          body: JSON.stringify({
            ...values,
            subject_id: Number(
              values.subject_id
            )
          })
        }
      )

      setMessage(
        'Assignment created successfully.'
      )

      setValues({})
      onSaved?.()
    } catch (error) {
      setMessage(error.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <form
      className="mutation-form"
      onSubmit={submit}
    >
      <h3>Create assignment</h3>

      {subjectError && (
        <p className="form-message">
          {subjectError}
        </p>
      )}

      <div className="mutation-grid">
        <TeacherSubjectSelect
          value={values.subject_id || ''}
          onChange={subject_id =>
            setValues({
              ...values,
              subject_id
            })
          }
          subjects={subjects}
        />

        <label>
          Title

          <input
            value={values.title || ''}
            onChange={event =>
              setValues({
                ...values,
                title: event.target.value
              })
            }
            required
            maxLength={200}
          />
        </label>

        <label>
          Description

          <textarea
            value={
              values.description || ''
            }
            onChange={event =>
              setValues({
                ...values,
                description:
                  event.target.value
              })
            }
            required
            maxLength={1000}
          />
        </label>

        <label>
          Due date

          <input
            type="datetime-local"
            value={
              values.due_date || ''
            }
            onChange={event =>
              setValues({
                ...values,
                due_date:
                  event.target.value
              })
            }
            required
          />
        </label>
      </div>

      <button
        className="primary-button"
        disabled={
          saving || !subjects.length
        }
      >
        {saving
          ? 'Creating...'
          : 'Create assignment'}
      </button>

      {message && (
        <p className="form-message">
          {message}
        </p>
      )}
    </form>
  )
}

function TeacherAnnouncementForm({
  onSaved
}) {
  const {
    subjects,
    error: subjectError
  } = useTeacherSubjects()

  const [values, setValues] =
    useState({})

  const [message, setMessage] =
    useState('')

  const [saving, setSaving] =
    useState(false)

  async function submit(event) {
    event.preventDefault()

    setSaving(true)
    setMessage('')

    const payload = {
      title: values.title,
      message: values.message
    }

    if (values.subject_id) {
      payload.subject_id = Number(
        values.subject_id
      )
    }

    try {
      await api(
        '/announcements/create',
        {
          method: 'POST',
          body: JSON.stringify(payload)
        }
      )

      setMessage(
        'Announcement created successfully.'
      )

      setValues({})
      onSaved?.()
    } catch (error) {
      setMessage(error.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <form
      className="mutation-form"
      onSubmit={submit}
    >
      <h3>Create announcement</h3>

      {subjectError && (
        <p className="form-message">
          {subjectError}
        </p>
      )}

      <div className="mutation-grid">
        <label>
          Audience subject

          <select
            value={values.subject_id || ''}
            onChange={event =>
              setValues({
                ...values,
                subject_id:
                  event.target.value
              })
            }
          >
            <option value="">
              College-wide
            </option>

            {subjects.map(subject => (
              <option
                key={subject.id}
                value={subject.id}
              >
                {subject.code} · {subject.name}
              </option>
            ))}
          </select>
        </label>

        <label>
          Title

          <input
            value={values.title || ''}
            onChange={event =>
              setValues({
                ...values,
                title: event.target.value
              })
            }
            required
            maxLength={200}
          />
        </label>

        <label>
          Content

          <textarea
            value={values.message || ''}
            onChange={event =>
              setValues({
                ...values,
                message:
                  event.target.value
              })
            }
            required
            maxLength={2000}
          />
        </label>
      </div>

      <button
        className="primary-button"
        disabled={saving}
      >
        {saving
          ? 'Creating...'
          : 'Create announcement'}
      </button>

      {message && (
        <p className="form-message">
          {message}
        </p>
      )}
    </form>
  )
}

function Toolbar({
  filters,
  updateFilter,
  assignment = false,
  roster = false,
  subjects = []
}) {
  return (
    <div className="toolbar">
      <div className="search-box">
        <Search size={17} />

        <input
          value={filters.q}
          onChange={event =>
            updateFilter(
              'q',
              event.target.value
            )
          }
          placeholder={
            roster
              ? 'Search students'
              : 'Search by name or code'
          }
        />
      </div>

      {assignment && (
        <select
          value={filters.status}
          onChange={event =>
            updateFilter(
              'status',
              event.target.value
            )
          }
        >
          <option value="">
            All statuses
          </option>

          <option value="pending">
            Pending
          </option>

          <option value="submitted">
            Submitted
          </option>
        </select>
      )}

      {roster && (
        <select
          value={filters.subject_id}
          onChange={event =>
            updateFilter(
              'subject_id',
              event.target.value
            )
          }
        >
          <option value="">
            All assigned subjects
          </option>

          {subjects.map(subject => (
            <option
              key={subject.id}
              value={subject.id}
            >
              {subject.code} · {subject.name}
            </option>
          ))}
        </select>
      )}

      <button
        className="secondary-button"
        onClick={() => {
          updateFilter('q', '')
          updateFilter('status', '')
          updateFilter('subject_id', '')
        }}
      >
        Clear
      </button>
    </div>
  )
}

function Pagination({
  data,
  updateFilter
}) {
  if (
    !data?.total_pages ||
    data.total_pages <= 1
  ) {
    return null
  }

  return (
    <div className="pagination">
      <button
        className="secondary-button"
        disabled={data.page <= 1}
        onClick={() =>
          updateFilter(
            'page',
            data.page - 1
          )
        }
      >
        Previous
      </button>

      <span>
        Page {data.page} of{' '}
        {data.total_pages} · {data.total}{' '}
        records
      </span>

      <button
        className="secondary-button"
        disabled={
          data.page >=
          data.total_pages
        }
        onClick={() =>
          updateFilter(
            'page',
            data.page + 1
          )
        }
      >
        Next
      </button>
    </div>
  )
}

function Table({
  headers,
  rows,
  empty
}) {
  return rows.length ? (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            {headers.map(header => (
              <th key={header}>
                {header}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {rows.map((row, index) => (
            <tr key={index}>
              {row.map(
                (cell, cellIndex) => (
                  <td key={cellIndex}>
                    {cell}
                  </td>
                )
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  ) : (
    <Empty text={empty} />
  )
}

export default App