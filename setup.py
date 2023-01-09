"""Install dependencies."""

from setuptools import setup, find_packages

setup(
    name="awesome-kreport-charts",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["pandas==1.1.5",
                      "plotly==5.3.1"],
)