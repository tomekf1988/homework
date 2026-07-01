class CodeGenerationError(Exception):
    """Raised when a unique short code could not be generated."""

class ShortLinkNotFoundError(Exception):
    """Raised when a short link could not be found."""