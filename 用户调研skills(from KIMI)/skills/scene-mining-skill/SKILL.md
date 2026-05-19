---
name: scene-mining-skill
description: >
  High-value scenario discovery and product opportunity mining. Use when the task involves:
  (1) Identifying high-value user scenarios, use cases, or jobs-to-be-done (JTBD),
  (2) Mapping customer journey touchpoints to find friction and opportunity,
  (3) Discovering "Aha moments" or product activation opportunities for growth,
  (4) Analyzing user behavior data to find underserved or high-pain scenarios,
  (5) Prioritizing product opportunities using value-versus-effort frameworks,
  (6) Conducting JTBD interviews or "switch" analysis to understand user motivation,
  (7) Building product opportunity scorecards or scenario prioritization matrices, or
  (8) Any task requiring transformation of user insights into prioritized product scenarios
  with business value assessment. Combines qualitative research methods with quantitative
  prioritization frameworks.
---

# Scene Mining Skill

Discover and prioritize high-value user scenarios that drive product strategy and growth.

## Core Workflow

1. **Gather inputs**: Collect user research, behavioral data, market signals, competitive intel
2. **Map jobs**: Identify Jobs-to-be-Done using interviews or feedback analysis
3. **Map journeys**: Build user journey maps to find pain points and opportunity gaps
4. **Score scenarios**: Evaluate each scenario on frequency × pain × willingness-to-pay × feasibility
5. **Prioritize**: Build ranked opportunity backlog with clear value hypothesis
6. **Validate**: Test top scenarios with users before committing engineering resources

## Scenario Definition Template

Each high-value scenario must include these 5 elements:

```
**User**: [Who — specific persona/segment]
**Context**: [When/Where — specific situation]
**Job**: [What they need to accomplish]
**Current pain**: [What's frustrating about existing solutions]
**Success metric**: [How we'd measure if we solved it]
```

Example: "Small business owner (User) during monthly tax filing (Context) needs to categorize business expenses from mixed personal/business transactions (Job). Current pain: manually reviewing 200+ transactions takes 3 hours. Success: auto-categorization accuracy >90% saving 2+ hours/month."

## JTBD Discovery Method

### Jobs-to-be-Done Framework
Users "hire" products to get jobs done. Three dimensions of every job:

- **Functional**: Practical task completion ("file my taxes correctly")
- **Emotional — Personal**: How user wants to feel ("feel in control of finances")
- **Social**: How user wants to be perceived ("appear organized and professional")

### Switch Interview Protocol
Interview users who recently switched to/from your product:

1. **Timeline**: "Walk me through the day you decided to look for a solution."
2. **Consideration**: "What alternatives did you evaluate? Why did you reject each?"
3. **Decision**: "What was the final straw that made you choose [product]?"
4. **First use**: "What happened when you first tried it? Did reality match expectations?"
5. **Forces analysis**: Map push (old solution pain), pull (new solution appeal), anxiety (switching fears), habit (inertia).

See `references/jtbd-deep-dive.md` for complete interview guide and force diagram template.

## User Journey Mapping

### Journey Map Structure

```
Stage 1: Awareness → Stage 2: Consideration → Stage 3: Purchase → Stage 4: Onboarding → Stage 5: Habitual Use → Stage 6: Advocacy
```

For each stage, document:
- **Actions**: What is the user doing?
- **Touchpoints**: Which channels/features are they interacting with?
- **Thoughts**: What are they thinking? (use quotes from research)
- **Emotion**: Plot on -5 (frustrated) to +5 (delighted) scale
- **Pain points**: Where does friction occur?
- **Opportunities**: What could improve this stage?

### High-Value Scenario Signals in Journey Maps

Look for these patterns that indicate high-value scenarios:

| Signal | What It Means | Action |
|--------|--------------|--------|
| Deep emotion valleys (< -3) | Strong pain = willingness to pay for solution | Prioritize fixing |
| Drop-off between stages | Users abandoning at specific transition | Investigate cause |
| Workarounds mentioned | Users building manual processes | Productize the workaround |
| Delight peaks (> +3) | Moments users love = differentiate here | Double down |
| Repeated across personas | Universal pain = largest TAM | Strategic priority |
| Competitor mentioned | Users comparing alternatives | Competitive vulnerability |

See `references/journey-map-guide.md` for facilitation instructions and visualization templates.

## Scenario Scoring & Prioritization

### RICE-Based Scenario Scoring

Score each discovered scenario on 4 dimensions (1-10 scale):

| Dimension | Question | Weight |
|-----------|----------|--------|
| **Reach** | How many users experience this scenario monthly? | 1.0 |
| **Intensity** | How painful/frustrating is it? (1=minor annoyance, 10=blocker) | 1.2 |
| **Willingness-to-pay** | Would users pay for a solution? (1=nice-to-have, 10=must-have) | 1.0 |
| **Strategic fit** | Aligns with product vision? (1=misaligned, 10=core) | 0.8 |
| **Feasibility** | Can we build this well? (1=extremely hard, 10=straightforward) | 0.8 |

**Score = (Reach × Intensity × Willingness × Strategic fit) / (11 - Feasibility)**

Higher score = higher priority. Scenarios scoring >200 are typically P0/P1.

### Opportunity Canvas

For top 3-5 scenarios, complete an opportunity canvas:

```
**Scenario**: [One-line description]
**Current state**: [What users do today + associated pain]
**Desired state**: [What "great" looks like]
**Target users**: [Segment + estimated count]
**Value hypothesis**: [If we build X, then Y metric will improve by Z%]
**Key risk**: [Biggest unknown that could invalidate this opportunity]
**Validation approach**: [How to test before building — concierge MVP, landing page, prototype test]
**Estimated effort**: [T-shirt: S/M/L/XL]
```

## Aha Moment Discovery

For PLG (Product-Led Growth) products, identify the activation trigger:

1. **Correlate behaviors with retention**: Find actions that highly correlate with 7-day / 30-day retention
2. **Interview retained users**: "What moment made you decide to keep using [product]?"
3. **Map activation funnel**: Identify the specific step where non-activated users drop off
4. **Define activation criteria**: "User is activated when they complete [specific action] within [timeframe]"
5. **Optimize time-to-aha**: Reduce steps/delays between signup and activation moment

Common activation actions by product type:
- **Collaboration tool**: First collaborative doc shared
- **Analytics tool**: First dashboard created with real data
- **SaaS platform**: First team member invited
- **E-commerce**: First purchase completed
- **Social app**: First connection made + message sent

## Output Format

```markdown
# High-Value Scenario Discovery: [Product Area]

## Top Opportunities (Ranked)

### #1: [Scenario Name] — Score: [X]
**Job statement**: When [situation], I want to [motivation], so I can [expected outcome].
**Evidence**: [Data/quote support]
**User count**: [N] users/month
**Current pain**: [Description]
**Proposed solution**: [Direction]
**Validation plan**: [Approach]

### #2: [Scenario Name] — Score: [X]
...

## Journey Map Summary
[Key insight: where in the journey the highest-value opportunities lie]

## Activation Insights
[If applicable: Aha moment definition and optimization recommendations]

## Recommended Next Steps
1. [Action item with owner and timeline]
2. [Action item with owner and timeline]
```

## References

- **JTBD deep dive**: `references/jtbd-deep-dive.md` — Complete switch interview guide and force diagram
- **Journey map guide**: `references/journey-map-guide.md` — Facilitation instructions and templates
- **Prioritization frameworks**: `references/prioritization.md` — RICE, Kano, Opportunity scoring detailed formulas
