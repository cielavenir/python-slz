import sys
import platform
from os.path import dirname
from os.path import abspath
sys.path.append(dirname(abspath(__file__)))
import monkeypatch_distutils
import subprocess

from setuptools import setup
from setuptools.command.build_ext import build_ext
try:
    from pybind11.setup_helpers import Pybind11Extension
except ImportError:
    from setuptools import Extension as Pybind11Extension

class build_ext_hook(build_ext, object):
    def build_extension(self, ext):
        if platform.system() == 'Windows':
            if sys.maxsize < 1<<32:
                msiz = '-m32'
            else:
                msiz = '-m64'
            subprocess.check_call(['gcc', msiz, '-c', '-DPRECOMPUTE_TABLES=1', '-o', 'slz.o', '-O2', 'src/libslz/src/slz.c'])
            subprocess.check_call(['gcc', msiz, '-c', '-o', 'chkstk.o', 'src/chkstk.S'])
            ext.extra_objects.extend(['slz.o', 'chkstk.o'])
        else:
            ext.sources.append('src/libslz/src/slz.c')
        build_ext.build_extension(self, ext)

ext_modules = [
    Pybind11Extension(
        "slz",
        sources=['src/pyslz.cpp'],
        extra_objects=[],
        extra_compile_args=['-O2'],
        extra_link_args=['-s'],
    ),
]

setup(
    name='slz',
    description='a (light) binding for libslz',
    long_description=open("README.md").read(),
    version='0.0.0.4',
    url='https://github.com/cielavenir/python-slz',
    license='MIT',
    author='cielavenir',
    author_email='cielartisan@gmail.com',
    setup_requires=["pybind11"],
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext_hook},
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
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
