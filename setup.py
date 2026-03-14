from setuptools import setup, find_packages

setup(
    name="psdc-bot",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],  # добавляйте зависимости, если будут
    entry_points={
        "console_scripts": [
            "psdc-bot=psdc_bot.main:main",  # позволяет запускать из командной строки
        ]
    },
    author="Oleksandr Miedviediev",
    description="Bot for assigning shifts from CSV files",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/psdc-bot",  # поменяй на репозиторий
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)