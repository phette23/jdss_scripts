# Generate Stats Profile

Take CSV list of all SCELC institution landing pages and create a report so we can total up full public contribution of SCELC organizations.

Install the browser once with `uv run playwright install chromium`.

Usage:

```sh
> uv run stats data/urls.txt
> uv run stats --help
Usage: stats [OPTIONS] URLS_FILE

Options:
  -h, --help           Show this message and exit.
  -c, --csv FILE       path to output CSV file
  -l, --limit INTEGER  max number of URLs to process
```

## Notes

JSTOR protects pages with a verification captcha so we cannot merely scrape the HTML pages and process with BeautifulSoup, we have to use [Playwright](https://playwright.dev/docs/intro). The browser window will open, we complete the verification, then that verification should persist as the script completes. To be polite, we wait for 2 seconds between page loads with the `pause` argument in the main `scrape_urls` function which is not exposed via the CLI.
