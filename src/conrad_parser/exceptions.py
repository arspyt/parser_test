class ParserError(Exception):
    """An error after which there is no point in continuing the run."""


class AuthError(ParserError):
    """--auth mode was requested, but logging in failed."""
