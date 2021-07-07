import logging
import os

import click
import coloredlogs

from applecatalog.catalog import Catalog

coloredlogs.install(level=logging.DEBUG)

logging.getLogger('urllib3.connectionpool').disabled = True


class Command(click.Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params[:0] = [
            click.Option(('catalog', '--type'), type=click.Choice(['seed', 'beta', 'costumerseed']), default='seed',
                         callback=self.catalog),
        ]

    @staticmethod
    def catalog(ctx, param, value):
        if '_APPCAT_COMPLETE' in os.environ:
            # prevent connection establishment when in autocomplete mode
            return
        return Catalog(value)


@click.group()
def cli():
    pass


@cli.command(cls=Command)
def date(catalog):
    """ last update date """
    print(catalog.date)


@cli.group()
def products():
    """ products options """
    pass


@products.command('list', cls=Command)
@click.option('-q', '--quick', is_flag=True, help='don\'t require extended information')
def products_list(catalog, quick):
    """ list all products """
    for product in catalog.products(detailed=not quick):
        print(product)


@products.command('download', cls=Command)
@click.argument('product_id')
@click.argument('out_dir', type=click.Path(dir_okay=True, exists=False))
def products_download(catalog, product_id, out_dir):
    """ download a single product packages """
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    catalog.download(product_id, out_dir)


@products.group()
def macos():
    """ macos products options """
    pass


@macos.command('list', cls=Command)
def macos_list(catalog):
    """ list all macos products """
    for k in catalog.macos_products:
        print(k)


if __name__ == '__main__':
    cli()
