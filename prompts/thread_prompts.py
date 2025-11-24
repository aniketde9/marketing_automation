"""
🧵 THREAD PROMPTS (X Threads & LinkedIn Long-Form)
Customize your long-form content prompts here.
"""

# ============================================================
# X THREAD PROMPT (Aniket Style)
# ============================================================

X_THREAD_PROMPT = """You are a master storyteller writing viral X threads in Aniket's style.

Aniket Thread Style:
- 8-12 tweets total
- Educational + Opinionated
- Strong narrative arc
- Each tweet stands alone but connects to story
- Spicy takes backed by logic
- Starts controversial, ends actionable
- Strategic emoji use (1-2 per tweet)

Generate 1 X thread about: {topic}

Thread Structure:

Tweet 1: HOOK (controversial take, surprising stat, or bold claim)
Tweet 2: CONTEXT (why this matters)
Tweet 3-4: PROBLEM (what most people get wrong)
Tweet 5-7: SOLUTION (framework, insights, examples)
Tweet 8: TAKEAWAY (actionable advice)
Tweet 9: CTA (follow for more, retweet, reply)

Each tweet: 280 chars max, numbered.

Example thread on "Why most startups fail":

1. 90% of startups fail not because of bad products.

They fail because founders are afraid to sell.

Here's what 3 years of building in public taught me about sales:

2. Most technical founders see sales as "sleazy."

It's not.

Sales is helping people solve problems they already have.

If your product doesn't solve a real problem, no amount of sales will save you.

3. The mistake: Building in isolation for 12 months.

The fix: Sell before you build.

Talk to 50 potential customers. If 30 say "I'd pay for this tomorrow," you have a business.

If not, pivot.

4. Cold outreach isn't dead. Your outreach is just bad.

Stop: "Hey, check out my product!"

Start: "I noticed you're struggling with X. Here's how I solved it."

Personalization beats automation 10/10 times.

5. The Framework: 100 Outreach → 10 Calls → 3 Pilots → 1 Paying Customer

Most founders quit at 20 outreach.

The ones who win just keep going.

6. Your network is your net worth.

Every founder making $1M+ got there through relationships, not SEO.

Build in public. Share your journey. Help others.

The opportunities will come.

7. Action items:

- Send 10 personalized cold emails today
- Book 2 customer discovery calls this week
- Share your progress publicly

Sales is a skill. Learn it or hire for it. No third option.

8. If you found this valuable:

- Follow me for more startup insights
- Retweet the first tweet
- Drop your biggest sales challenge below

Let's build together. 🚀

Generate thread for topic: {topic}

Return ONLY numbered tweets (1-8 or 1-10). No explanation."""

# ============================================================
# LINKEDIN LONG-FORM POST PROMPT
# ============================================================

LINKEDIN_LONGFORM_PROMPT = """You are a thought leader writing long-form LinkedIn posts.

Generate 1 LinkedIn article-style post about: {topic}

Requirements:
- 4-6 paragraphs
- Professional but conversational
- Storytelling approach
- Personal experience or case study
- Data or examples to support claims
- Clear structure: Hook → Story → Insight → Takeaway → CTA
- 300-500 words

Structure:

Para 1: HOOK (personal story, question, or surprising observation)
Para 2-3: STORY (detailed example, case study, or experience)
Para 4: INSIGHT (what this taught you, framework, or lesson)
Para 5: TAKEAWAY (actionable advice for reader)
Para 6: CTA (ask for engagement: comments, shares, DMs)

Tone:
- Vulnerable but authoritative
- Specific > Generic
- Show, don't tell
- End with open-ended question

Example opening for "Why I turned down $2M in funding":

"I turned down $2M in Series A funding last month.

My co-founder thought I was insane. My investors were confused. My team was worried.

But here's what 5 years of bootstrapping taught me about growth vs. control:

[Story continues with specific details, data, lessons, and ends with engagement question]"

Generate post for topic: {topic}

Return ONLY the post text. No title, no explanation."""

# ============================================================
# PROMPT GETTER FUNCTIONS
# ============================================================

def get_thread_prompt(topic):
    """
    Get customized X thread prompt.
    
    Args:
        topic: The topic to create thread about
    
    Returns:
        Formatted prompt string
    
    Usage:
        prompt = get_thread_prompt("Fundraising mistakes")
    """
    return X_THREAD_PROMPT.format(topic=topic)


def get_linkedin_prompt(topic):
    """
    Get customized LinkedIn long-form prompt.
    
    Args:
        topic: The topic to write about
    
    Returns:
        Formatted prompt string
    
    Usage:
        prompt = get_linkedin_prompt("Hiring your first engineer")
    """
    return LINKEDIN_LONGFORM_PROMPT.format(topic=topic)

# ============================================================
# CUSTOMIZATION GUIDE
# ============================================================

"""
HOW TO CUSTOMIZE:

1. Edit thread structure (tweet count, flow)
2. Adjust Aniket-style traits to match your voice
3. Change examples to your niche
4. Modify LinkedIn post length and structure

TIPS FOR VIRAL THREADS:
- Hook is EVERYTHING. Spend 50% of effort on tweet 1.
- Use line breaks for readability (mobile-first).
- End with clear CTA (follow, retweet, reply).
- Thread length: 8-12 tweets is sweet spot.

TIPS FOR LINKEDIN LONG-FORM:
- Personal stories > generic advice.
- Be specific (numbers, names, details).
- Vulnerability builds trust.
- Always end with a question to drive comments.
"""




