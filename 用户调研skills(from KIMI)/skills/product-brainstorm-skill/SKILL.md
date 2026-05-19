---
name: product-brainstorm-skill
description: >
  Product ideation, creative problem-solving, and concept generation facilitation. Use when the task involves:
  (1) Brainstorming product features, directions, or solutions to user problems,
  (2) Running structured ideation workshops using design thinking or innovation frameworks,
  (3) Generating creative solutions to specific product challenges or user pain points,
  (4) Evaluating and prioritizing product concepts or feature ideas,
  (5) Using frameworks like SCAMPER, Six Thinking Hats, or Double Diamond for structured ideation,
  (6) Creating user stories, problem statements, or hypothesis statements from raw ideas,
  (7) Designing concept validation experiments or MVPs to test ideas, or (8) Any task requiring
  divergent thinking to generate product ideas followed by convergent thinking to select
  the most promising directions. Covers both solo ideation and team workshop facilitation.
---

# Product Brainstorm Skill

Structured creative problem-solving for product direction exploration and concept generation.

## Core Workflow

1. **Frame the problem**: Define clear problem statement or opportunity space
2. **Diverge**: Generate maximum quantity of ideas using structured techniques
3. **Cluster & organize**: Group related ideas, remove duplicates
4. **Converge**: Evaluate ideas using objective criteria, select top candidates
5. **Conceptualize**: Flesh out selected ideas into testable concepts
6. **Validate plan**: Design quick validation experiments for top concepts

## Problem Framing

Before ideation, ensure the problem is well-defined. Use these formats:

**"How Might We" (HMW) statement**:
"How might we [desired outcome] for [user] who is [constraint/context]?"

Example: "How might we help remote workers stay focused for deep work sessions without feeling isolated?"

**Problem hypothesis**:
"We believe [user type] has a problem [doing/getting/achieving] because [obstacle]. If we solve this, they will [benefit]."

Example: "We believe freelance designers have a problem invoicing clients because current tools don't handle milestone-based payments. If we solve this, they will save 2 hours/week on admin."

## Divergent Thinking Techniques

### Technique 1: SCAMPER
Systematically explore modifications to existing solutions:

- **S**ubstitute: What component, material, person, or process could we replace?
- **C**ombine: What could we merge with another product, feature, or service?
- **A**dapt: What existing solution (from another industry) could we borrow from?
- **M**odify/Magnify/Minify: What could we change in scale, shape, frequency, or attribute?
- **P**ut to other use: What other contexts or users could benefit from this?
- **E**liminate: What could we remove or simplify without losing core value?
- **R**everse/Rearrange: What if we flipped the order, timeline, or ownership model?

Use each letter as a prompt to generate 3-5 ideas. Do not skip letters even if they seem irrelevant — forced constraints spark unexpected creativity.

### Technique 2: Six Thinking Hats (Evaluation)
After initial ideation, evaluate concepts from 6 perspectives:

| Hat | Perspective | Questions |
|-----|------------|-----------|
| White | Facts & data | What data supports this? What do we know? |
| Red | Emotion & intuition | How does this feel? What's my gut reaction? |
| Black | Caution & risks | What could go wrong? What are the risks? |
| Yellow | Optimism & benefits | What's the best-case outcome? Who benefits? |
| Green | Creativity & alternatives | What variations exist? What if we changed X? |
| Blue | Process & meta | Are we asking the right question? What's our thinking process? |

Run each hat for 3-5 minutes. Capture output per hat separately before synthesizing.

### Technique 3: Analogous Inspiration
Look outside the immediate domain for solutions:

1. **Identify the abstract job**: What is the user fundamentally trying to do? (e.g., "feel confident about their decision")
2. **Find analogies**: Where else does this job get done well? (e.g., wine ratings help buyers feel confident; travel reviews reduce booking anxiety)
3. **Borrow mechanisms**: What specific mechanism from the analogy could transfer? (e.g., expert curation + peer validation = decision confidence)
4. **Adapt to context**: How would this work in our product's context?

### Technique 4: Constraint Removal
Systematically remove constraints to find new possibilities:

"What would we build if..."
- Money was unlimited?
- Users had infinite technical literacy?
- There were no regulatory restrictions?
- We had 10x the engineering team?
- Users never made mistakes?
- We had to ship in 1 week?

Then identify which "unconstrained" ideas have a feasible core worth exploring.

See `references/ideation-techniques.md` for 6 additional advanced techniques including "Bad Ideas First", "Assumption Reversal", and "User Persona Swap".

## Convergent Thinking: Evaluation Framework

### Step 1: Initial Triage
Apply **3 filters** to quickly eliminate weak ideas:

1. **User desirability**: Does a real user actually want this? (Evidence required — no "users would love this" without backing)
2. **Strategic alignment**: Does this support our product vision and business goals?
3. **Technical feasibility**: Can we realistically build this with available resources?

Ideas failing any filter go to an "icebox" list, not trash — revisit quarterly.

