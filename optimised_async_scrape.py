import asyncio
from playwright.async_api import async_playwright
import random

async def scroll_page_and_get_html(page, url: str) -> str:

    print(f"🌐 Opening: {url}")

    try:
        await page.goto(url, timeout=90000)
        await page.wait_for_load_state("domcontentloaded", timeout=90000)
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
            await page.evaluate("window.scrollBy(0, window.innerHeight * 0.9);")
            await asyncio.sleep(1.0)

            try:
                await page.wait_for_load_state("domcontentloaded", timeout=3000)
            except:
                pass

            curr_state = await page.evaluate(js_get_dom_state)
            stable_count = stable_count + 1 if curr_state == prev_state else 0
            if stable_count >= 2:
                break

            prev_state = curr_state

        # load lazy images
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


async def scrape_multiple(urls, proxies, concurrency_limit = 8):
    async with async_playwright() as p:

        # launch ONE browser
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

        # create ONLY ONE context
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
            java_script_enabled=True,
        )

        semaphore = asyncio.Semaphore(concurrency_limit)
        tasks = []

        async def scrape_single(url):
            async with semaphore:
                proxy_raw = random.choice(proxies)

                # Expect format: IP:PORT:USER:PASS
                try:
                    ip, port, user, pw = proxy_raw.split(":")
                except ValueError:
                    raise ValueError(f"Invalid proxy format: {proxy_raw}")

                proxy_config = {
                    "server": f"http://{ip}:{port}",
                    "username": user,
                    "password": pw
                }

                # 👉 CREATE CONTEXT WITH PROXY
                context = await browser.new_context(
                    proxy=proxy_config,
                    user_agent=(
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    ),
                    viewport={"width": 1920, "height": 1080},
                    java_script_enabled=True,
                )

                page = await context.new_page()
                html = await scroll_page_and_get_html(page, url)

                await context.close()
                return html

        for url in urls:
            tasks.append(scrape_single(url))

        results = await asyncio.gather(*tasks)

        await context.close()
        await browser.close()
        return results
