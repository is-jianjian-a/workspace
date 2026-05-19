# LLM Prompt Library for VOC Analysis

Ready-to-use prompts for LLM-powered feedback analysis. Adapt based on product context.

## Prompt 1: Theme Extraction

```
You are a senior product analyst. Analyze the following user feedback items and extract themes.

Feedback items:
{feedback_list}

For each theme, provide:
- Theme name (2-4 words)
- Description (1 sentence)
- Count of items in this theme
- Sentiment distribution (positive/neutral/negative)
- 2-3 representative user quotes (verbatim)

Rules:
- Group into 5-10 themes maximum
- Use business language, not technical jargon
- Highlight cross-cutting themes that appear across multiple features
- Flag any urgent or safety-related issues separately

Output as structured markdown.
```

## Prompt 2: Sentiment Deep-Dive

```
Analyze the sentiment of these user reviews with nuance:

Reviews:
{reviews}

For each review:
1. Overall polarity (positive/mixed/negative)
2. Aspect-based sentiment: rate each aspect (1-5) — UI/UX, Performance, Features, Support, Value
3. Emotional tone (frustrated, excited, neutral, disappointed, grateful)
4. Intensity (1-5, how strongly expressed)

Flag:
- Contradictory statements ("love the design but hate the speed")
- Implicit complaints (things users workaround rather than report)
- Feature requests disguised as complaints
```

## Prompt 3: Insight Synthesis

```
Transform these VOC analysis results into actionable product insights.

Analysis data:
{analysis_results}

For each insight:
1. **Observation**: What the data shows (with specific numbers)
2. **Pattern**: What's changing or consistent over time
3. **Root cause hypothesis**: Why this is happening (3 possible explanations)
4. **Impact assessment**: Who is affected, severity, business risk
5. **Recommendation**: Specific action item with priority (P0/P1/P2) and owner suggestion

Prioritize insights by: frequency × severity × strategic alignment.
Format as executive briefing with "So What?" for each finding.
```

## Prompt 4: Competitive Signal Detection

```
Analyze these user reviews for competitive intelligence signals:

Reviews:
{reviews}

Extract:
1. **Competitor mentions**: Which competitors are named, in what context
2. **Switch signals**: Users comparing us to competitors, considering switching
3. **Feature gaps**: Features competitors have that users want from us
4. **Advantage signals**: What users say we do better than alternatives
5. **Market positioning clues**: How users categorize us vs. competitors

Output: Competitive threat matrix with severity ratings.
```

## Prompt 5: Prioritization Framework

```
Given these user feedback themes and product roadmap constraints, prioritize:

Themes:
{themes_with_counts}

Constraints:
- Engineering capacity: {N} sprints
- Strategic focus: {business_goals}
- Technical debt budget: {percentage}%

Apply RICE scoring:
- Reach: How many users affected (1-10)
- Impact: Business value if solved (1-10)
- Confidence: Evidence strength (0-1)
- Effort: Engineering weeks (1-10)

RICE Score = (Reach × Impact × Confidence) / Effort

Output prioritized backlog with top 5 recommendations.
```
