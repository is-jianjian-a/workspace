---
name: voc-research-skill
description: >
  Voice of Customer (VOC) research and user feedback collection. Use when the task involves:
  (1) Designing user research plans or VOC programs, (2) Creating surveys, questionnaires,
  interview guides, or NPS programs, (3) Conducting user interviews (JTBD, usability,
  exploratory), (4) Collecting user feedback from multiple channels (surveys, support tickets,
  social media, reviews, community forums), (5) Planning customer satisfaction measurement
  (CSAT, NPS, CES), (6) Building feedback portals or user research operations, or
  (7) Any task requiring systematic collection of user voice/feedback/insights for product
  decision-making. Covers both quantitative survey design and qualitative interview methodology.
---

# VOC Research Skill

Systematic user feedback collection through surveys, interviews, and multi-channel monitoring.

## Core Workflow

1. **Define research objective**: Clarify what decisions this research will inform
2. **Select methodology**: Choose quantitative (survey), qualitative (interview), or mixed methods
3. **Design instruments**: Create survey, interview guide, or feedback collection mechanism
4. **Recruit participants**: Define target user segments and sample size
5. **Execute collection**: Run survey, conduct interviews, or monitor channels
6. **Document & organize**: Structure raw data for analysis handoff

## Methodology Selection Matrix

| Research Goal | Method | Sample Size | Duration | Output |
|--------------|--------|-------------|----------|--------|
| Measure satisfaction trend | NPS/CSAT survey | 100+ | Ongoing | Score + drivers |
| Identify top problems | Feedback categorization | All available | 1-2 weeks | Priority list |
| Understand "why" behind data | User interviews | 8-15 | 2-3 weeks | Insight report |
| Validate feature ideas | Concept testing | 20-50 | 1 week | Viability score |
| Discover unmet needs | JTBD interviews | 10-20 | 2-4 weeks | Job statements |
| Map user journey | Journey mapping sessions | 5-10 | 1-2 weeks | Journey map |

## Survey Design Standards

Follow these principles for effective surveys:

**Structure**: Screening (2-3 Q) → Context (2-3 Q) → Core (5-10 Q) → Open (2-3 Q) → Demographics (3-5 Q). Total: 15-25 questions max, 3-5 minutes to complete.

**Question types**: Use rating scales (Likert 1-5/1-7, NPS 0-10) for quantifiable metrics. Use multiple choice for categorization. Use open-ended for "why" exploration (limit to 2-3 open questions to reduce fatigue).

**NPS question**: "On a scale of 0-10, how likely are you to recommend [product] to a friend or colleague?" Follow-up: "What is the primary reason for your score?"

**CSAT question**: "How satisfied were you with [specific interaction/feature]?" Scale: 1-5 (Very dissatisfied to Very satisfied).

**CES question**: "How easy was it to [complete task]?" Scale: 1-7 (Very difficult to Very easy).

## Interview Guide Templates

### Exploratory Interview (30-45 min)
1. **Warm-up** (5 min): Background, role, product usage context
2. **Current behavior** (10 min): Walk me through how you currently [do X]. What tools do you use?
3. **Pain points** (10 min): What's most frustrating about [current process]? Tell me about the last time this was difficult.
4. **Needs & motivations** (10 min): If you could wave a magic wand, what would change? What would "better" look like?
5. **Wrap-up** (5 min): Anything else? Who else should I talk to?

### JTBD Switch Interview (45-60 min)
1. **Purchase timeline** (10 min): When did you first start looking for a solution? What triggered the search?
2. **Consideration set** (10 min): What alternatives did you consider? Why did you reject each one?
3. **Decision moment** (10 min): What tipped you toward [our product]? What were you most anxious about?
4. **First use** (10 min): What happened when you first tried it? Did it meet expectations?
5. **Ongoing use** (10 min): How has your usage evolved? What keeps you using it?
6. **Forces analysis** (10 min): Push (what pushed you away from old solution)? Pull (what pulled you to new)? Anxiety (what worried you)? Habit (what held you back)?

See `references/interview-techniques.md` for advanced probing techniques and facilitation tips.

## Multi-Channel Feedback Collection

When tasked with building a VOC system, map these 7 channels:

1. **In-app surveys** (micro-surveys triggered by events: feature use, error occurrence, milestone completion)
2. **Email/post-interaction surveys** (CSAT after support ticket, NPS quarterly)
3. **User interviews** (recruited from power users, churned users, new signups)
4. **Support tickets & chat logs** (categorize by topic, sentiment, resolution time)
5. **App store & review site comments** (Apple App Store, Google Play, G2, Capterra, 知乎, 小红书)
6. **Social media & community** (brand mentions, product discussions, feature requests on forums)
7. **Behavioral signals** (feature adoption rates, drop-off points, time-on-task as implicit feedback)

## Output Format

Structure research deliverables as:

```markdown
# VOC Research Report: [Title]

## Research Objective
[What decision this research informs]

## Methodology
[Approach, sample size, timeline]

## Key Findings
1. [Finding with supporting quote/evidence]
2. [Finding with supporting quote/evidence]
3. [Finding with supporting quote/evidence]

## User Quotes (Raw Voice)
- "[Direct user quote]" — [User type, context]
- "[Direct user quote]" — [User type, context]

## Recommendations
1. [Specific, actionable recommendation with priority]
2. [Specific, actionable recommendation with priority]

## Appendix
[Interview guide, raw data summary, participant demographics]
```

## References

- **Interview techniques**: `references/interview-techniques.md` — Advanced probing, facilitation, note-taking methods
- **Survey templates**: `references/survey-templates.md` — NPS, CSAT, CES, product-market fit survey templates
- **Channel setup guide**: `references/channel-setup.md` — Setting up feedback collection across 7 channels