### Step 2: Deep Evaluation (for ideas passing triage)
Score remaining ideas on:

| Criterion | Weight | Score (1-5) |
|-----------|--------|-------------|
| User impact (how many users, how deeply) | 1.5x | |
| Strategic fit | 1.0x | |
| Differentiation (vs. competitors) | 1.0x | |
| Revenue potential | 1.0x | |
| Effort to MVP (inverse: lower effort = higher score) | 1.0x | |
| Confidence in success (evidence strength) | 0.8x | |

**Total = sum of (weight × score)**. Sort descending. Top 20% proceed to concept development.

### Step 3: Portfolio Check
Before finalizing, verify the selected set has balance:
- Short-term wins (ship in 1-2 sprints) + Long-term bets (2-3 quarters)
- Low-risk improvements + High-risk innovations
- User-facing features + Infrastructure/platform work

If lopsided, adjust by adding/removing ideas to achieve balance.

## Concept Development

For each top idea, develop a **Concept Brief**:

```markdown
## Concept: [Name]

### Problem Statement
[Clear description of the user problem being solved]

### Proposed Solution (1-paragraph)
[What it is and how it works from user perspective]

### User Story
"As a [persona], I want to [action], so that [outcome]."

### Key Hypothesis
"We believe [solution] will [outcome] because [reasoning]."

### Success Metrics
- Primary: [The one metric that validates the hypothesis]
- Secondary: [Supporting metrics]

### MVP Scope
[Minimum version to test hypothesis — what to include and exclude]

### Validation Plan
[How to test with minimal investment — see validation options below]

### Estimated Effort
[T-shirt size: S/M/L/XL with rough person-week estimate]

### Open Questions
[Key unknowns that could invalidate this concept]
```

## Validation Options

Match validation approach to concept risk:

| Risk Level | Validation Method | Timeline | Cost |
|-----------|------------------|----------|------|
| Low (incremental improvement) | A/B test on existing feature | 2-4 weeks | Low |
| Medium (new feature) | Prototype test with 5 users | 1-2 weeks | Medium |
| High (new direction) | Landing page + waitlist test | 1-2 weeks | Low |
| Very High (new product) | Concierge MVP / Wizard of Oz | 2-4 weeks | Medium |

See `references/validation-playbook.md` for detailed experiment design templates.

## Solo Brainstorm Protocol

When facilitating ideation alone (without team):

1. **Input gathering** (20 min): Review user research, analytics, competitor analysis
2. **Divergent burst** (15 min): Use SCAMPER, generate at least 20 ideas — no filtering
3. **Rest** (10 min): Step away — subconscious processing improves creativity
4. **Clustering** (10 min): Group ideas by theme, identify patterns
5. **Convergent evaluation** (15 min): Apply evaluation framework, select top 5
6. **Concept briefs** (30 min): Develop briefs for top 3-5 ideas
7. **Reality check** (10 min): Review against constraints — adjust if needed

Total: ~2 hours for structured solo ideation session.

## Workshop Facilitation (Team)

For 4-8 person team workshops (2-3 hours):

**Preparation**: Send problem brief 2 days ahead. Prepare Miro board with templates.

**Agenda**:
- 0:00 Problem framing (10 min) — align on what we're solving
- 0:10 Warm-up (5 min) — quick silly ideation to lower inhibitions
- 0:15 Diverge Round 1: Individual ideation (15 min) — silent, each person generates 10+ ideas on sticky notes
- 0:30 Share & cluster (20 min) — each person shares top 3 ideas, group clusters by theme
- 0:50 Diverge Round 2: Build on clusters (15 min) — improve/combine ideas from Round 1
- 1:05 Evaluation (20 min) — dot vote on top ideas, then score with framework
- 1:25 Break (10 min)
- 1:35 Concept development (40 min) — break into pairs, develop concept briefs for top 2-3 ideas
- 2:15 Share & feedback (15 min) — each pair presents, group gives feedback
- 2:30 Next steps (10 min) — assign owners for validation, schedule follow-up

## Output Format

```markdown
# Brainstorm Session: [Topic]
## Problem Framed
[Problem statement / HMW question]

## Ideas Generated
Total: [N] ideas across [M] themes

### Theme 1: [Name]
- Idea 1 (Score: [X]): [Brief description]
- Idea 2 (Score: [X]): [Brief description]

## Top Concepts
### #1: [Concept Name] — Score: [X]
[Concept brief — problem, solution, hypothesis, validation plan]

### #2: [Concept Name] — Score: [X]
...

## Recommended Next Steps
1. [Validation experiment for #1 concept — owner, timeline]
2. [Validation experiment for #2 concept — owner, timeline]
3. [Icebox ideas to revisit — date]
```

## References

- **Ideation techniques**: `references/ideation-techniques.md` — 10 total techniques with step-by-step guides
- **Validation playbook**: `references/validation-playbook.md` — Experiment design templates for concept testing
