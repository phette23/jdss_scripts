from pathlib import Path

import click

from stats.scrape import InstitutionStats

from .scrape import scrape_urls


@click.command()
@click.help_option("-h", "--help")
@click.argument(
    "urls_file",
    type=click.Path(dir_okay=False, exists=True, readable=True, path_type=Path),
)
@click.option("-l", "--limit", help="max number of URLs to process", default=100)
def main(urls_file: Path, limit: int):
    urls: list[str] = []
    with Path.open(urls_file) as fh:
        urls.extend(fh.readlines())
    stats: list[InstitutionStats] = scrape_urls(urls, limit=limit)
    print(stats)  # TODO write to CSV
