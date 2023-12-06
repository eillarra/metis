import nh3


def sanitize(html: str, *, tags: set | None = None) -> str:
    """Escape or strip markup and attributes from a text (html).

    Args:
        html: The text to sanitize.
        tags: A set of allowed html tags. No tags allowed by default.

    Returns:
        The sanitized html.
    """
    if not tags:
        tags = set()

    return nh3.clean(html, tags)
