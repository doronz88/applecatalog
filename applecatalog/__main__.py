import logging
import os
from pathlib import Path
from pprint import pprint

import click
import coloredlogs

from applecatalog.catalog import Catalog, ProductInfo

coloredlogs.install(level=logging.DEBUG)

logging.getLogger('urllib3.connectionpool').disabled = True


def extract_package(filename: Path, out_dir: Path) -> None:
    assert 0 == os.system(f'pkgutil --expand "{filename}" "{out_dir}"')
    payload = os.path.join(out_dir, 'Payload')
    assert 0 == os.system(f'tar xf "{payload}" -C "{out_dir}"')


def get_unique_product(match: str) -> ProductInfo:
    products = []
    for product in Catalog().products(detailed=False):
        if product.basename and match in product.basename:
            products.append(product)
    assert len(products) == 1
    return products[0]


def get_xprotect_product() -> ProductInfo:
    return get_unique_product('XProtectPayloads')


@click.group()
def cli():
    pass


@cli.command()
def date():
    """ last update date """
    print(Catalog().date)


@cli.command('list')
@click.option('--macos', is_flag=True)
@click.option('-q', '--quick', is_flag=True, help='don\'t require extended information')
def list(macos: bool, quick: bool):
    """ list all products """

    catalog = Catalog()
    if macos:
        for k in catalog.macos_products:
            print(k)
        return
    for product in catalog.products(detailed=not quick):
        print(product)


@cli.command('download')
@click.argument('product_id')
@click.argument('out_dir', type=click.Path(dir_okay=True, exists=False))
def download(product_id: str, out_dir: str):
    """ download a single product packages """
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True, parents=True)
    Catalog().download(product_id, out_dir)


@cli.command('info')
@click.argument('product_id')
def info(product_id: str):
    """ query info for a single product """
    pprint(Catalog().get_product(product_id))


if __name__ == '__main__':
    cli()
