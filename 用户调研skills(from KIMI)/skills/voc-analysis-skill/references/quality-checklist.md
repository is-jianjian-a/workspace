# VOC Analysis Quality Checklist

Validation steps to ensure analysis accuracy and reliability.

## Pre-Analysis Checks

- [ ] Data source clearly documented (where feedback came from, date range)
- [ ] Sample size sufficient (minimum 100 items for statistical significance; 30 acceptable for qualitative)
- [ ] Data cleaned: duplicates removed, spam filtered, test data excluded
- [ ] Language detection performed: mixed-language data handled appropriately
- [ ] Product context understood: key features, recent releases, known issues reviewed

## Analysis Validation

- [ ] Sentiment calibration: manual spot-check 20-50 items against automated classification
  - Target: >80% agreement for rule-based, >90% for ML-based
  - If below target: adjust keyword lists or retrain model
- [ ] Theme coherence: check that items within each theme are semantically related
  - Look for: themes that are too broad ("general feedback") or too narrow (1-2 items)
  - Re-cluster if more than 20% of items could fit multiple themes
- [ ] Keyword accuracy: verify top keywords make sense in product domain
  - Add product-specific terms to custom dictionary if missing
- [ ] Temporal check: if date data available, verify trends are not artifacts of sample timing
  - Watch for: pre/post launch bias, seasonal effects, event-driven spikes

## Bias Detection

- [ ] Source bias: Are all channels represented proportionally?
  - App store reviews tend more negative; support tickets are inherently problem-focused
  - Weight or segment by channel when reporting
- [ ] Recency bias: Is the analysis over-weighting recent feedback?
  - Compare month-over-month distributions for consistency
- [ ] Vocal minority bias: Are power users or angry customers over-represented?
  - Check: segment analysis by user tenure, usage frequency, plan tier
- [ ] Selection bias: Was the sample self-selected (voluntary surveys)?
  - Note this limitation in report; triangulate with behavioral data

## Insight Quality

- [ ] Evidence-backed: Every insight has quantitative support + user quotes
- [ ] Actionable: Recommendations specify who should do what by when
- [ ] Prioritized: Findings ranked by business impact, not just frequency
- [ ] Balanced: Both problems AND positive feedback reported
- [ ] Contextualized: Compared to baseline or benchmark where possible

## Report Completeness

- [ ] Executive summary: 3-5 bullet points a stakeholder can read in 30 seconds
- [ ] Methodology section: How analysis was performed, limitations noted
- [ ] Sample characteristics: Total N, source breakdown, date range
- [ ] Raw quotes included: Verbatim user voice as evidence (anonymized)
- [ ] Recommendations: Specific, prioritized, with suggested owners
- [ ] Appendix: Full topic list, methodology notes, data quality flags
