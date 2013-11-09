import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="admin_bootstrap3",
    version="0.1.13",
    author="Jonas Hagstedt",
    author_email="hagstedt@gmail.com",
    description=("Bootstrap3 admin"),
    license="BSD",
    keywords="bootstrap3 django admin",
    url = "https://github.com/jonashagstedt/bootstrap3-django-admin",
    packages=['admin_bootstrap3', ],
    long_description=read('README.md'),
    install_requires=[
        "Django >= 1.4",
        "django-compressor",
    ],
    classifiers=[
        "Development Status :: Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
