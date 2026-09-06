def slugify(text):
    """Convert text into a URL-friendly slug."""
    text = text.lower().strip()
    text = text.replace(" ", "-")
    return text
