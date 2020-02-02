from setuptools import setup
from distutils.sysconfig import get_python_lib

SITE_PACKAGES_PATH = get_python_lib()

setup(
    name="inlinec",
    version="0.0.1",
    packages=["inlinec", "inlinec.codec"],
    description="Effortlessly write inline C functions",
    author="George Kharchenko",
    author_email="kharchenko.george@gmail.com",
    keywords=["C", "inline", "ffi", "ctypes", "pyxl"],
    download_url="https://github.com/georgek42/inlinec/archive/0.0.1.tar.gz",
    data_files=[(SITE_PACKAGES_PATH, ["inlinec.pth"])],
    install_requires=["parso", "pycparserext", "cffi"],
)

