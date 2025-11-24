"""
🎬 VIDEO PROMPTS FOR SORA
Customize your video generation prompts here.
"""

# ============================================================
# VIDEO TYPES & DISTRIBUTION
# ============================================================

VIDEO_TYPES = {
    "educational": 10,    # Educational/explainer videos
    "viral": 12,          # Viral short-form content
    "promotional": 8      # Product/service promos
}
# Total: 30 videos (matches Sora daily limit)

# ============================================================
# VIDEO PROMPT TEMPLATES
# ============================================================

VIDEO_PROMPTS = {
    "educational": """Create a 15-second professional educational video about: {topic}

Visual Style:
- Clean, modern aesthetic
- High-quality graphics and animations
- Professional color palette
- Text overlays with key insights
- Smooth transitions

Audio:
- Upbeat but professional background music
- No voiceover needed

Technical Specs:
- Duration: 15 seconds
- Resolution: 720p
- Aspect ratio: 16:9 (YouTube/LinkedIn optimized)

Content Flow:
- 0-3s: Hook with surprising stat or question
- 3-10s: Core educational content (2-3 key points)
- 10-15s: Call-to-action ("Follow for more", "Save this")

Make it informative, visually engaging, and shareable.""",

    "viral": """Create a 15-second viral-style short video about: {topic}

Visual Style:
- Fast-paced, energetic cuts
- Trendy effects and transitions
- Bold text overlays
- Eye-catching colors
- Scroll-stopping first frame

Audio:
- Trending audio (if available)
- Upbeat, high-energy music

Technical Specs:
- Duration: 15 seconds
- Resolution: 720p
- Aspect ratio: 9:16 (TikTok/Reels/Shorts optimized)

Content Flow:
- 0-2s: STRONG HOOK (surprising, controversial, or intriguing)
- 2-12s: Rapid-fire content delivery (3-4 quick points)
- 12-15s: Viral CTA ("Double tap if you agree", "Tag someone")

Make it addictive, shareable, and algorithm-friendly.""",

    "promotional": """Create a 15-second promotional video about: {topic}

Visual Style:
- Professional brand aesthetic
- Clean, minimal design
- Product/service showcase
- Subtle branding elements
- Trust-building visuals

Audio:
- Calm, professional background music
- Corporate-friendly tone

Technical Specs:
- Duration: 15 seconds
- Resolution: 720p
- Aspect ratio: 1:1 (LinkedIn/Facebook optimized)

Content Flow:
- 0-3s: Problem/pain point introduction
- 3-10s: Solution showcase (your product/service)
- 10-15s: Soft CTA ("Learn more", "Get started", "Book a demo")

Make it value-driven, professional, and conversion-focused."""
}

# ============================================================
# CUSTOM VIDEO STYLES (Add your own)
# ============================================================

# Example: Add a new video type
# VIDEO_PROMPTS["testimonial"] = """Your custom prompt here..."""
# Then update VIDEO_TYPES above to include it

# ============================================================
# PROMPT GETTER FUNCTION
# ============================================================

def get_video_prompt(topic, video_type="educational"):
    """
    Get customized Sora video prompt.
    
    Args:
        topic: The topic to create video about
        video_type: 'educational', 'viral', or 'promotional'
    
    Returns:
        Formatted prompt string
    
    Usage:
        prompt = get_video_prompt("AI in healthcare", "educational")
    """
    if video_type not in VIDEO_PROMPTS:
        print(f"⚠️  Unknown video type: {video_type}. Using 'educational'.")
        video_type = "educational"
    
    prompt_template = VIDEO_PROMPTS[video_type]
    return prompt_template.format(topic=topic)

# ============================================================
# CUSTOMIZATION GUIDE
# ============================================================

"""
HOW TO CUSTOMIZE:

1. Edit the prompt templates above
2. Adjust visual style, audio, content flow as needed
3. Add your own video types by creating new entries in VIDEO_PROMPTS
4. Update VIDEO_TYPES distribution to match your needs

TIPS:
- Be specific about visual style (Sora responds well to detailed descriptions)
- Mention text overlays if you want them
- Specify aspect ratios for platform optimization
- Include pacing/timing for better results
"""




