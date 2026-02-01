from setuptools import setup, find_packages

setup(
    name="fridger",
    version="0.1",
    package_dir={"": "src"},  # Указываем, что пакеты в src
    packages=find_packages(where="src"),  # Ищем пакеты в src
    install_requires=[
        "termcolor",
        "sqlalchemy",
        "flask",
        "telebot"
    ],
    include_package_data=True,
)