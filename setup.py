import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="boilerlib",
    version="0.0.1",
    author="Fredrik Averpil",
    author_email="fredrik@averpil.com",
    description="A boilerplate Py* app that runs inside of Maya, Nuke, python2, or python3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fredrikaverpil/pyvfx-boilerplate",
    packages=setuptools.find_packages(),
    include_package_data=True,
    scripts=[
             'bin/boilerplate',
             ],
    install_requires=[
                      'Qt.py',
                      'PySide2',
                        ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
