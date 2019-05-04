import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvfx.boilerplate",
    version="3.2.0",
    # author="Fredrik Averpil",
    # author_email="fredrik@averpil.com",
    author="Zachary Cole",
    author_email="zcole@nzaneproductions.com",
    description="A boilerplate Py* app that runs inside of Maya, Nuke, python2, or python3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/fredrikaverpil/pyvfx-boilerplate",
    url="https://github.com/nzanepro/pyvfx.boilerplate",
    packages=setuptools.find_packages(),
    scripts=[
        'bin/pyvfx.boilerplateUI.sh',
    ],
    package_data={
        "pyvfx.boilerplate": ["resources/*.ui", "resources/*.json"],
    },
    install_requires=[
        'Qt.py',
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
