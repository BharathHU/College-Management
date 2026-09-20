import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

function DashboardChart({ data, role }) {
  return <ResponsiveContainer width="100%" height={260}><BarChart data={data}><CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e7e4dc" /><XAxis dataKey="subject" tick={{ fill: '#7e7a70', fontSize: 12 }} /><YAxis tick={{ fill: '#7e7a70', fontSize: 12 }} /><Tooltip /><Bar dataKey={role === 'STUDENT' ? 'percentage' : 'average_marks'} fill="#d8664a" radius={[5, 5, 0, 0]} /></BarChart></ResponsiveContainer>
}

export default DashboardChart
