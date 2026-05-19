# Playwright Scraping Patterns

Common code patterns for Playwright-based scraping scenarios.

## Pattern 1: Basic Page Scraping
```python
from playwright.async_api import async_playwright
import asyncio

async def scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://example.com', wait_until='networkidle')
        
        # Extract data with CSS selectors
        items = await page.query_selector_all('.item')
        data = []
        for item in items:
            title = await item.query_selector_eval('.title', 'el => el.textContent')
            price = await item.query_selector_eval('.price', 'el => el.textContent')
            data.append({'title': title.strip(), 'price': price.strip()})
        
        await browser.close()
        return data

asyncio.run(scrape())
```

## Pattern 2: API Interception (Bypass Frontend)
```python
# Intercept API calls that return JSON data
async def intercept_api(page):
    api_responses = []
    
    def handle_route(route, request):
        if 'api/' in request.url:
            route.continue_()
        else:
            route.continue_()
    
    page.on('response', lambda response: 
        api_responses.append(response) if 'api/' in response.url else None
    )
    
    await page.route('**/*', handle_route)
    await page.goto('https://example.com')
    
    # Parse JSON from API responses
    for resp in api_responses:
        if resp.status == 200:
            data = await resp.json()
            # process structured data directly
```

## Pattern 3: Infinite Scroll
```python
async def scroll_to_bottom(page, scroll_pause=2):
    last_height = await page.evaluate('document.body.scrollHeight')
    while True:
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await page.wait_for_timeout(scroll_pause * 1000)
        new_height = await page.evaluate('document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height
```

## Pattern 4: Stealth Context Setup
```python
async def create_stealth_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=True,
        args=['--disable-blink-features=AutomationControlled']
    )
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        locale='en-US',
        timezone_id='America/New_York',
    )
    
    # Apply all fingerprint masking
    page = await context.new_page()
    await page.add_init_script("""
        delete navigator.__proto__.webdriver;
        window.chrome = { runtime: {} };
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    """)
    return playwright, browser, page
```

## Pattern 5: Login & Session Persistence
```python
import json
import os

async def login_with_session(page, cookies_file='cookies.json'):
    if os.path.exists(cookies_file):
        cookies = json.load(open(cookies_file))
        await page.context.add_cookies(cookies)
        await page.goto('https://example.com/dashboard')
        # Check if still logged in
        if await page.query_selector('.user-profile'):
            return True
    
    # Perform login
    await page.goto('https://example.com/login')
    await page.fill('#username', 'user@example.com')
    await page.fill('#password', 'password')
    await page.click('#submit')
    await page.wait_for_url('**/dashboard')
    
    # Save cookies for next run
    cookies = await page.context.cookies()
    json.dump(cookies, open(cookies_file, 'w'))
    return True
```

## Pattern 6: Multi-tab Parallel Scraping
```python
async def scrape_multiple(urls, max_concurrent=5):
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def scrape_one(url):
        async with semaphore:
            page = await context.new_page()
            await page.goto(url, wait_until='domcontentloaded')
            data = await page.evaluate('''() => {
                return {
                    title: document.title,
                    h1: document.querySelector('h1')?.innerText || '',
                };
            }''')
            await page.close()
            return data
    
    results = await asyncio.gather(*[scrape_one(url) for url in urls])
    return results
```
