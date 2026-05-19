# Prioritization Frameworks

Detailed formulas and templates for evaluating product opportunities.

## 1. RICE Scoring

**Formula**: `RICE = (Reach × Impact × Confidence) / Effort`

| Factor | Scale | How to Estimate |
|--------|-------|----------------|
| **Reach** | Users/quarter | Count or estimate users affected in one quarter |
| **Impact** | 0.25 (minimal), 0.5 (low), 1 (medium), 2 (high), 3 (massive) | Effect on target metric per user |
| **Confidence** | % (50%=low, 80%=medium, 100%=high) | Evidence strength |
| **Effort** | Person-months | Engineering + design + PM time |

**Example**: Auto-categorize expenses
- Reach: 5,000 users/quarter = 5
- Impact: 2 (high — saves 2+ hours/month per user)
- Confidence: 80% (user research + competitor data)
- Effort: 3 person-months = 3
- **RICE = (5 × 2 × 0.8) / 3 = 2.67**

Interpretation: RICE > 5 = Do immediately. 2-5 = Strong candidate. < 2 = Deprioritize or reconsider scope.

## 2. Kano Model Classification

Classify features by user reaction to categorize as:

| Category | User Reaction | Strategy |
|----------|--------------|----------|
| **Must-have** (Basic) | Dissatisfied if absent, neutral if present | Must build. Table stakes. |
| **Performance** | Linear satisfaction — better = happier | Invest proportionally. Key differentiator. |
| **Exciter** (Delighter) | Neutral if absent, delighted if present | Surprise users. Build if low effort. |
| **Indifferent** | Don't care either way | Don't build. |
| **Reverse** | Prefer absence | Actively remove. |

**Kano questionnaire template** (ask for each feature):
- Functional question: "If [product] has [feature], how would you feel?" (Like/Expect/Neutral/Tolerate/Dislike)
- Dysfunctional question: "If [product] does NOT have [feature], how would you feel?" (Same scale)

**Classification matrix**:
| | Like | Expect | Neutral | Tolerate | Dislike |
|---|------|--------|---------|----------|---------|
| **Like** | Q | A | A | A | O |
| **Expect** | R | I | I | I | M |
| **Neutral** | R | I | I | I | M |
| **Tolerate** | R | I | I | I | M |
| **Dislike** | R | R | R | R | Q |

A = Attractive (Exciter), M = Must-have, O = One-dimensional (Performance), I = Indifferent, R = Reverse, Q = Questionable

## 3. Opportunity Score (Weight-Adjusted)

For scenario mining specifically, use this weighted formula:

```
Opportunity Score = (Reach × Intensity × WTP × Strategic_Fit) / (11 - Feasibility)

Where:
- Reach: Monthly affected users (1=10s, 10=10000s+)
- Intensity: Pain severity (1-10)
- WTP: Willingness to pay (1-10)
- Strategic_Fit: Alignment with vision (1-10)
- Feasibility: Implementation ease (1-10)
```

**Scoring thresholds**:
- 300+: P0 — Strategic initiative, allocate team immediately
- 150-300: P1 — Strong opportunity, validate and plan
- 50-150: P2 — Worth exploring if resources available
- <50: P3 — Icebox, monitor but don't actively pursue

## 4. Value vs. Effort Matrix

Quick visual prioritization when data is limited:

```
        Low Effort          High Effort
       ┌─────────────────┬─────────────────┐
High   │   QUICK WINS    │  MAJOR PROJECTS │
Value  │  (Do first)     │  (Plan carefully)│
       ├─────────────────┼─────────────────┤
Low    │  FILL-INS       │  AVOID/RETHINK  │
Value  │  (Low priority) │  (High risk)    │
       └─────────────────┴─────────────────┘
```

Use this for initial triage, then apply RICE or Opportunity Score for detailed ranking.

## 5. Comparison: When to Use Which

| Framework | Best For | Data Required | Speed |
|-----------|----------|---------------|-------|
| **RICE** | Feature backlog prioritization | User counts, effort estimates | Medium |
| **Kano** | Feature categorization | Survey data (20+ responses) | Slow |
| **Opportunity Score** | New scenario discovery | User research + market data | Medium |
| **Value/Effort** | Quick triage, low data | Rough estimates | Fast |

**Recommended**: Start with Value/Effort for initial triage. Use Opportunity Score for top candidates. Use RICE for roadmap construction. Use Kano for feature-set definition.
