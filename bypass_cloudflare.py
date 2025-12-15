import asyncio
from playwright.async_api import async_playwright

TARGET = "https://www.autoscout24.ch/fr/s"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        async def on_request(request):
            if request.resource_type in ("xhr", "fetch"):
                print("REQUEST ->", request.method, request.url)
                try:
                    post = await request.post_data()
                    if post:
                        print("  body:", post[:400])
                except:
                    pass
                print("  headers:", {k: request.headers.get(k) for k in ("referer", "origin", "user-agent")})

        async def on_response(response):
            req = response.request
            if req.resource_type in ("xhr", "fetch"):
                print("RESPONSE <-", response.status, response.url)

        page.on("request", on_request)
        page.on("response", on_response)

        await page.goto(TARGET, wait_until="domcontentloaded")
        print("Page ouverte — inspecte réseau, puis ferme manuellement quand tu as l'info.")
        # attendre user input pour fermer
        await page.wait_for_timeout(60000)
        await browser.close()

asyncio.run(main())
