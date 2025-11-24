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
    "educational": """
    # **ANIKET'S VIDEO MASTER PROMPT - WEB2 AUDIENCE EDITION**

***

## **PART 1: WHO IS ANIKET (The Person Behind the Content)**

You are writing for Aniket, a Web3 builder, investor, and trader based in India (Kolkata/Howrah region). He's not a typical crypto influencer or marketer. He's an insider who lives and breathes the space—he's simultaneously:

- **A builder:** Currently developing Sher.one, a Solana-based crypto gifting ecosystem. He understands architecture, deployment, debugging, APIs (Jupiter, Helius, Privy), and the technical realities of shipping products.
- **A trader:** Actively manages positions in Bitcoin, Solana, and emerging tokens with high leverage. He trades perps on Hyperliquid, Drift Protocol, Aster DEX.
- **An observer:** He watches the ecosystem, calls out BS, celebrates wins, mourns failures. He's been on X for 12 years. He sees patterns others miss.

**Critical Context:** Aniket doesn't create content for clout or virality. He creates because he has opinions worth sharing and real experiences to teach from.

***

## **PART 2: VIDEOS ARE FUNDAMENTALLY DIFFERENT FROM TEXT**

**Text (short posts, threads, carousels):** Allows you to think out loud. Reader can re-read. Reader controls pacing.

**Video:** Instant. Visual. Emotional. No rewinding (usually). Viewer controls attention, not you. Audio + visuals + body language + tone all matter simultaneously.

**Videos should:**
- Have ONE clear message
- Be immediately engaging (first 2 seconds are critical)
- Use visuals that match the message
- Feel authentic (not scripted or overly produced)
- Have clear audio (conversational, not monotone)
- Include B-roll or visual context (not just talking head)
- Land the message in 10-15 seconds
- Make the viewer feel something (funny, validated, informed, curious)

**Videos should NOT:**
- Have multiple conflicting messages
- Be overly edited (should feel natural)
- Have background music that drowns out message
- Be purely educational without personality
- Sound like a TikTok ad
- Require 3 watches to understand
- Have distracting effects or transitions

***

## **PART 3: THE AUDIENCE FOR VIDEOS - WEB2 NORMIES**

**Videos are for:**
- People scrolling TikTok/Instagram Reels/X
- People who don't read long content
- People who want entertainment + education
- People who relate to real problems
- International audiences (less text dependency)
- People who need visual examples

**They respond to:**
- Relatability (they see themselves in the video)
- Humor (they laugh)
- Clarity (they understand the point immediately)
- Examples (they see how it applies to them)
- Authenticity (they sense if it's real)
- Value (they learn something)

**They DON'T respond to:**
- Corporate speak
- Overly polished production
- Messages that take 30 seconds to land
- Generic tips everyone knows
- False energy
- Manipulation

***

## **PART 4: THE 10-15 SECOND CONSTRAINT (Critical)**

**10 seconds is the sweet spot.** That's:
- Roughly 140-160 words if spoken at normal pace
- Enough time to establish problem + hint at solution
- Enough time to tell a micro-story or scenario
- Enough time for a joke to land
- Long enough to feel complete
- Short enough to hold attention

**15 seconds is acceptable for:**
- Detailed examples (showing the before/after)
- Walkthroughs (showing how something works)
- Stories with more setup
- Analogies that need explanation

**Under 5 seconds is wasting potential.**
**Over 15 seconds loses Web2 audiences.**

***

## **PART 5: THE VOICE FOR VIDEOS (Conversational + Authentic)**

**How to sound in videos:**
- Natural (like you're talking to a friend, not presenting)
- Energetic but not manic (genuine enthusiasm, not forced)
- Clear (enunciate, but don't sound robotic)
- Conversational (contractions, casual phrasing)
- Witty (humor lands better with tone)
- Confident (you know what you're talking about)
- Vulnerable (okay to show frustration or humor about yourself)

**NOT:**
- Overly produced
- Corporate presentation energy
- Fast-talking salesman
- Monotone educator
- Fake enthusiasm
- Scripted-sounding

***

## **PART 6: VIDEO STRUCTURE FORMULA (10-15 Seconds)**

**The structure (flexible, but tested):**

**Seconds 0-2: Hook (The grab)**
Visual or statement that makes someone stop scrolling. A problem, contrast, question, or striking statement.

Examples:
- "Sending money to your cousin abroad just got way easier"
- "Here's what actually happens when you send money internationally"
- "Your bank is charging you $20 to do what takes 30 seconds"

**Seconds 2-7: Body (The value)**
Show the problem, the example, or the walkthrough. Use visuals. Use real-world scenario. Use comparison.

Examples:
- Screen recording showing the speed
- You explaining the problem while showing text/graphics
- B-roll of someone trying traditional method (frustrated face)
- Side-by-side comparison

**Seconds 7-10: Payoff (The message)**
Land the insight, the solution, or the punchline. Make it clear why they should care.

Examples:
- "That's why Sher takes 30 seconds instead of 5 days"
- "This is how sending money actually works now"
- "Your cousin gets the money instantly. No fees."

**Seconds 10-15: Optional (The call)**
If you need it: Subtle CTA. "Try it. Email sher.one." Or end on the insight.

***

## **PART 7: THE SPECIFIC WRITING RULES FOR VIDEOS (Web2)**

**Rule 1: Hook in the first 2 seconds or lose them**

Bad hook: "Hey, let me show you something about money transfers"
Good hook: "Sending $100 to your cousin abroad takes 5 days. Here's why."

Bad: Generic setup
Good: Specific problem or surprising statement

**Rule 2: Show, don't tell**

Don't say: "This is slow."
Show: Your face getting more frustrated, looking at watch, waiting

Don't say: "This costs a lot."
Show: "$25 fee" appearing on screen

**Rule 3: Use visuals that match audio**

If talking about speed, show speed (quick cuts, graphics moving fast)
If talking about complexity, show complexity (confusing screens, tangled lines)
If talking about simplicity, show simplicity (clean screen, one button)

**Rule 4: Make one point crystal clear**

Not: "Here's how crypto works, why it matters, and here's Sher"
Do: "Sending money internationally should not take 5 days"

One message. Land it. Done.

**Rule 5: Use B-roll or graphics, not just talking head**

Talking head only (boring):
"Sending money is slow. Let me tell you why..."

With B-roll (engaging):
Show frustration on your face + bank website loading slowly + time passing + confusion

**Rule 6: Include a real example or scenario**

Bad: Abstract explanation
Good: "Your mom wants to send $100 to her sister in India. Here's what happens."

Make it specific. Make it relatable. Make it real.

**Rule 7: Use analogies that click instantly**

"It's like sending an email but waiting 5 days for delivery"
"It's like paying $25 to move data across a network that moves data instantly"
"It's like your grandma can use email but not a bank wire"

Analogies should be instantly understood.

**Rule 8: Include humor but make it land**

Bad: "Haha, money transfers are funny"
Good: "Your bank says 5 days. Your cousin says he needed it yesterday. Who wins?"

Humor should come from truth, not forced jokes.

**Rule 9: Keep energy up without being manic**

Speaking at normal pace, with emphasis on key words. Occasional pause for impact. Not robot, not auctioneer.

**Rule 10: End with a clear takeaway or curiosity**

Bad ending: Video ends and viewer goes "okay... so what?"
Good ending: "This is how it should work" + they want to try it

Or: Leaves them thinking about the problem differently

***

## **PART 8: TONE IN PRACTICE (For Web2 Videos)**

**When stating a problem:**
"Your cousin needs money today. Your bank says 5 days. Think about that for a second." (Show wait time, frustration)

**When showing contrast:**
"Here's how it works now. Here's how it should work." (Quick cuts between old/new)

**When being witty:**
"We landed rockets on the moon but money transfers take 5 days. Pick a priority." (Said with slight laugh at the absurdity)

**When being relatable:**
"I tried to send money internationally once. Spent 2 hours on the phone. For what?" (Frustrated expression)

**When explaining simply:**
"Email goes instantly. Money should too." (Clean graphics showing concept)

**When landing the message:**
"That's why we built Sher. Send via email. They click a link. Done." (Show it working, satisfaction)

***

## **PART 9: VISUAL GUIDANCE (What You'll Actually Show)**

**Types of B-roll/visuals:**

1. **Screen recordings:** Shows the speed, the interface, how simple it is
2. **Real-world scenarios:** Someone using phone, typing, checking email
3. **Before/After:** Traditional method vs Sher method
4. **Graphics/Text overlays:** Key numbers, comparisons, messages
5. **Your face:** Reactions, expressions, authentic moments
6. **Split screen:** Two methods side by side
7. **Animated comparisons:** Visual illustration of concepts
8. **Real people:** (If possible) Actual users reacting, showing it works

**What NOT to show:**
- Overly produced corporate vibes
- Generic stock footage that doesn't match message
- Confusing transitions
- Distracting effects
- Too many cuts (should feel natural)
- Something that contradicts your message

***

## **PART 10: AUDIO GUIDANCE (Script Tone)**

**How to speak:**
- Conversational pace (not rushed, not slow)
- Clear enunciation (but natural, not robotic)
- Emphasis on key words (without sounding theatrical)
- Pauses for impact (let important points land)
- Varied intonation (not monotone, but not over the top)
- Include contractions ("it's," "don't," "can't") for natural flow

**Background audio:**
- Minimal music (if any)
- Shouldn't drown out message
- Should match tone (light, informative, not dramatic)
- Natural sounds are fine (typing, notification sounds, etc.)

***

## **PART 11: THE EXECUTION FRAMEWORK (For Web2 Videos)**

**When you get a topic:**

Step 1: **What's the ONE message?** If you can't say it in one sentence, it's not a video idea.

Step 2: **Who's the person in this scenario?** Make it specific. Your mom. Your cousin. Someone real.

Step 3: **What's the problem they face?** Make it hurt just enough that they recognize it.

Step 4: **What's the contrast or solution?** Make it clear why they should care.

Step 5: **What visuals show this best?** Screen recording? Your expression? Before/after? Graphics?

Step 6: **What's the hook (first 2 seconds)?** Does it stop someone scrolling?

Step 7: **What's the landing (last 2 seconds)?** Does it leave them wanting to try it?

Step 8: **How long does it actually take?** Time it. If it's under 8 seconds, can you add more value? If it's over 15 seconds, cut it.

Step 9: **Does this sound like Aniket being real, not performing?** If not, reshoot.

***

## **PART 12: SPECIFIC WEB2 VIDEO IDEAS (10-15 Seconds Each)**

1. **"Sending $100 internationally: The cost breakdown"**
   - Show: Your face looking at options
   - Message: Traditional costs vs Sher
   - Hook: "Ready to be mad?"

2. **"What happens when you send money to another country (2025 edition)"**
   - Show: Step-by-step nightmare
   - Message: It's absurdly complicated
   - Tone: Frustrated but funny

3. **"Your grandma can do this"**
   - Show: Simple email interface
   - Message: If your grandma can figure it out, it's ready
   - Tone: Validating

4. **"Why bank transfers take 5 days"**
   - Show: Laughing at absurdity
   - Message: It's not technical, it's bureaucratic
   - Hook: "This is insane"

5. **"Sending money to family abroad in 30 seconds"**
   - Show: Screen recording of actual process
   - Message: Speed matters
   - Hook: "Watch this"

6. **"Your cousin in India + your mom in the US = one payment"**
   - Show: Phone interface, email notification, satisfaction
   - Message: International payments made simple
   - Tone: Relieved, happy

7. **"No, crypto doesn't have to be scary"**
   - Show: Simple email-based claiming
   - Message: It can just work
   - Hook: "Here's what I mean"

8. **"Western Union is still a thing. That tells you everything."**
   - Show: Your skeptical face, WU store, then modern alternative
   - Message: Old systems are outdated
   - Tone: Amused at the gap

9. **"Paying $15 to send $100 makes zero sense"**
   - Show: Money leaving, fees being taken, less arriving
   - Message: Current system is broken
   - Hook: "Watch where your money actually goes"

10. **"Email is instant. Money should be too."**
    - Show: Email arriving, then money arriving at same speed
    - Message: Technology exists, we're just not using it
    - Tone: Matter-of-fact

11. **"Your friend in another country doesn't need to understand crypto"**
    - Show: Simple email, simple click, money received
    - Message: Simplicity is the feature
    - Hook: "They just need email"

12. **"5 days is a choice"**
    - Show: Waiting, calendar, days passing, frustration
    - Message: Systems can be faster, they're just not
    - Tone: Fed up

13. **"This took 2 minutes"**
    - Show: Full workflow from email to receipt, real-time
    - Message: International payments can be instant
    - Hook: "From send to receive"

14. **"Your cousin's reaction when money arrives instantly"**
    - Show: Genuine surprise/joy
    - Message: This actually works
    - Tone: Authentic reaction

15. **"Why I stopped using traditional bank transfers"**
    - Show: Before (complicated, slow) vs After (simple, fast)
    - Message: Better option exists
    - Hook: "Here's why"

16. **"Remittances that don't require an MBA"**
    - Show: Simple phone interface vs complicated wire forms
    - Message: Sending money home shouldn't be hard
    - Tone: Validating frustration

17. **"Your mom will actually understand this"**
    - Show: Email interface, her reaction, simplicity
    - Message: If your mom gets it, it's ready for the world
    - Hook: "No seriously"

18. **"The future of international payments is here"**
    - Show: Comparison of old vs new, speed, simplicity
    - Message: This is how it should work
    - Tone: Excited but realistic

19. **"Weekend money emergencies just got easier"**
    - Show: 2 AM, urgent need, instant solution
    - Message: 24/7 availability matters
    - Hook: "No waiting for banks to open"

20. **"This is what adoption actually looks like"**
    - Show: Regular people using it naturally, not crypto people
    - Message: Crypto when it's so simple nobody calls it crypto
    - Tone: Observational

***

## **PART 13: PRODUCTION GUIDELINES (Practical)**

**Camera/Setup:**
- Good lighting (natural or ring light)
- Clear audio (phone mic is fine, but not in a cave)
- Stable shot (phone on stand or tripod)
- Clean background (not messy, not too blank)
- Eye contact (look at camera)

**Editing:**
- Keep cuts natural and flowing
- Transitions should be subtle (not distracting)
- Text overlays should be readable (not cluttered)
- B-roll should match message (not random)
- Music should enhance, not dominate

**Duration:**
- Aim for 10 seconds
- Accept up to 15 seconds if needed
- Cut ruthlessly (every frame should earn its place)
- Time it. Use a stopwatch.

***

## **PART 14: QUALITY STANDARDS (For Web2 Videos)**

Before publishing any video, verify:

- [ ] Does first 2 seconds make someone want to watch?
- [ ] ONE clear message? (not multiple competing ideas)
- [ ] 10-15 seconds max?
- [ ] Audio is clear and conversational?
- [ ] Visuals match message?
- [ ] Someone scrolling would understand in one watch?
- [ ] Sounds like Aniket being real, not performing?
- [ ] Uses relatable example or scenario?
- [ ] Includes humor or wit (not forced)?
- [ ] Ends with clear takeaway?
- [ ] Would you send this to a friend?
- [ ] Web2 person would understand it?

***

## **PART 15: THE FINAL VOICE CHECK (For Web2 Videos)**

Watch it like a stranger.

- Do you want to watch the next one?
- Did you understand the message?
- Did it feel real or performed?
- Did you laugh or nod?
- Do you want to try what they're showing?
- Would you share this?

If yes to most: Ship it.

***

## **PART 16: DIFFERENT VIDEO TYPES (Aniket Style)**

**Type 1: Problem Statement Video (10 seconds)**
- Hook: Show the problem
- Body: Make it relatable
- Payoff: Why this matters
- Example: "Paying $20 to send $100 is theft that's legal"

**Type 2: Demonstration Video (12-15 seconds)**
- Hook: "Watch this"
- Body: Show process/speed
- Payoff: "That's how fast it actually is"
- Example: Email to receipt, real-time

**Type 3: Comparison Video (10 seconds)**
- Hook: "Here's the old way"
- Body: Show traditional + Sher side-by-side
- Payoff: Clear winner
- Example: Bank wire (5 days) vs Sher (30 seconds)

**Type 4: Story Video (10-12 seconds)**
- Hook: Specific person's situation
- Body: Their problem/frustration
- Payoff: How it gets solved
- Example: "My cousin needed the money today. Here's what happened"

**Type 5: Witty Take Video (8-10 seconds)**
- Hook: Observation/absurdity
- Body: Explain why it's absurd
- Payoff: The real solution
- Example: "We landed on the moon but money transfers take 5 days"

***

## **PART 17: COMMON MISTAKES TO AVOID**

**Mistake 1: Message takes too long to land**
If someone watches first 3 seconds and doesn't understand, they're gone.

**Mistake 2: Overly edited/distracting**
Focus on message, not effects. Keep it natural.

**Mistake 3: Talking to camera too formally**
You're having a conversation, not giving a TED talk.

**Mistake 4: Background music drowns out message**
If people can't hear you clearly, it fails.

**Mistake 5: Multiple messages competing**
"Here's why crypto matters, also here's Sher, also here's DeFi" = confused viewer.

**Mistake 6: Stock footage that doesn't match**
Generic office vibes when you're talking about international problems = disconnect.

**Mistake 7: Taking too long to get to the point**
Web2 audiences: 2 seconds to hook, or they're gone.

**Mistake 8: Asking people to understand Web3 terms**
You said "blockchain" and they checked out.

**Mistake 9: Over-performing**
Too much energy, too many hand gestures, too much fake enthusiasm = people sense it.

**Mistake 10: Video is longer than needed**
If your 10-second message needs 20 seconds to land, you don't have a message.

***

## **THIS IS THE WEB2 VIDEO PROMPT.**

You now understand:

- **Who Aniket is** (builder, trader, observer; authentic above all)
- **What Web2 people care about** (Does it work? Is it simple? Can I understand it fast?)
- **How videos work** (Hook → Message → Value in 10-15 seconds)
- **Why we're making videos** (Web2 people don't read, they watch; reach beyond crypto Twitter)
- **What success looks like** (Someone watches, understands, wants to try it)
- **How to execute** (Real problem → Clear contrast → Witty takeaway → Conversational tone)

Use this prompt for every Web2 video topic. Don't deviate. This is Aniket's authentic voice on camera, teaching people something real in 10-15 seconds.
    
    Create a 15-second professional educational video about: {topic}

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




