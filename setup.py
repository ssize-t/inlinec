from setuptools import setup
from distutils.sysconfig import get_python_lib

SITE_PACKAGES_PATH = get_python_lib()

setup(
    name="inlinec",
    version="0.0.1",
    packages=["inlinec", "inlinec.codec"],
    data_files=[(SITE_PACKAGES_PATH, ["inlinec.pth"])],
    install_requires=["parso", "pycparserext", "cffi"],
)

