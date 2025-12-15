import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth


async def main():
    # -----------------------------
    # 1) LANCER PLAYWRIGHT + STEALTH
    # -----------------------------
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=False)

        # Contexte simple (pas d’UA custom pour éviter les faux positifs)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="fr-FR",
            extra_http_headers={
                "Accept-Language": "fr-FR,fr;q=0.9"
            }
        )

        page = await context.new_page()

        # -----------------------------
        # 2) LOGS POUR VOIR LES BLOQUAGES RÉSEAU
        # -----------------------------
        page.on("requestfailed", lambda req: print("❌ Request FAILED:", req.url))
        page.on("response", lambda res: print("Response", res.status, res.url))

        # -----------------------------
        # 3) OUVERTURE DE LA PAGE
        # -----------------------------
        print("Chargement de la page...")
        await page.goto("https://www.autoscout24.ch/fr/s", wait_until="domcontentloaded")

        print("URL finale =", page.url)
        await page.wait_for_timeout(3000)

        # -----------------------------
        # 4) TESTS DE DÉTECTION ANTI-BOT
        # -----------------------------
        print("\n=== ANALYSE ANTI-BOT ===")

        print("navigator.webdriver  =", await page.evaluate("() => navigator.webdriver"))
        print("navigator.plugins    =", await page.evaluate("() => navigator.plugins.length"))
        print("navigator.languages  =", await page.evaluate("() => navigator.languages"))
        print("WebGL disponible     =", await page.evaluate("() => !!window.WebGLRenderingContext"))

        # -----------------------------
        # 5) SCREENSHOT POUR VOIR L'ÉTAT DE LA PAGE
        # -----------------------------
        await page.screenshot(path="analyse_autoscout.png")
        print("\n📸 Screenshot enregistré : analyse_autoscout.png")

        await browser.close()


asyncio.run(main())
