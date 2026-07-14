"""
Exporta cada slide do carousel.html como PNG 1080x1350.
Roda a partir do diretório do carrossel — lê ./carousel.html, escreve em ./slides/.
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE = Path(__file__).parent
INPUT_HTML = BASE / "carousel.html"
OUTPUT_DIR = BASE / "slides"
OUTPUT_DIR.mkdir(exist_ok=True)

VIEW_W = 420
VIEW_H = 525
SCALE = 1080 / 420


async def export_slides():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": VIEW_W, "height": VIEW_H},
            device_scale_factor=SCALE,
        )

        html_content = INPUT_HTML.read_text(encoding="utf-8")
        await page.set_content(html_content, wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Descobre total de slides via DOM
        total_slides = await page.evaluate(
            "document.querySelectorAll('.slide').length"
        )

        await page.evaluate(
            """() => {
            document.querySelectorAll('.ig-header,.ig-dots,.ig-actions,.ig-caption')
                .forEach(el => el.style.display='none');
            const frame = document.querySelector('.ig-frame');
            frame.style.cssText = 'width:420px;height:525px;max-width:none;border-radius:0;box-shadow:none;overflow:hidden;margin:0;padding:0;border:0;';
            const viewport = document.querySelector('.carousel-viewport');
            viewport.style.cssText = 'width:420px;height:525px;aspect-ratio:unset;overflow:hidden;cursor:default;';
            document.documentElement.style.cssText = 'padding:0;margin:0;background:#0F0505;';
            document.body.style.cssText = 'padding:0;margin:0;display:block;overflow:hidden;background:#0F0505;';
        }"""
        )
        await page.wait_for_timeout(500)

        for i in range(total_slides):
            await page.evaluate(
                """(idx) => {
                const track = document.querySelector('.carousel-track');
                track.style.transition = 'none';
                track.style.transform = 'translateX(' + (-idx * 420) + 'px)';
            }""",
                i,
            )
            await page.wait_for_timeout(400)

            out = OUTPUT_DIR / f"slide_{i+1}.png"
            await page.screenshot(
                path=str(out),
                clip={"x": 0, "y": 0, "width": VIEW_W, "height": VIEW_H},
            )
            print(f"  slide {i+1}/{total_slides} -> {out.name}")

        await browser.close()


asyncio.run(export_slides())
print(f"\nExport concluído: {OUTPUT_DIR}")
