import os
import requests
from setuptools import setup


def md_to_rst(from_file, to_file):
    r = requests.post(url='http://c.docverter.com/convert',
                      data={'to': 'rst', 'from': 'markdown'},
                      files={'input_files[]': open(from_file, 'rb')})
    if r.ok:
        with open(to_file, "wb") as f:
            f.write(r.content)


md_to_rst("README.md", "README.rst")

setup(
    name='py_cross_platform',
    version='0.0.1',
    description="Python's cross-platform tool library.",
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       'README.rst')).read(),
    python_requires='>=3.4',
    url='https://github.com/Thoxvi/PyCrossPlatform',
    author='Thoxvi',
    author_email='A@Thoxvi.com',

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    keywords='library tools python cross-platform windows linux mac',

    packages=["py_cross_platform"],
)
