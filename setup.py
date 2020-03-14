import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

name = "pyvfx-boilerplate"
author = "Fredrik Averpil"
author_email = "fredrik@averpil.com"
url = "https://github.com/fredrikaverpil/pyvfx-boilerplate"
description = "A boilerplate Py* app that runs inside of many dcc apps, python2, or python3"
package_dir = "source"
cli_modules = [
    "pyvfx-boilerplate=pyvfx.boilerplate.cli:main",
]

setuptools.setup(
    setup_requires=['setuptools_scm'],
    use_scm_version={
        'local_scheme': 'node-and-timestamp',
    },
    name=name,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    packages=setuptools.find_packages(package_dir),
    package_dir={"": package_dir},
    entry_points={
        'console_scripts': cli_modules,
    },
    include_package_data=True,
    install_requires=[
        'Qt.py',
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
