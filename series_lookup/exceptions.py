class NoAPIKeyError(Exception):
    """
    Exception raised when no TMDB API Key is set.
    """

    ...


class DatabaseError(Exception):
    """
    Exception raised when error encountered during database operations.
    """

    ...
