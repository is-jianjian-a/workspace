# Browser Fingerprint Masking — 12 Dimension Checklist

Complete checklist for evading bot detection systems (Cloudflare, DataDome, PerimeterX, custom WAF).

## 1. navigator.webdriver
```python
page.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });
""")
```

## 2. WebGL Fingerprint
Override `getParameter` to return realistic GPU vendor/renderer:
```python
page.add_init_script("""
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
        if (parameter === 37445) return 'Intel Inc.';       // UNMASKED_VENDOR_WEBGL
        if (parameter === 37446) return 'Intel Iris Xe';    // UNMASKED_RENDERER_WEBGL
        return getParameter(parameter);
    };
""")
```

## 3. Canvas Fingerprint (Noise)
```python
page.add_init_script("""
    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
    HTMLCanvasElement.prototype.toDataURL = function(type) {
        const result = originalToDataURL.call(this, type);
        // Add imperceptible noise to pixel data to break fingerprinting
        return result;  // Advanced: modify pixel-level output
    };
""")
```

## 4. Timezone & Locale
```python
context = browser.new_context(
    locale='en-US',
    timezone_id='America/New_York',
    geolocation={'latitude': 40.7128, 'longitude': -74.0060}
)
```

## 5. Viewport & Screen Resolution
```python
context = browser.new_context(
    viewport={'width': 1920, 'height': 1080},
    screen={'width': 1920, 'height': 1080},  # screen resolution
    device_scale_factor=1,
)
```

## 6. User-Agent & Client Hints
```python
context = browser.new_context(
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    extra_http_headers={
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-mobile': '?0',
    }
)
```

## 7. Plugins
```python
page.add_init_script("""
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5]  // Return array with realistic length
    });
""")
```

## 8. Permissions API
```python
page.add_init_script("""
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' 
            ? Promise.resolve({state: Notification.permission})
            : originalQuery(parameters)
    );
""")
```

## 9. Iframe Consistency
Ensure iframe contexts match parent context timezone/locale settings. Playwright's `add_init_script` applies globally including iframes when using `page` level.

## 10. Chrome Runtime
```python
page.add_init_script("""
    window.chrome = { runtime: {} };
""")
```

## 11. Notification Permission
```python
page.add_init_script("""
    const originalNotification = window.Notification;
    Object.defineProperty(window, 'Notification', {
        get: function() {
            return originalNotification;
        }
    });
    Object.defineProperty(Notification, 'permission', {
        get: function() { return 'default'; }
    });
""")
```

## 12. Behavior Patterns
- Random delays: `page.wait_for_timeout(random.randint(1000, 5000))`
- Natural mouse: Move mouse in curves, not straight lines
- Realistic scroll: Variable speed, pause at content, scroll back occasionally
- Session persistence: Save/load cookies and localStorage across sessions
