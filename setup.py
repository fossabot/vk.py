import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vk.py",
    version="0.6.0",
    author="prostomarkeloff",
    description="Extremely-fast Python 3.6+ toolkit for create applications work`s with VKAPI. Has bot framework out of-the-box. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prostomarkeloff/vk.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        'fast': ['ujson', 'uvloop']
    },
    install_requires=[
        "aiohttp",
        "pydantic",
        "watchgod",
    ]
)
