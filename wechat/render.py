from typing import Literal

from playwright.async_api import async_playwright


async def html_to_image(
    html: str,
    path: str | None = None,
    dom: str | None = None,
    quality: int | None = None,
    type: Literal["jpeg", "png"] = "png",
) -> bytes:
    """html渲染为图片.

    Args:
        html (str): html内容.
        path (str | None, optional): 图片保存路径.
        dom (str | None, optional): 定位dom元素如: "#main".
        quality (int | None, optional): 图片质量1~100.
        type (Literal[&quot;jpeg&quot;, &quot;png&quot;], optional):图片类型.

    Returns:
        bytes: 图片.
    """
    async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch()
        page = await browser.new_page()
        await page.set_content(html, wait_until="load")
        if dom:
            page = page.locator(dom)
        return await page.screenshot(path=path, type=type, quality=quality)


async def url_to_image(
    url: str,
    path: str | None = None,
    dom: str | None = None,
    quality: int | None = None,
    type: Literal["jpeg", "png"] = "png",
) -> bytes:
    """html渲染为图片.

    Args:
        url (str): url.
        path (str | None, optional): 图片保存路径.
        dom (str | None, optional): 定位dom元素如: "#main".
        quality (int | None, optional): 图片质量1~100.
        type (Literal[&quot;jpeg&quot;, &quot;png&quot;], optional):图片类型.

    Returns:
        bytes: 图片.
    """
    async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch()
        page = await browser.new_page()
        await page.goto(url, timeout=60000, wait_until="load")
        if dom:
            page = await page.wait_for_selector(dom)
        return await page.screenshot(path=path, type=type, quality=quality)
