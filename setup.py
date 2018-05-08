import os

import setuptools

REQUIRES = [
    'pyshark'
]

_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_ROOT, 'README.md')) as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="pcap-processor",
    version="0.0.1",
    description="Read and process pcap files using this nifty tool.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Gobinath Loganathan",
    author_email="slgobinath@gmail.com",
    url="https://github.com/slgobinath/pcap-processor",
    download_url="https://github.com/slgobinath/pcap-processor/releases",
    packages=setuptools.find_packages(),
    install_requires=REQUIRES,
    setup_requires=['setuptools>=38.6.0'],
    entry_points={'console_scripts': ['pcap-processor = pcap_processor.__main__:main']},
    keywords='pcap utility csv json',
    classifiers=[
                    "Operating System :: POSIX :: Linux",
                    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                    "Development Status :: 5 - Production/Stable",
                    "Intended Audience :: End Users/Desktop",
                    "Topic :: Utilities"] + [('Programming Language :: Python :: %s' % x) for x in
                                             '3 3.4 3.5 3.6'.split()]
)
