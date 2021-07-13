import logging
import os
import shutil
import tempfile
from pprint import pprint

import click
import coloredlogs
from applecatalog.catalog import Catalog

coloredlogs.install(level=logging.DEBUG)

logging.getLogger('urllib3.connectionpool').disabled = True


def extract_package(filename, out_dir):
    assert 0 == os.system(f'pkgutil --expand "{filename}" "{out_dir}"')
    payload = os.path.join(out_dir, 'Payload')
    assert 0 == os.system(f'tar xf "{payload}" -C "{out_dir}"')


def get_unique_product(catalog: Catalog, match):
    products = []
    for product in catalog.products(detailed=False):
        if product.basename and match in product.basename:
            products.append(product)
    assert len(products) == 1
    return products[0]


def get_xprotect_product(catalog: Catalog):
    return get_unique_product(catalog, 'XProtect')


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


@products.command('info', cls=Command)
@click.argument('product_id')
def products_info(catalog, product_id):
    """ query info for a single product """
    pprint(catalog.get_product(product_id))


@products.group()
def macos():
    """ macos products options """
    pass


@macos.command('list', cls=Command)
def macos_list(catalog):
    """ list all macos products """
    for k in catalog.macos_products:
        print(k)


@products.group()
def xprotect():
    """ xprotect products options """
    pass


@xprotect.command('date', cls=Command)
def xprotect_date(catalog):
    """ XProtect update date """
    product = get_xprotect_product(catalog)
    print(product.date)


@xprotect.command('download', cls=Command)
@click.argument('out_path', type=click.Path(dir_okay=True, file_okay=False, exists=False))
def xprotect_download(catalog, out_path):
    """ download latest xprotect rules """
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    product = get_xprotect_product(catalog)

    with tempfile.TemporaryDirectory() as download_temp_dir:
        # download XProtect package
        results = catalog.download(product.id, download_temp_dir)

        # verify exactly one was found
        assert len(results) == 1, 'expected exactly one result'

        # extract the XProtect package
        package_temp_dir = os.path.join(download_temp_dir, 'package')
        extract_package(results[0], package_temp_dir)
        resource_dir = os.path.join(package_temp_dir,
                                    'Library/Apple/System/Library/CoreServices/XProtect.bundle/Contents/Resources')

        for filename in os.listdir(resource_dir):
            # copy to target directory
            logging.debug(f'copying {filename} from extracted package...')
            filename = os.path.join(resource_dir, filename)
            shutil.copyfile(filename, os.path.join(out_path, os.path.basename(filename)))


if __name__ == '__main__':
    cli()
