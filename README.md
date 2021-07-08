[![Python application](https://github.com/doronz88/applecatalog/workflows/Python%20application/badge.svg)](https://github.com/doronz88/applecatalog/actions/workflows/python-app.yml "Python application action")
[![Pypi version](https://img.shields.io/pypi/v/applecatalog.svg)](https://pypi.org/project/applecatalog/ "PyPi package")

# Description

Simple library for automating downloads of updates from Apple's servers. Use this simply tool for downloads macOS
images, CommandLineTools, XProtect database and just everything you can think of :).

# Installation

You can either install using `pip`:

```shell
python3 -m pip install -U --user applecatalog
```

Or install locally from git:

```shell
git clone git@github.com:doronz88/applecatalog.git
cd applecatalog
python3 -m pip install -U --user -e .
```

# Usage

```
Usage: applecatalog [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  date      last update date
  products  products options
```

## Example

```
➜  dev applecatalog products list
Product(id='031-17335', version='11.0.0.0', title='Photo Content Catalogs', date=datetime.datetime(2015, 2, 23, 18, 1, 41), basename='PhotoContentCatalogs.smd')
Product(id='031-17334', version='11.0.0.0', title='Photo Content Themes', date=datetime.datetime(2015, 2, 23, 18, 1, 41), basename='PhotoContentThemes.smd')
Product(id='031-18981', version='17.0.0.0', title='Photo Content Catalogs', date=datetime.datetime(2015, 3, 25, 17, 12, 1), basename='PhotoContentCatalogs.smd')
Product(id='091-76740', version='1.0.0.0', title='Noticeboard Removal Tool', date=datetime.datetime(2018, 4, 5, 17, 17, 49), basename='NRT.smd')
Product(id='041-91737', version='1.0', title='BootCamp', date=datetime.datetime(2019, 10, 9, 19, 40, 56), basename='BootCampESD.smd')
Product(id='041-91736', version='1.0', title='BootCamp', date=datetime.datetime(2019, 10, 9, 19, 43, 9), basename='BootCampESD.smd')
Product(id='041-88235', version='31.0.0.0', title='Photo Content Catalogs', date=datetime.datetime(2019, 10, 9, 21, 33, 35), basename='PhotoContentCatalogs.smd')
Product(id='041-88237', version='31.0.0.0', title='Photo Content Themes', date=datetime.datetime(2019, 10, 9, 21, 34, 21), basename='PhotoContentThemes.smd')
Product(id='041-88232', version='1.8', title='Mac mini EFI Firmware Update', date=datetime.datetime(2019, 10, 9, 21, 35, 34), basename='MacminiEFIUpdate1.8.smd')
Product(id='041-88233', version='3.7.2', title='Remote Desktop Admin Update', date=datetime.datetime(2019, 10, 9, 21, 37, 47), basename='RemoteDesktopAdmin372.smd')
Product(id='041-88177', version='2.0.1', title='Dictation Language Update - Italian (Italy)', date=datetime.datetime(2019, 10, 9, 23, 10, 48), basename='SRCLUpdate_it_IT.smd')
Product(id='041-94866', version='2.0.1', title='Dictation Language Update - English (Australia)', date=datetime.datetime(2019, 10, 9, 23, 11, 3), basename='SRCLUpdate_en_AU.smd')
Product(id='041-88170', version='2.0.3', title='Dictation Language Update - French (France)', date=datetime.datetime(2019, 10, 9, 23, 12, 27), basename='SRCLUpdate_fr_FR.smd')
Product(id='041-88171', version='2.0.1', title='Dictation Language Update - Spanish (United States)', date=datetime.datetime(2019, 10, 9, 23, 12, 28), basename='SRCLUpdate_es_US.smd')
Product(id='041-88172', version='2.0.1', title='Dictation Language Update - Chinese (China)', date=datetime.datetime(2019, 10, 9, 23, 12, 28), basename='SRCLUpdate_zh_CN.smd')
...
```

# Downloading macOS Images

Listing macOS images can be done as follows:

```
➜  apple-catalog git:(master) ✗ applecatalog products macos list
MacOsProduct(product='061-26578', name=None, build='18F2059', version='10.14.5')
MacOsProduct(product='061-26589', name=None, build='18G103', version='10.14.6')
MacOsProduct(product='041-91758', name=None, build='17G66', version='10.13.6')
MacOsProduct(product='041-88800', name=None, build='18E2034', version='10.14.4')
MacOsProduct(product='041-90855', name=None, build='17F66a', version='10.13.5')
MacOsProduct(product='061-86291', name=None, build='19D2064', version='10.15.3')
MacOsProduct(product='001-04366', name=None, build='19E2269', version='10.15.4')
MacOsProduct(product='001-15219', name=None, build='19F2200', version='10.15.5')
MacOsProduct(product='001-36735', name=None, build='19G2006', version='10.15.6')
MacOsProduct(product='001-36801', name=None, build='19G2021', version='10.15.6')
MacOsProduct(product='001-51042', name=None, build='19H2', version='10.15.7')
MacOsProduct(product='001-57224', name=None, build='19H4', version='10.15.7')
MacOsProduct(product='001-68446', name=None, build='19H15', version='10.15.7')
MacOsProduct(product='071-14766', name='macOS Big Sur', build='20D91', version='11.2.3')
MacOsProduct(product='071-29172', name='macOS Big Sur', build='20E232', version='11.3')
MacOsProduct(product='071-32414', name='macOS Big Sur', build='20E241', version='11.3.1')
MacOsProduct(product='071-00696', name='macOS Big Sur', build='20F71', version='11.4')
MacOsProduct(product='071-52235', name='macOS Big Sur Beta', build='20G5042c', version='11.5')
MacOsProduct(product='071-59953', name='macOS Monterey beta', build='21A5268h', version='12.0')
```

For Downloading each one you just download their packages as you would for any other product:

```
➜  apple-catalog git:(master) ✗ applecatalog products download 071-59953 ~/Downloads/macos
2021-07-08 10:48:27 DoronZ.local root[21530] DEBUG downloading: UpdateBrain.zip
100%|██████████████████████████████████████████████████████████████████████████████████████████| 2.75M/2.75M [00:00<00:00, 44.7MiB/s]
2021-07-08 10:48:27 DoronZ.local root[21530] DEBUG downloading: Info.plist
...
```

For creating an installation from these files you can now simply:

```shell
sudo installer -pkg /path/to/InstallAssistant.pkg -target /
```

This should create an `Install macOS XXXXXX.app` application at your `/Applications` folder. If you wish to make a
bootable device from this installation you can use the following official guidelines:

https://support.apple.com/en-us/HT201372

# Downloading latest XProtect files

```
➜  apple-catalog git:(master) applecatalog products xprotect download ./xprotect
2021-07-08 12:05:30 DoronZ.local root[24986] DEBUG downloading: XProtectPlistConfigData_10_15.pkg
100%|█████████████████████████████████████████████████████████████████████████████████████████████| 972k/972k [00:00<00:00, 109MiB/s]
➜  apple-catalog git:(master) ✗ ll xprotect
total 4744
-rw-r--r--  1 z  staff   2.0M Jul  8 12:05 LegacyEntitlementAllowlist.plist
-rw-r--r--  1 z  staff    23K Jul  8 12:05 XProtect.meta.plist
-rw-r--r--  1 z  staff   111K Jul  8 12:05 XProtect.plist
-rw-r--r--  1 z  staff   128K Jul  8 12:05 XProtect.yara
-rw-r--r--  1 z  staff    28K Jul  8 12:05 gk.db
```
