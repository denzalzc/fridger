from setuptools import setup, find_packages

setup(
    name="fridger",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "termcolor",
        "sqlalchemy",
        "flask",
        "telebot",
        "pytz"
    ],
    include_package_data=True,
)