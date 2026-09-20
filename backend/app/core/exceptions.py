class BusinessLogicError(Exception):
    pass


class NotFoundError(BusinessLogicError):
    pass


class PermissionDeniedError(BusinessLogicError):
    pass


class DuplicateEntryError(BusinessLogicError):
    pass
