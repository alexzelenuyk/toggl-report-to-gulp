import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="toggl-report",
    version="1.0.6",
    description="Generate PDF report from toggl",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/alexzelenuyk/toggl-report-to-gulp",
    author="Oleksii Zeleniuk",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=("test",)),
    include_package_data=True,
    install_requires=["fpdf", "iso8601", "requests"],
    entry_points={
        "console_scripts": [
            "toggl_report=cli:main",
        ]
    },
)
