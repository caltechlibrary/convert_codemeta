import io
import os
import glob
import sys, json
from shutil import rmtree

from setuptools import find_packages, setup, Command


def read(fname):
    with open(fname, mode="r", encoding="utf-8") as f:
        src = f.read()
    return src


def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join(".", "requirements.txt")
    with open(reqs_path, "r") as f:
        requirements = [line.rstrip() for line in f]
    return requirements


codemeta_json = "codemeta.json"

# Let's pickup as much metadata as we need from codemeta.json
with open(codemeta_json, mode="r", encoding="utf-8") as f:
    src = f.read()
    meta = json.loads(src)

# Let's make our symvar string
version = meta["version"]

# Now we need to pull and format our author, author_email strings.
author = ""
author_email = ""
for obj in meta["author"]:
    given = obj["givenName"]
    family = obj["familyName"]
    email = obj["email"]
    if len(author) == 0:
        author = given + " " + family
    else:
        author = author + ", " + given + " " + family
    if len(author_email) == 0:
        author_email = email
    else:
        author_email = author_email + ", " + email
description = meta["description"]
url = meta["codeRepository"]
download = meta["downloadUrl"]
license = meta["license"]
name = meta["name"]

here = os.path.abspath(os.path.dirname(__file__))


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel distribution…")
        os.system("{0} setup.py sdist bdist_wheel ".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        sys.exit()


tests_require = [
    'pytest>=6.1.1',
]

extras_require = {
    'all': tests_require,
    'tests': tests_require,
}

setup(
    name=name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    download_url=download,
    license=license,
    packages=find_packages(),
    package_data={"convert_codemeta": ["crosswalk.csv", "codemeta_schema.jsonld"]},
    py_modules=["convert_codemeta"],
    install_requires=read_requirements(),
    tests_require=tests_require,
    extras_require=extras_require,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
    ],
    # $ setup.py publish support.
    cmdclass={"upload": UploadCommand},
)
