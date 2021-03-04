class EmailNotValid(Exception):
    pass


class UserRoleError(Exception):
    pass


class UserNotActive(Exception):
    """Each user must activate his account using `activate` endpoint"""
    pass


class InvalidTimeError(Exception):
    pass
