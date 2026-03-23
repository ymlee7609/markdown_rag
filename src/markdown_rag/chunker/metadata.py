"""Extract YAML frontmatter from Markdown content.

Uses the python-frontmatter library to separate YAML metadata
from the Markdown body.
"""

from __future__ import annotations

import frontmatter


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and return (metadata, body).

    Args:
        content: Raw Markdown string, possibly with YAML frontmatter
            delimited by ``---``.

    Returns:
        A tuple of (metadata_dict, body_content).
        If no frontmatter is present, metadata_dict is an empty dict
        and body_content is the original content.
    """
    if not content:
        return {}, ""

    post = frontmatter.loads(content)
    metadata: dict = dict(post.metadata)
    body: str = post.content
    return metadata, body
