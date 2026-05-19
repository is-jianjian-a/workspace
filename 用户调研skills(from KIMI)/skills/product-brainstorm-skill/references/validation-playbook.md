# Concept Validation Playbook

Experiment templates for testing product concepts before full development.

## Experiment 1: Landing Page Test

**Purpose**: Validate demand for a new product or major feature.

**Setup**:
1. Create a landing page describing the concept with a "Join Waitlist" or "Get Early Access" CTA
2. Drive traffic via paid ads ($100-500 budget), social posts, or email blast
3. Measure: visit-to-signup conversion rate, email open rate for follow-up

**Success criteria**:
- >10% visit-to-signup rate = strong demand
- 5-10% = moderate demand, refine messaging
- <5% = weak demand, reconsider concept

**Tools**: Unbounce, Webflow, Carrd + Stripe for pre-orders

## Experiment 2: Concierge MVP

**Purpose**: Validate that users will pay for a solution before building the product.

**Setup**:
1. Offer the service manually behind the scenes
2. User interacts through simple interface (form, email, chat)
3. Human team performs the actual work
4. Charge real money

**Example**: Before building an AI resume reviewer, offer manual resume reviews via email for $29. If 20+ people pay and are satisfied, build the automated version.

**Success criteria**: 10+ paying customers with >70% satisfaction.

## Experiment 3: Prototype User Test

**Purpose**: Validate usability and desirability of a specific interaction or flow.

**Setup**:
1. Build clickable prototype in Figma (low-fi acceptable)
2. Recruit 5 target users
3. Give them 3-5 tasks to complete
4. Observe: task success rate, time-to-complete, confusion points
5. Debrief: "Would you use this?" "What would make it better?" "How much would you pay?"

**Success criteria**:
- >60% task success rate without help
- Positive "would you use this" response from 4/5 users
- Clear articulation of value from users

## Experiment 4: Fake Door Test

**Purpose**: Measure interest in a feature by adding a UI element that doesn't work yet.

**Setup**:
1. Add a button/menu item for the proposed feature in your existing product
2. When clicked, show "Coming soon — get notified" with email capture
3. Track click rate over 1-2 weeks

**Success criteria**:
- >5% of eligible users click = strong interest
- 2-5% = moderate interest, lower priority
- <2% = weak interest, deprioritize

**Caution**: Don't overuse — damages trust if "coming soon" never ships. Limit to 1-2 fake doors at a time.

## Experiment 5: A/B Test (for incremental features)

**Purpose**: Compare two approaches or validate an improvement.

**Setup**:
1. Build minimal working version of the feature (not polished)
2. Show to 50% of eligible users (treatment), 50% see control
3. Run for minimum 1 week or until statistical significance (p<0.05)
4. Track primary metric + guardrail metrics

**Success criteria**: Primary metric improves with statistical significance, guardrail metrics don't degrade.

**Minimum sample**: Use sample size calculator. Typically 1000+ users per variant for conversion metrics.

## Experiment 6: Customer Interview Validation

**Purpose**: Deeply validate problem-solution fit before any building.

**Setup**:
1. Recruit 8-12 target users
2. Show concept description + rough mockup
3. Ask structured questions:
   - "Is this solving a real problem for you?" (problem validation)
   - "How do you solve this today?" (current alternative assessment)
   - "What would make you switch?" (switching trigger)
   - "Would you pay [price]?" (willingness to pay)
   - "Who else should I talk to?" (referral = strong interest signal)

**Success criteria**:
- 7/10+ confirm it's a real problem
- 5/10+ would pay the proposed price
- 3/10+ give referrals to other potential users

## Experiment Selection Matrix

| Concept Type | Recommended Experiment | Timeline | Cost |
|-------------|----------------------|----------|------|
| New product | Landing page + waitlist | 1-2 weeks | $100-500 |
| Service offering | Concierge MVP | 2-4 weeks | $500-2000 |
| UI/UX change | Prototype user test | 1 week | $0-500 |
| Feature addition | Fake door test | 1-2 weeks | $0 (engineering time) |
| Optimization | A/B test | 1-3 weeks | Engineering time |
| Problem exploration | Customer interviews | 2 weeks | $0-1000 (incentives) |

## Validation Result Documentation

For each experiment, document:

```markdown
## Experiment: [Name]
**Concept tested**: [Brief description]
**Method**: [Landing page / Concierge / Prototype / Fake door / A/B / Interview]
**Timeline**: [Dates]
**Sample size**: [N users / N interviews]

### Results
- Primary metric: [Value] vs. target [Value]
- Key qualitative finding: [Insight from users]
- Surprising finding: [Unexpected learning]

### Decision
[GO / ITERATE / KILL] with reasoning

### Next steps
[If GO: Engineering spec timeline]
[If ITERATE: What to change and re-test]
[If KILL: What we learned for future concepts]
```
