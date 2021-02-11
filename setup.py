# coding=utf-8

from distutils.core import setup, Extension
import sys
import os
import platform

ARCH='64'
SQLPARSER_DIR = './general_sql_parser/'

if sys.maxsize > 2**32:
    ARCH = '64'
else:
    ARCH = '32'


def download_library():
    if platform.python_version_tuple()[0] == '2':
        from urllib import urlretrieve
    else:
        from urllib.request import urlretrieve

    file_name = "gsp_c_lib.tar.gz"

    url = "http://www.sqlparser.com/dl/gsqlparser_c_linux32_trial_1_0_1.tar.gz"
    if os.name == "nt":
        if ARCH == '32':
            url = "http://www.sqlparser.com/dl/gsqlparser_c_win32_trial_1_1_0.zip"
        else:
            url = "http://www.sqlparser.com/dl/gsqlparser_c_win64_trial_1_1_0.zip"
        file_name = "gsp_c_lib.zip"
    else:
        if ARCH == '64':
            url = "http://www.sqlparser.com/dl/gsqlparser_c_linux64_trial_1_1_0.tar.gz"

    print("Downloading library from '%s'..." % url)

    urlretrieve(url, file_name)

    print("Done!")
    print("Extracting archive...")

    if os.name == "nt":
        import zipfile

        archive = zipfile.ZipFile(file_name, 'r')
        archive.extractall(SQLPARSER_DIR)
    else:
        import tarfile

        archive = tarfile.open(file_name)
        archive.extractall(SQLPARSER_DIR)

    print("Done!")


if __name__ == '__main__':
    if not os.path.isdir(SQLPARSER_DIR):
        print("Could not find the general sql parser library in %s" % SQLPARSER_DIR)
        download_library()

    # check again (the user might have downloaded the library)
    if os.path.isdir(SQLPARSER_DIR):
        parsebridge = Extension(
            'sqlparser',
            sources=[
                'Parser.c', 'Statement.c', 'Node.c', 'ENodeType.c', 'parsebridgemodule.c',
                SQLPARSER_DIR + 'ext/node_visitor/node_visitor.c',
                SQLPARSER_DIR + 'ext/expr_traverse/expr_traverse.c',
                SQLPARSER_DIR + 'ext/modifysql/modifysql.c'
            ],
            include_dirs=[
                SQLPARSER_DIR + 'core/',
                SQLPARSER_DIR + 'ext/collection/includes/',
                SQLPARSER_DIR + 'ext/expr_traverse/',
                SQLPARSER_DIR + 'ext/modifysql/',
                SQLPARSER_DIR + 'ext/node_visitor/'
            ],
            library_dirs=[SQLPARSER_DIR + '/lib/'],
            libraries=['gspcollection', 'gspcore'],
            define_macros=[('_CRT_SECURE_NO_WARNINGS', None), ('DONT_FIX_FRAGMENTS', None), ],
            extra_compile_args=['-Wno-strict-prototypes']
        )

        if sys.platform == 'win32' or sys.platform == 'win64':
            parsebridge.extra_link_args = ['/MANIFEST', '/DEBUG']
            parsebridge.extra_compile_args = ['/Zi']

        with open("README.md", "r", encoding="utf-8") as fh:
            long_description = fh.read()

        setup(name='python-sqlparser',
              version='1.1',
              description='A package for parsing SQL queries',
              long_description=long_description,
              long_description_content_type='text/markdown',
              author='Timo Djürken',
              url='https://github.com/546133753/python-sqlparser',
              license='GPL',
              ext_modules=[parsebridge])
