import datetime
import gzip
import logging
import plistlib
from collections import namedtuple
from pathlib import Path
from typing import Generator, List, Mapping

import requests
from parameter_decorators import str_to_path
from tqdm import tqdm

APPLE_SEED_URL = 'https://swscan.apple.com/content/catalogs/others/index-13-12-10.16-10.15-10.14-10.13-10.12-10.11-' \
                 '10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog.gz'
MacOsProductInfo = namedtuple('MacOsProduct', 'product name build version')
ProductInfo = namedtuple('ProductInfo', 'id version title date basename')


def download_file(url: str, out_dir: Path) -> Path:
    local_filename = url.split('/')[-1]
    logging.debug(f'downloading: {local_filename}')
    local_filename = out_dir / local_filename
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size_in_bytes = int(r.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, dynamic_ncols=True)

        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                progress_bar.update(len(chunk))
                f.write(chunk)

        progress_bar.close()
    return local_filename


class Catalog:
    def __init__(self):
        self._catalog = {}
        self.reload()

    def reload(self) -> None:
        self._catalog = plistlib.loads(gzip.decompress(requests.get(APPLE_SEED_URL, verify=False).content))

    @property
    def date(self) -> datetime.datetime:
        return self._catalog.get('IndexDate', None)

    def get_product(self, product_id: str) -> Mapping:
        return self._catalog['Products'].get(product_id)

    def get_product_info(self, product_id: str, detailed=True) -> ProductInfo:
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
        return ProductInfo(id=product_id, version=version, title=title, date=date, basename=basename)

    def products(self, detailed=True) -> Generator[ProductInfo, None, None]:
        for product_id, product in self._catalog['Products'].items():
            yield self.get_product_info(product_id, detailed=detailed)

    @property
    def macos_products(self) -> Generator[MacOsProductInfo, None, None]:
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

            yield MacOsProductInfo(product=product_id, name=name, build=auxinfo.get('BUILD'),
                                   version=auxinfo.get('VERSION'))

    @str_to_path('out_dir')
    def download(self, product_id: str, out_dir: Path) -> List[Path]:
        results = []
        product = self._catalog['Products'][product_id]
        for package in product['Packages']:
            results.append(download_file(package['URL'], out_dir))
        return results
