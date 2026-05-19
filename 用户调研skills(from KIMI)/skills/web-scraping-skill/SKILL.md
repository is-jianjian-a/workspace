---
name: web-scraping-skill
description: >
  Professional web scraping and data extraction automation. Use when the task involves:
  (1) Extracting data from websites, APIs, or online sources, (2) Building web crawlers or spiders,
  (3) Collecting structured or unstructured data from the internet, (4) Monitoring website changes,
  (5) Scraping product reviews, prices, articles, or social media content, (6) Bypassing anti-bot
  measures for legitimate data collection, or (7) Any task requiring automated browser interaction
  or HTTP-based data retrieval. Covers static HTML parsing, JavaScript-rendered dynamic content,
  API interception, proxy rotation, fingerprint masking, and data pipeline construction.
---

# Web Scraping Skill

Execute web scraping tasks through a systematic workflow: analyze target → select stack → implement → validate → deliver.

## Core Workflow

1. **Analyze target site**: Determine static vs dynamic rendering, identify data location (HTML/JSON/API/JS-rendered), check robots.txt and anti-bot measures
2. **Select technology stack**: Choose tools based on target complexity (see "Stack Selection" below)
3. **Implement crawler**: Write extraction code with proper error handling, retries, and rate limiting
4. **Handle anti-bot measures**: Apply fingerprint masking and proxy rotation if needed
5. **Validate output**: Verify data completeness, correctness, and format
6. **Deliver data**: Export to requested format (CSV/JSON/Excel/Database)

## Stack Selection

Determine the appropriate stack based on target characteristics:

**Static HTML content** (no JS rendering):
→ Use `requests` + `BeautifulSoup` or `requests` + `lxml`
- Fast, lightweight, minimal resource usage
- Good for: news articles, simple listing pages, basic HTML tables

**Dynamic JavaScript-rendered content** (React/Vue/SPA):
→ Use `Playwright` (preferred) or `Puppeteer`
- Full browser automation, handles JS rendering, API interception
- Playwright advantages: cross-browser, built-in stealth, async support, faster than Selenium

**Large-scale distributed crawling**:
→ Use `Scrapy` + `Playwright` integration
- Async architecture, built-in middleware pipeline, scheduling, data export
- Add `scrapy-playwright` for JS-rendered pages

**Cloud/managed scraping** (avoid infrastructure):
→ Use `Apify`, `ScrapingBee`, or `Bright Data`
- Managed proxy rotation, browser fingerprinting, CAPTCHA solving
- Higher cost but zero infrastructure maintenance

## Anti-Bot Countermeasures

When encountering Cloudflare, DataDome, or custom anti-bot systems, apply in order:

1. **Browser fingerprint masking** (Playwright): Use `add_init_script` to override `navigator.webdriver`, modify WebGL/Canvas fingerprints, set realistic viewport and timezone. See `references/fingerprint-masking.md` for complete 12-dimension checklist.
2. **Proxy rotation**: Rotate residential or datacenter proxies per request. Integrate `Scrapy-Proxy-Pool` or Playwright's `proxy` context option.
3. **Request behavior humanization**: Random delays (1-5s), realistic mouse movements, scroll patterns, session persistence with cookies.
4. **API interception**: Monitor Network tab for XHR/Fetch API calls that return structured JSON—often easier than parsing HTML.
5. **Headed mode debugging**: Run browser in headed mode with slow motion to visually diagnose detection points.

## Rate Limiting & Compliance

Always implement these guardrails:
- Respect `robots.txt` directives
- Rate limit: max 1-2 requests/second to same domain
- Add randomized delays between requests
- Set proper User-Agent string
- Implement exponential backoff for retries (max 3 retries)
- Never scrape personal data or bypass authentication for non-public content
- Check target website's Terms of Service

## Output Format

Structure the final deliverable as:

```
## Scraping Summary
- Target: [URL/pattern]
- Records extracted: [count]
- Fields: [list of extracted fields]
- Duration: [time taken]

## Sample Data (first 3 rows)
[formatted preview]

## Full Data
[file path or inline data]
```

## References

- **Fingerprint masking checklist**: `references/fingerprint-masking.md` — 12-dimension browser fingerprint evasion guide
- **Playwright patterns**: `references/playwright-patterns.md` — Common Playwright snippets for scraping scenarios
- **Scrapy integration**: `references/scrapy-patterns.md` — Scrapy spider templates and middleware configuration
