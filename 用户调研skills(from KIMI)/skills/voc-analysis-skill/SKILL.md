---
name: voc-analysis-skill
description: >
  Voice of Customer (VOC) analysis and user feedback insight extraction. Use when the task involves:
  (1) Analyzing user feedback, reviews, survey responses, or support tickets, (2) Extracting
  themes, sentiments, and insights from unstructured text data, (3) Processing customer comments
  from app stores, social media, or community forums, (4) Generating VOC reports with actionable
  recommendations, (5) Building feedback classification or prioritization systems, (6) Performing
  text mining, sentiment analysis, or topic modeling on user-generated content, or (7) Any task
  requiring transformation of raw user feedback into structured, actionable product insights.
  Supports Chinese and English text analysis with NLP pipelines and LLM-powered insight generation.
---

# VOC Analysis Skill

Transform raw user feedback into structured, actionable product insights through systematic text analysis.

## Core Workflow

1. **Ingest data**: Load feedback from CSV, JSON, API, or database
2. **Preprocess text**: Clean, tokenize, normalize text for analysis
3. **Analyze**: Run sentiment analysis, topic modeling, keyword extraction
4. **Synthesize**: Cluster findings into themes, identify patterns and anomalies
5. **Generate insights**: Translate data patterns into actionable product insights
6. **Deliver report**: Output structured VOC analysis report with evidence

## Analysis Stack Selection

Choose analysis approach based on data volume and complexity:

**Small dataset (<500 items) or quick analysis**:
→ Use LLM-powered analysis (GPT-4/Claude). Direct prompt: "Analyze these [N] user feedback items. Extract top themes, sentiment distribution, and actionable insights."
- Fast, no setup, handles nuanced language well
- Higher cost per item, less reproducible

**Medium dataset (500-10,000 items)**:
→ Use Python NLP pipeline: `Jieba` (Chinese) / `NLTK` (English) for tokenization + `SnowNLP` (Chinese) / `TextBlob`/`VADER` (English) for sentiment + `Gensim` for topic modeling.
- Reproducible, cost-effective, customizable
- Requires Python environment setup

**Large dataset (10,000+ items) or continuous pipeline**:
→ Use cloud NLP APIs: Alibaba Cloud NLP, Baidu NLP, AWS Comprehend, or Google Cloud Natural Language.
- Production-grade, scalable, pre-trained on domain data
- Higher ongoing cost, vendor lock-in

**Mixed-language or global products**:
→ Use `polyglot`, `spaCy` (multi-language), or cloud APIs with multi-language support. Ensure consistent preprocessing across languages.

## Preprocessing Pipeline

Always preprocess before analysis:

1. **Deduplication**: Remove exact duplicates and near-duplicates (use fuzzy matching for near-dupes)
2. **Noise removal**: Strip HTML tags, URLs, email addresses, phone numbers
3. **Normalization**: Convert to lowercase (English), unify whitespace, standardize punctuation
4. **Tokenization**: Split into words (English) or use `Jieba` (Chinese). Use `Jieba.lcut()` with custom dictionary for product-specific terms.
5. **Stopword removal**: Remove common words that carry no meaning (the, and, 的, 了, 是). Use domain-specific stopword lists for better results.
6. **Entity preservation**: Keep product names, feature names, and brand mentions intact during normalization.

## Sentiment Analysis

**Three-tier approach**:

1. **Polarity** (Positive/Negative/Neutral): Use for overall distribution and trend tracking.
2. **Intensity** (1-5 scale): Use for prioritization—intensity 4-5 items need immediate attention.
3. **Aspect-based sentiment**: Identify what specific feature/topic each sentiment refers to. E.g., "Great UI but terrible performance" → UI: positive, Performance: negative.

**Sentiment classification rules**:
- Count explicit sentiment words (great, terrible, love, hate, 好用, 难用)
- Weight by intensity modifiers (very, extremely, 非常, 太)
- Handle negation ("not bad" ≠ "bad")
- Detect sarcasm (requires context; flag uncertain cases for manual review)

## Topic Modeling & Theme Extraction

**Automated approach** (LDA with Gensim):
```python
from gensim import corpora, models

# After tokenization
dictionary = corpora.Dictionary(tokenized_texts)
corpus = [dictionary.doc2bow(text) for text in tokenized_texts]

# Optimal topic count: try 3-15, evaluate coherence score
lda_model = models.LdaModel(corpus, num_topics=8, id2word=dictionary)
topics = lda_model.print_topics(num_words=5)
```

**LLM-powered approach** (recommended for nuanced themes):
- Prompt: "Group these feedback items into 5-10 themes. Name each theme concisely. For each theme, provide: name, description, count, sentiment distribution, and 3 representative quotes."
- Advantages: Better handles implicit themes, generates human-readable labels, identifies cross-cutting concerns

**Hybrid approach** (best of both):
1. Use LDA to discover initial topic structure
2. Use LLM to name and describe topics in business language
3. Use LLM to classify edge cases that LDA misclassified

## Insight Generation Framework

Transform analysis outputs into actionable insights using the **"So What?" ladder**:

1. **Observation** (what the data shows): "35% of negative reviews mention 'slow loading'"
2. **Pattern** (what it means): "Performance is the #1 driver of dissatisfaction"
3. **Insight** (why it matters): "Users expect sub-2s load times; our 5s average violates this expectation"
4. **Recommendation** (what to do): "Prioritize image optimization and CDN implementation in next sprint"

## Output Format

```markdown
# VOC Analysis Report: [Product/Feature] — [Date Range]

## Executive Summary
- Total feedback analyzed: [N]
- Sentiment: [X]% Positive | [Y]% Neutral | [Z]% Negative
- Top insight: [One-sentence key finding]

## Sentiment Distribution
[Chart or table by channel/time]

## Top Themes
| Rank | Theme | Count | % of Total | Sentiment | Trend |
|------|-------|-------|------------|-----------|-------|
| 1 | Performance | 234 | 23% | Negative ↑ | Worsening |
| 2 | Onboarding | 189 | 19% | Mixed → | Stable |

## Key Insights
### Insight 1: [Title]
**Evidence**: [Data point + 2-3 user quotes]
**Impact**: [User segments affected, business impact]
**Recommendation**: [Specific action, owner, timeline]

## Appendix
- Methodology note
- Raw data sample
- Analysis code (if applicable)
```

## References

- **NLP pipeline setup**: `references/nlp-pipeline.md` — Python code for full analysis pipeline
- **Prompt library**: `references/prompt-library.md` — LLM prompts for different analysis tasks
- **Quality checklist**: `references/quality-checklist.md` — Validation steps for analysis accuracy
