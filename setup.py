import sys
from os.path import dirname
from os.path import abspath
sys.path.append(dirname(abspath(__file__)))
import monkeypatch_distutils

from setuptools import setup
try:
	from pybind11.setup_helpers import Pybind11Extension
except ImportError:
	from setuptools import Extension as Pybind11Extension

ext_modules = [
    Pybind11Extension(
        "slz",
        ['src/pyslz.cpp', 'src/slz.c'],  # Sort source files for reproducibility
    ),
]

setup(
    name='slz',
    description='slz',
    long_description=open("README.md").read(),
    version='0.0.0.1',
    url='https://github.com/cielavenir/python-slz',
    license='PSF',
    author='cielavenir',
    author_email='cielartisan@gmail.com',
    setup_requires=["pybind11"],
    ext_modules=ext_modules,
    #cmdclass={"build_ext": build_ext},
    zip_safe=False,
    include_package_data=True,
    # platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: Implementation :: PyPy',
    ]
)