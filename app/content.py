import bleach

ALLOWED_HTML_TAGS = [
    "p", "br", "h1", "h2", "h3", "strong", "b", "em", "i",
    "u", "ol", "ul", "li", "blockquote", "pre", "code", "a"
]
ALLOWED_HTML_ATTRIBUTES = {"a": ["href", "title", "target", "rel"]}
ALLOWED_HTML_PROTOCOLS = ["http", "https", "mailto"]


def sanitize_description(value):
    return bleach.clean(
        value or "",
        tags=ALLOWED_HTML_TAGS,
        attributes=ALLOWED_HTML_ATTRIBUTES,
        protocols=ALLOWED_HTML_PROTOCOLS,
        strip=True,
    )
