import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def basic_anti_crawling_analysis(target_url, from_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": from_url
    }

    print(f"\n* Scanning target page:{target_url}")
    print("* Simulating static request (non-browser rendering)...")

    try:
        res = requests.get(target_url, headers=headers, timeout=10)

        if res.status_code != 200:
            print(f"[E] Return status code: {res.status_code}, indicating that access may be blocked or abnormal.")
            print("[W] The page may have protection mechanisms in place, such as a WAF or require a login.")
            return

        html = res.text.lower()
        score = 0
        checks = {
            "html": "<html" in html,
            "body": "<body" in html,
            "title": "<title" in html,
            "content-length": len(html) > 500
        }

        print("\n* Scan Details:")
        for key, result in checks.items():
            if result:
                score += 1
                print(f"[OK] {key} tag/content found.")
            else:
                print(f"[W] {key} was not found. There may be a reverse crawl or an incomplete page returned.")

        print("\n* Overall Anti-Crawling Assessment")
        if score == 4:
            print("[OK] The page has no obvious anti-crawling mechanism and is suitable for crawling with requests.")
        elif score >= 2:
            print("[W] The page is partially normal, but there are some missing parts. There may be slight anti-crawl or JS rendering is required.")
        else:
            print("[E] If the page content is abnormal or encounters serious anti-crawl, it is recommended to use Selenium or browser simulation instead.")

    except Exception as e:
        print("[E] Request error, it may be a network problem or the other party's server blocking:")
        print("[E] error message:", e)


def page_render_analysis(url):
    options = Options()
    options.add_argument("--headless")  # No head modle
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    print(f"\n* Analyzing website: {url}")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    html = driver.page_source
    title = driver.title.strip()
    
    # Determine whether JavaScript is executed (based on the class added by Modernizr to HTML)
    js_rendered = "class=\"js" in html.lower()

    # Try to get the H1 main content
    try:
        h1 = driver.find_element("tag name", "h1")
        h1_text = h1.text.strip()
        has_h1 = bool(h1_text)
    except:
        h1_text = ""
        has_h1 = False

    driver.quit()

    print("\n* Analysis Results:")

    if js_rendered:
        print("[OK] The webpage successfully executed JavaScript, indicating that automated browsers are not blocked.")
    else:
        print("[W] The webpage did not successfully execute JavaScript. There may be JS detection or redirection.")

    if title:
        print(f"[OK] The page title is: {title}, which means the content is partially loaded normally.")
    else:
        print("[W] The page has no title and may be incompletely loaded or redirected.")

    if has_h1:
        print(f"[OK] Found the main title of the page (H1): {h1_text}")
    else:
        print("[W] The page does not have an H1 main title, which may be due to content not being loaded, delayed loading, or anti-crawl processing.")

    print("\n* Overall Assessment:")
    if js_rendered and title and has_h1:
        print("[OK] The website has no obvious anti-crawler mechanism and is suitable for crawling.")
    else:
        print("[W] The website may have a mild anti-crawling mechanism or some content may need to wait for dynamic loading. It is recommended to use Selenium + delay processing.")


basic_anti_crawling_analysis("https://musicalmoon.com/", "https://google.com")
page_render_analysis("https://musicalmoon.com/")
