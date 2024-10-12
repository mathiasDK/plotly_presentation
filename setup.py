import codecs
import os
import re
from codecs import open
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

with open("README.md") as readme_file:
    readme = readme_file.read()


# requirements
def package_is_pinned(name):
    """quick check to make sure packages are pinned"""
    for pin in [">", "<", "=="]:
        if pin in name:
            return True
    return False


with open(os.path.join(HERE, "requirements.txt"), encoding="utf-8") as f:
    requirements = []
    for line in f.readlines():
        line = line.strip()
        if line and line[0] != "#":
            requirements.append(line)
    if not all(map(package_is_pinned, requirements)):
        raise RuntimeError("All Packages in requirements.txt must be pinned")

setup_requirements = [
    "plotly>=5.24.0",
    "pandas>=2.2",
    "numpy>=2.1",
    "pyyaml>=6.0.2",
    "black==24.*",
    "pytest==8.*",
]

test_requirements = [
    "plotly>=5.24.0",
    "pandas>=2.2",
    "numpy>=2.1",
    "pyyaml>=6.0.2",
    "black==24.*",
    "pytest==8.*",
]

PACKAGE_NAME = "plotly_presentation"


def read(*filenames, **kwargs):
    """
    Build an absolute path from ``*filenames``, and  return contents of
    resulting file.  Defaults to UTF-8 encoding.
    """
    encoding = kwargs.get("encoding", "utf-8")
    sep = kwargs.get("sep", "\n")
    buf = []
    for fl in filenames:
        with codecs.open(os.path.join(HERE, fl), "rb", encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


META_FILE = read(os.path.join(PACKAGE_NAME, "__init__.py"))


def find_meta(meta):
    """Extract __*meta*__ from META_FILE."""
    re_str = r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta)
    meta_match = re.search(re_str, META_FILE, re.M)
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


setup(
    name=PACKAGE_NAME,
    version=find_meta("version"),
    description="Python library to make it easier to plot using plotly",
    long_description=readme,
    author=find_meta("author"),
    author_email=find_meta("email"),
    url="https://github.dev/mathiasDK/plotly_presentation",
    packages=find_packages(include=["plotly_presentation"]),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords="plotly_presentation",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
    ],
    test_suite="tests",
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    python_requires=">=3.8,<4",
    license="MIT",
)
