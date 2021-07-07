# Description

Simple library for automating downloads of updates from Apple's servers. Use this simply tool for downloads macOS
images, CommandLineTools, XProtect database and just everything you can think of :).

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

