import setuptools

setuptools.setup(
    name='disjoint_set',
    version='0.5.0',
    packages=setuptools.find_packages(),
    description='Disjoint set data structure implementation for Python',
    url='https://github.com/mrapacz/disjoint_set',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    maintainer="Maciej Rapacz",
    maintainer_email="python.disjointset@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
