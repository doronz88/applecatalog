import gzip
import os
import plistlib
import logging
from collections import namedtuple

import requests
from tqdm import tqdm

APPLE_SEED_URL = 'https://swscan.apple.com/content/catalogs/others/index-10.16{type}-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog.gz'
MacOsProduct = namedtuple('MacOsProduct', 'product name build version')
Product = namedtuple('Product', 'id version title date basename')


def download_file(url, out_dir):
    local_filename = url.split('/')[-1]
    logging.debug(f'downloading: {local_filename}')
    local_filename = os.path.join(out_dir, local_filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size_in_bytes = int(r.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                progress_bar.update(len(chunk))
                f.write(chunk)

        progress_bar.close()
    return local_filename


class Catalog:
    def __init__(self, type_='seed'):
        self._type = type_
        self._catalog = {}
        self.reload()

    def reload(self):
        self._catalog = plistlib.loads(gzip.decompress(requests.get(APPLE_SEED_URL.format(type=self._type)).content))

    @property
    def date(self):
        return self._catalog.get('IndexDate', None)

    def get_product(self, product_id: str):
        return self._catalog['Products'].get(product_id)

    def get_product_info(self, product_id: str, detailed=True):
        product = self.get_product(product_id)
        date = product.get('PostDate')
        title = None
        version = None
        basename = None
        if 'ServerMetadataURL' in product:
            basename = product['ServerMetadataURL'].split('/')[-1]
            if detailed:
                metadata = plistlib.loads(requests.get(product['ServerMetadataURL']).content)
                version = metadata.get('CFBundleShortVersionString')
                localization = metadata['localization']
                english = localization.get('English')
                if english is None:
                    english = localization.get('en')
                title = english['title']
        return Product(id=product_id, version=version, title=title, date=date, basename=basename)

    def products(self, detailed=True):
        for product_id, product in self._catalog['Products'].items():
            yield self.get_product_info(product_id, detailed=detailed)

    @property
    def macos_products(self):
        for product_id, product in self._catalog['Products'].items():
            extended_meta_info = product.get('ExtendedMetaInfo')
            if extended_meta_info is None:
                continue

            if 'InstallAssistantPackageIdentifiers' not in extended_meta_info:
                continue

            metadata = requests.get(product['Distributions']['English']).text
            if 'auxinfo' not in metadata:
                continue

            name = metadata.split('<title>')[1].split('<')[0]

            if name == 'SU_TITLE':
                name = None

            auxinfo = metadata.split('<auxinfo>')[1].split('</auxinfo>')[0].encode()
            auxinfo = plistlib.loads(b'<plist version="1.0">' + auxinfo + b'</plist>')

            yield MacOsProduct(product=product_id, name=name, build=auxinfo.get('BUILD'),
                               version=auxinfo.get('VERSION'))

    def download(self, product_id: str, out_dir: str):
        results = []
        product = self._catalog['Products'][product_id]
        for package in product['Packages']:
            results.append(download_file(package['URL'], out_dir))
        return results
