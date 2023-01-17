"""Install dependencies."""

from setuptools import setup, find_packages

setup(
    name="awesome-kreport-charts",
    author="Tania Girao Mangolini",
    author_email="tania.mangolini@gmail.com",
    description="Create awesome charts for kreports (kraken-style reports)",
    long_description="Create awesome charts for kreports (kraken-style reports)",
    url="https://github.com/taniagmangolini/awesome_kreport_charts",
    version="1.1.2",
    keywords=['kraken', 'kreport', 'ccmetagen', 'kraken-style reports'],
    packages=find_packages(),
    install_requires=["pandas==1.1.5",
                      "plotly==5.3.1"],
)