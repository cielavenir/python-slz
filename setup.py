import sys
import platform
from os.path import dirname
from os.path import abspath
sys.path.append(dirname(abspath(__file__)))
import monkeypatch_distutils
import subprocess

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
try:
    from pybind11.setup_helpers import Pybind11Extension
except ImportError:
    from setuptools import Extension as Pybind11Extension

class build_ext_hook(build_ext, object):
    def build_extension(self, ext):
        if platform.system() == 'Windows':
            if sys.maxsize < 1<<32:
                gcc = 'i686-w64-mingw32-gcc'
                gxx = 'i686-w64-mingw32-g++'
            else:
                gcc = 'x86_64-w64-mingw32-gcc'
                gxx = 'x86_64-w64-mingw32-g++'
            subprocess.check_call([gcc, '-c', '-DPRECOMPUTE_TABLES=1', '-o', 'slz.o', '-O2', 'src/libslz/src/slz.c'])
            subprocess.check_call([gcc, '-c', '-o', 'chkstk.o', 'src/chkstk.S'])
            if sys.version_info < (3,5):
                import sysconfig
                import pybind11
                subprocess.check_call([gxx, '-c', '-o', 'pyslz.o', '-O2',
                    '-I', sysconfig.get_paths()['include'],
                    '-I', sysconfig.get_paths()['platinclude'],
                    '-I', pybind11.get_include(),
                    'src/pyslz.cpp'])
                # ext.extra_objects.append('pyslz.o')
                subprocess.check_call(['mkdir', '-p', 'build\lib.win32-2.7'])
                subprocess.check_call(['ls', sysconfig.get_paths()['stdlib']])
                subprocess.check_call([gxx, '-shared', '-o', 'build\lib.win32-2.7\slz.pyd',
                    'pyslz.o', 'slz.o', 'chkstk.o',
                    '-L', sysconfig.get_paths()['stdlib'],
                    '-lpython27'
                ])
                return
            else:
                ext.sources.append('src/pyslz.cpp')
            ext.extra_objects.extend(['slz.o', 'chkstk.o'])
        else:
            ext.sources.extend(['src/pyslz.cpp', 'src/libslz/src/slz.c'])
        build_ext.build_extension(self, ext)

kwargs = {
    'name': 'slz',
    'sources': [],
    'extra_objects': [],
    'extra_compile_args': ['-O2'],
    'extra_link_args': ['-s'],
}
klass = Extension if platform.system() == 'Windows' and sys.version_info < (3,5) else Pybind11Extension
ext_modules = [klass(**kwargs)]

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
