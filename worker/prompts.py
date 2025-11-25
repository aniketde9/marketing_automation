"""
Default prompt templates for content generation

Supports long, complex prompts with markdown formatting
"""

# Simplified templates - one carousel for both platforms
PROMPT_TEMPLATES = {
    "carousel": """Create a professional carousel post about: {topic}

Requirements:
- 6-8 slides total
- Each slide: Title + Content
- Professional yet engaging tone
- Value-driven content
- Clear progression
- Works for both LinkedIn and Instagram

Format each slide as:
Slide N: [Title]
[Content]
""",
    "thread_x": """Create a Twitter/X thread about: {topic}

Requirements:
- 5-8 tweets
- First tweet: hook (under 280 chars)
- Each tweet: one key point
- Conversational tone
- End with CTA

Format as:
1/ [Hook tweet]
2/ [Point 1]
3/ [Point 2]
...
""",
    "short_linkedin": """Create a LinkedIn post about: {topic}

Requirements:
- 100-150 words
- Professional tone
- Include 1-2 relevant hashtags
- End with engagement question
""",
    "short_x": """Create a Twitter/X post about: {topic}

Requirements:
- Maximum 280 characters
- Punchy and engaging
- Use 1-2 relevant hashtags
""",
    "short_instagram": """Create an Instagram caption about: {topic}

Requirements:
- 80-120 words
- Engaging and visual
- 5-8 relevant hashtags
- Include emoji
- Call to action
""",
    "mixed": """Create engaging social media content about: {topic}

Choose the best format and create compelling content that would work across platforms.
""",
    "short_posts": """Create a short, punchy social media post about: {topic}

Requirements:
- 50-100 words
- Platform-agnostic
- Engaging hook
- 2-3 hashtags
""",
}


def get_content_type_key(content_type: str) -> str:
    """
    Map content types to prompt template keys

    Simplified to use single carousel template
    """
    # Normalize the content type
    normalized = content_type.lower().strip()

    # Simplified mappings - all carousels use same template
    mappings = {
        "carousel": "carousel",
        "linkedin/instagram": "carousel",
        "linkedin": "carousel",
        "instagram": "carousel",
        "x threads": "thread_x",
        "x thread": "thread_x",
        "thread": "thread_x",
        "linkedin posts": "short_linkedin",
        "linkedin post": "short_linkedin",
        "x posts": "short_x",
        "x post": "short_x",
        "tweet": "short_x",
        "instagram captions": "short_instagram",
        "instagram caption": "short_instagram",
        "mixed": "mixed",
        "all formats": "mixed",
        "short posts": "short_posts",
        "short post": "short_posts",
    }

    # Check each mapping
    for key, value in mappings.items():
        if key in normalized:
            return value

    # Default to mixed for unknown types
    return "mixed"


