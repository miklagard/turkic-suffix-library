import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="turkic-suffix-library",
    version="0.1.4",
    author="Cem Yildiz, Oguzhan Moroglu, Sadullah Duman",
    author_email="cem.yildiz@proton.me",
    description="Turkic suffix library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miklagard/turkic-suffix-library",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
