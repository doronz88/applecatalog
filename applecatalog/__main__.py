import logging
from pathlib import Path
from pprint import pprint

import click
import coloredlogs

from applecatalog.catalog import Catalog, MacOsCatalog, RosettaCatalog

coloredlogs.install(level=logging.DEBUG)

logging.getLogger('urllib3.connectionpool').disabled = True
logging.getLogger('charset_normalizer').disabled = True


@click.group()
@click.argument('catalog', type=click.Choice(['macos', 'rosetta']))
@click.pass_context
def cli(ctx: click.Context, catalog: str) -> None:
    """ CLI util for downloading updates from either macos/rosetta seeds """
    ctx.ensure_object(Catalog)
    ctx.obj = MacOsCatalog() if catalog == 'macos' else RosettaCatalog()


@cli.command()
@click.pass_context
def date(ctx: click.Context) -> None:
    """ last update date """
    print(ctx.obj.date)


@cli.command('list')
@click.pass_context
@click.option('--os', is_flag=True)
@click.option('-q', '--quick', is_flag=True, help='don\'t require extended information')
def list(ctx: click.Context, os: bool, quick: bool) -> None:
    """ list all products """
    catalog = ctx.obj
    if os:
        for k in catalog.macos_products:
            print(k)
        return
    for product in catalog.products(detailed=not quick):
        print(product)


@cli.command('download')
@click.pass_context
@click.argument('product_id')
@click.argument('out_dir', type=click.Path(dir_okay=True, exists=False))
def download(ctx: click.Context, product_id: str, out_dir: str) -> None:
    """ download a single product packages """
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True, parents=True)
    ctx.obj.download(product_id, out_dir)


@cli.command('info')
@click.argument('product_id')
@click.pass_context
def info(ctx: click.Context, product_id: str) -> None:
    """ query info for a single product """
    pprint(ctx.obj.get_product(product_id))


if __name__ == '__main__':
    cli()
