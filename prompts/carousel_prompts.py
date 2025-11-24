"""
📊 CAROUSEL PROMPTS (LinkedIn & Instagram Multi-Slide Content)
Customize your carousel generation prompts here.
"""

# ============================================================
# LINKEDIN CAROUSEL PROMPT
# ============================================================

LINKEDIN_CAROUSEL_PROMPT = """You are a content strategist creating LinkedIn carousel posts.

Generate 1 carousel outline about: {topic}

Requirements:
- 6-8 slides total
- Educational and value-driven
- Each slide: Title (5-7 words) + Talking Point (1-2 sentences)
- Professional tone but engaging
- Data-backed when possible
- Clear progression/story arc

Slide Structure:
- Slide 1: HOOK (question, surprising stat, or bold claim)
- Slides 2-6: EDUCATION (insights, frameworks, examples)
- Slide 7: CTA (follow, save, share, comment)
- Slide 8: ABOUT (optional: who you are/what you do)

Format:

Slide 1: [Title] | [Hook/Stat]
Slide 2: [Title] | [Insight + Example]
Slide 3: [Title] | [Framework or How-to]
...

Example for "How to raise your first $1M":

Slide 1: Most VCs Say No in 3 Minutes | Learn what separates funded founders from everyone else.
Slide 2: The Traction Trap | VCs don't invest in ideas. They invest in momentum. Show 20% MoM growth.
Slide 3: The Pitch Formula | Problem (30s) + Solution (30s) + Traction (60s) + Ask (30s) = Meeting.
Slide 4: Network Before You Need It | 80% of deals come from warm intros. Build relationships now.
Slide 5: The Deck That Converts | 10 slides max. Tell a story, not a feature list.
Slide 6: Timing Is Everything | Raise when you DON'T need it. Desperation kills deals.
Slide 7: Save This for Your Raise | Follow me for more fundraising insights. Drop questions below.

Generate for topic: {topic}

Return ONLY the slide outlines in the format above. No explanation."""

# ============================================================
# INSTAGRAM CAROUSEL PROMPT
# ============================================================

INSTAGRAM_CAROUSEL_PROMPT = """You are a social media expert creating Instagram carousel posts.

Generate 1 carousel outline about: {topic}

Requirements:
- 6-10 slides total
- Visual-first, highly shareable
- Each slide: Title (3-5 words) + Key Point (1 sentence)
- Casual, relatable tone
- Heavy emoji use
- Storytelling angle

Slide Structure:
- Slide 1: HOOK (bold statement, question, or pattern interrupt)
- Slides 2-8: VALUE (tips, insights, steps, or story beats)
- Slide 9: CTA (save, share, tag someone)
- Slide 10: OUTRO (call-to-action + branding)

Format:

Slide 1: [Title] 🔥 | [Hook line]
Slide 2: [Title] ✨ | [Point]
Slide 3: [Title] 💡 | [Point]
...

Example for "5 Habits of Millionaire Founders":

Slide 1: Stop Being Busy 🛑 | Millionaires focus on impact, not hours worked.
Slide 2: Wake Up at 5 AM? 😴 | Myth. Sleep 8 hours. Energy > Early mornings.
Slide 3: Inbox Zero Daily 📧 | Check email 2x/day max. Protect deep work time.
Slide 4: Say No to 90% 🚫 | Your time is your currency. Guard it ruthlessly.
Slide 5: Hire Fast, Fire Faster 👥 | Bad hires cost 6-12 months. Cut losses early.
Slide 6: Obsess Over One Metric 📊 | Pick your North Star. Ignore vanity metrics.
Slide 7: Save This 💾 | Swipe for the full list. Which habit are you adding?
Slide 8: Follow for More 🚀 | Daily tips on building wealth & scaling startups.

Generate for topic: {topic}

Return ONLY the slide outlines. No explanation."""

# ============================================================
# PROMPT GETTER FUNCTION
# ============================================================

def get_carousel_prompt(topic, platform="linkedin"):
    """
    Get customized carousel prompt.
    
    Args:
        topic: The topic to create carousel about
        platform: 'linkedin' or 'instagram'
    
    Returns:
        Formatted prompt string
    
    Usage:
        prompt = get_carousel_prompt("Sales frameworks", "linkedin")
    """
    prompts = {
        "linkedin": LINKEDIN_CAROUSEL_PROMPT,
        "instagram": INSTAGRAM_CAROUSEL_PROMPT
    }
    
    if platform not in prompts:
        print(f"⚠️  Unknown platform: {platform}. Using 'linkedin'.")
        platform = "linkedin"
    
    prompt_template = prompts[platform]
    return prompt_template.format(topic=topic)

# ============================================================
# CUSTOMIZATION GUIDE
# ============================================================

"""
HOW TO CUSTOMIZE:

1. Edit the slide structure requirements
2. Adjust tone (professional vs casual)
3. Change slide count (6-10 is optimal)
4. Modify CTA style

DESIGN TIPS:
- LinkedIn: Use professional colors, charts, clean layouts
- Instagram: Bold colors, minimal text, heavy visual hierarchy
- Both: Each slide should work standalone (for swipe-through)
"""




