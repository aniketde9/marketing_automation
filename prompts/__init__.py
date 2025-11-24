"""
Centralized prompt management system.

Import all prompt modules.
"""
from .video_prompts import get_video_prompt, VIDEO_TYPES
from .short_post_prompts import get_short_post_prompt
from .carousel_prompts import get_carousel_prompt
from .thread_prompts import get_thread_prompt, get_linkedin_prompt


__all__ = [
    'get_video_prompt',
    'get_short_post_prompt', 
    'get_carousel_prompt',
    'get_thread_prompt',
    'get_linkedin_prompt',
    'VIDEO_TYPES'
]




