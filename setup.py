"""Setuptools."""

from setuptools import setup

setup(
    name="exporting_csv",
    author="Denise Postl",
    author_email="postl190070@sr.htlweiz.at",
    description="Tool for importing data of db and export it in csv file.",
    version="1.0.0",
    url="https://github.com",
    python_requires=">=3.8",
    install_requires=[
        "psycopg2" 
    ],
    extras_require={
        "dev": ["pytest", "flake8"],
    },
)
