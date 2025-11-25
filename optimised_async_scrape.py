import asyncio
from playwright.async_api import async_playwright
import random
from proxies import PROXIES

async def scroll_page_and_get_html(page, url: str) -> str:
    print(f"🌐 Opening: {url}")

    try:
        await page.goto(url, timeout=90000)
        await page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(2)

        js_get_dom_state = """
        () => ({
            height: document.body.scrollHeight,
            images: document.images.length,
            nodes: document.querySelectorAll('body *').length
        })
        """

        prev_state = await page.evaluate(js_get_dom_state)
        stable_count = 0

        for _ in range(100):
            await page.evaluate("window.scrollBy(0, window.innerHeight * 0.6);")
            await asyncio.sleep(1)

            curr_state = await page.evaluate(js_get_dom_state)
            stable_count = stable_count + 1 if curr_state == prev_state else 0
            if stable_count >= 2:
                break
            prev_state = curr_state

        await page.evaluate("""
            const els = Array.from(document.querySelectorAll('img, source'));
            els.forEach(el => el.scrollIntoView());
            window.scrollTo(0, 0);
        """)
        await asyncio.sleep(1)

        html = await page.content()
        print(f"✅ DONE: {url} ({len(html)} chars)")
        return html

    except Exception as e:
        print(f"❌ Error on {url}: {e}")
        return ""

    finally:
        await page.close()


async def scrape_multiple(urls, proxies, concurrency_limit=8):
    async with async_playwright() as p:

        # 1) Launch one browser
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-infobars",
                "--window-size=1920,1080",
            ],
        )

        # 2) Create a dedicated context per proxy (best architecture)
        proxy_contexts = []
        for proxy_raw in proxies:
            ip, port, user, pw = proxy_raw.split(":")

            ctx = await browser.new_context(
                proxy={
                    "server": f"http://{ip}:{port}",
                    "username": user,
                    "password": pw,
                },
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1920, "height": 1080},
                java_script_enabled=True,
            )

            proxy_contexts.append(ctx)

        # Round robin index
        ctx_index = 0

        semaphore = asyncio.Semaphore(concurrency_limit)
        results = []

        async def scrape_single(url):
            nonlocal ctx_index
            async with semaphore:

                # Pick next proxy context in round-robin fashion
                ctx = proxy_contexts[ctx_index]
                ctx_index = (ctx_index + 1) % len(proxy_contexts)

                page = await ctx.new_page()
                html = await scroll_page_and_get_html(page, url)
                return html

        tasks = [scrape_single(url) for url in urls]
        results = await asyncio.gather(*tasks)

        # Cleanup
        for ctx in proxy_contexts:
            await ctx.close()

        await browser.close()
        return results

if __name__ == "__main__":
    # https://www.bloomingdales.com/shop/sale/men/?id=1001174
    # https://www.farfetch.com/in/shopping/men/sale/all/items.aspx
    urls = ["https://www.bloomingdales.com/shop/sale/men/?id=1001174"]
    proxies = PROXIES
    results = asyncio.run(scrape_multiple(urls, proxies))
    html_output = "\n".join(results) if isinstance(results, list) else results
    with open("bloomingdates.html", "w") as f:
        f.write(html_output)