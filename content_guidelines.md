# Content Guidelines — Shane Vanderleelie Mortgages (Instagram: @shanevandermortgages)

## Business info
- NMLS #2682924
- Licensed in: Florida
- Equal Housing Lender (always include the Equal Housing Opportunity statement/logo on promotional graphics)
- Veteran-owned and operated — every post image includes a "Veteran Owned and Operated" badge (added automatically by composite_post.py). Captions can occasionally reference this (e.g., "proud to be a veteran-owned business"), especially alongside VA loan content, but must not imply VA or government endorsement.

## Audience
Mixed: first-time homebuyers, refinancers/current homeowners, and VA loan borrowers/veterans. General homebuying education appeals to all of these.

## Content mix (rotate across posts)
1. **Educational** (~50%) — explainer content: loan types (Conventional, FHA, VA, USDA), credit score tips, down payment programs, refinancing basics, glossary terms ("What is APR vs interest rate?"), VA loan benefits/eligibility.
2. **Market updates** (~25%) — current mortgage rate trends, Florida housing market commentary. Always frame rates as "as of [date]" and "subject to change" — never imply a guaranteed/locked rate in a social post.
3. **Promotional / CTA** (~25%) — "Get pre-approved", "Reach out for a free consultation", VA loan eligibility checks. Must include compliance disclaimer (see below).

### VA angle (woven in, not dominant)
About 1 in every 3-4 posts (across any of the categories above) should lean into VA loan content, since this is a veteran-owned business — e.g., VA myth-busters ("you don't need 20% down"), VA benefit breakdowns (no PMI, funding fee waivers for disability ratings), VA eligibility basics. The rest of the rotation should stay general-audience (FHA/Conventional/USDA, credit, refinancing, market updates) so non-veteran homebuyers and refinancers stay equally well served. Avoid specific payment/dollar examples (e.g., "$2,040/month") and specific close-time promises ("21-30 days") in auto-generated posts — those need Shane/compliance review before use.

## Required disclosures
- Every post: include `NMLS #2682924` somewhere in the caption (can be small/at the end).
- Promotional posts: add "This is not a commitment to lend. Terms and programs subject to change without notice. Equal Housing Opportunity." (shortened forms acceptable, e.g. "Equal Housing Lender. NMLS #2682924. Not a commitment to lend.")
- Avoid: guaranteed approval claims, specific rate promises, "no cost" claims without qualification, discriminatory language of any kind (Fair Housing Act).
- VA loan content: don't imply affiliation with or endorsement by the VA or any government agency.

## Brand voice
- Friendly, approachable, educational — not salesy or high-pressure.
- Plain language, avoid excessive jargon (explain terms when used).
- Local Florida flavor where relevant (e.g., referencing Florida-specific programs like the Florida Hometown Heroes program, Florida Housing first-time buyer programs).

## Hashtag suggestions
#FloridaMortgage #FirstTimeHomeBuyer #VALoan #HomeLoanTips #MortgageBroker #FloridaRealEstate #RefinanceYourHome #HomeBuyingTips #VeteranOwned

## Caption format
- Hook line (question or bold statement)
- 2-4 short paragraphs or bullet points of value
- CTA (varies by content type — "Save this for later", "DM us your questions", "🔗 Link in bio to get pre-approved", "📞 Tap Call to talk through your options")
- Hashtags (5-8)
- Disclosure line at the very end

## Contact CTAs
The Instagram profile has a clickable website link (www.shanevanderleeliefairwaymc.com) and a "Call" button ((813)-245-2068). Reference these in CTAs instead of writing out raw URLs/numbers in the caption (Instagram captions don't make links or phone numbers clickable):
- "🔗 Link in bio" — for pre-approval, consultations, learning more
- "📞 Tap the Call button on our profile" — for direct questions, eligibility checks

## Posting cadence
1-2 times per day (morning and evening), rotating through the content mix.

## Reels (video posts)
- Vertical 9:16 aspect ratio, 15-30 seconds.
- Hook in the first 3 seconds (on-screen text + caption hook line).
- Use on-screen text overlays to reinforce key points (many viewers watch muted).
- Same content mix and disclosure rules as feed posts apply.
- `post_to_instagram.py` supports `--video-url` to publish as a Reel (uses `media_type=REELS`).
- Note: composite_post.py currently only brands static images. Reels need to be reviewed for branding/disclosures manually until a video-branding step is added.
