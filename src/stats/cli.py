import csv
from pathlib import Path
from typing import Any

import click

from stats.scrape import InstitutionStats

from .scrape import scrape_urls


@click.command()
@click.help_option("-h", "--help")
@click.argument(
    "urls_file",
    type=click.Path(dir_okay=False, exists=True, readable=True, path_type=Path),
)
@click.option(
    "-c",
    "--csv",
    "output_file",
    default="data/jdss_stats.csv",
    help="path to output CSV file",
    type=click.Path(dir_okay=False, readable=True, path_type=Path),
)
@click.option("-l", "--limit", help="max number of URLs to process", default=100)
def main(urls_file: Path, output_file: Path, limit: int):
    urls: list[str] = []
    with Path.open(urls_file) as fh:
        urls.extend(fh.readlines())

    stats: list[InstitutionStats] = scrape_urls(urls, limit=limit)
    print(f"Got data for {len(stats)} institutions, writing to {output_file}")

    with Path.open(output_file, "w") as fh:
        writer = csv.writer(fh)
        header_row: list[str] = ["Institution", "Collections", "Items", "URL"]
        writer.writerow(header_row)
        print("\t".join(header_row))
        for org in stats:
            org_info: list[Any] = [
                org.institution,
                str(org.collections),
                str(org.items),
                org.url,
            ]
            writer.writerow(org_info)
            # TODO rich table
            print("\t".join(org_info))
