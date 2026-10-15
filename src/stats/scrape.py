import re
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from playwright.sync_api import Browser, Page, sync_playwright


@dataclass
class InstitutionStats:
    collections: int
    items: int
    institution: str
    updated_date: datetime


items_collections_regex = re.compile(r"Search ([0-9,]+) items? in (\d+) collections?")


def process_page(page: Page) -> InstitutionStats | None:
    # TODO we could have another function for getting per-collection information
    title: str = page.locator('[data-qa="search-input-title"]').inner_text(
        timeout=120_000
    )
    print(title)
    items_collections: str = page.locator(".header-total-items").inner_text(
        timeout=120_000
    )
    print(items_collections)

    items_collections_matches: re.Match[str] | None = re.match(
        items_collections_regex, items_collections
    )
    if items_collections_matches:
        items: int = int(items_collections_matches.group(1).replace(",", ""))
        collections: int = int(items_collections_matches.group(2).replace(",", ""))
        return InstitutionStats(
            collections=collections,
            items=items,
            institution=title,
            updated_date=datetime.now(ZoneInfo("America/Los_Angeles")),
        )
    else:
        print("Error parsing collections data from page")


def scrape_urls(
    urls: list[str],
    *,
    limit: int = 100,
    pause: int = 2,
) -> list[InstitutionStats]:
    # pause for a MINIMUM of 2 seconds in between page loads
    pause = max(pause, 2)
    stats: list[InstitutionStats] = []

    with sync_playwright() as playwright:
        browser: Browser = playwright.chromium.launch(headless=False)
        try:
            page: Page = browser.new_page()
            for idx, url in enumerate(urls):
                if idx < limit and url:
                    response = page.goto(url, wait_until="domcontentloaded")
                    if response is not None:
                        print(f"HTTP {response.status} {response.url}")
                    # Collections info does not load immediately
                    page.wait_for_timeout(pause * 1_000)
                    data: InstitutionStats | None = process_page(page)
                    if data:
                        stats.append(data)
        finally:
            browser.close()

    return stats
