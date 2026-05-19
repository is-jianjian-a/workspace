# Multi-Channel VOC Collection Setup

Guide for establishing feedback collection across 7 core channels.

## Channel 1: In-App Micro-Surveys

**Trigger events**:
- Feature used 3+ times (satisfaction with feature)
- Error encountered (frustration detection)
- Milestone completed (success moment capture)
- Session duration exceeds average by 2x (engagement check)

**Implementation**: Use tools like Hotjar, Survicate, or Pendo. Show 1-2 question micro-surveys to avoid disruption. Target <5% of sessions to prevent survey fatigue.

## Channel 2: Post-Interaction Email Surveys

**Timing**: Send CSAT survey 24 hours after support ticket resolution. Send NPS survey quarterly (not more frequently). Send onboarding feedback survey at day 7 and day 30.

**Template**:
```
Subject: Quick question about your recent [interaction]
Body: Hi [Name], You recently [action]. How did it go?
[1-5 star buttons inline]
[Optional: What could we improve?]
```

**Tools**: Typeform, Delighted, SatisMeter, or custom integration via email platform.

## Channel 3: Scheduled User Interviews

**Recruitment sources**:
- In-app recruitment banner ("Help us improve—book a 30-min call")
- Customer success team referrals (high-engagement or at-risk users)
- Churned user outreach ("We'd love to learn why you left")
- Incentivized panels (gift cards, swag, extended trials)

**Scheduling**: Use Calendly or Chili Piper. Offer multiple time slots across time zones. Send reminder 24 hours before.

## Channel 4: Support Ticket Analysis

**Categorization framework**:
Tag every ticket with: Topic (billing/login/feature bug/feature request), Product area, Sentiment (positive/neutral/negative), Resolution status.

**Key metrics to track monthly**:
- Top 10 ticket categories by volume
- Average resolution time by category
- Sentiment trend over time
- Escalation rate (tickets requiring supervisor intervention)

## Channel 5: Review Site Monitoring

**Sites to monitor**: G2, Capterra, TrustRadius, Apple App Store, Google Play, 知乎, 小红书, 微博.

**Process**: Set up Google Alerts or Brandwatch for brand mentions. Weekly review mining: extract top themes, sentiment distribution, feature requests, and competitive mentions. Respond to all reviews within 48 hours.

## Channel 6: Community & Social Media

**Community platforms**: Discord, Slack community, Reddit, Facebook Groups, 微信群, 知识星球.

**Monitoring approach**: Assign community manager to daily patrol. Use sentiment analysis on posts. Track "feature request" tag usage. Monthly community sentiment report.

## Channel 7: Behavioral Signals (Implicit Feedback)

**Metrics as implicit feedback**:
- Feature adoption rate (feature launched → % users trying it within 30 days)
- Time-to-completion (increasing = potential UX issue)
- Error rate by feature (correlates with support tickets)
- Activation rate (reaching "Aha moment")
- Retention cohort analysis (where do users drop off?)

**Tools**: Mixpanel, Amplitude, PostHog, or Heap for behavioral analytics.

## Integration: Unified VOC Dashboard

Consolidate all channels into a single view:
- Volume: Total feedback items by channel (monthly)
- Sentiment: Positive/negative/neutral distribution
- Top themes: Automated topic clustering across all text feedback
- Trending: Themes with significant month-over-month change
- Action items: Feedback routed to product teams with priority scores

Recommended tools: Productboard (feedback → roadmap), Canny (public feedback portal), Dovetail (research repository), or custom Notion/Airtable setup.
