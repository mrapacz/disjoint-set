import setuptools

import disjoint_set

setuptools.setup(
    name="disjoint_set",
    version=disjoint_set.__version__,
    packages=setuptools.find_packages(),
    package_data={"disjoint_set": ["py.typed"]},
    description="Disjoint set data structure implementation for Python",
    url="https://github.com/mrapacz/disjoint_set",
    license_files=("LICENSE",),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    maintainer="Maciej Rapacz",
    maintainer_email="python.disjointset@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
