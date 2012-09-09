from distutils.core import setup

setup (
    name='pyipay',
    version='0.1.1',
    author='Chee-Hyung Yoon',
    author_email='yoon@tikkon.com',
    packages=['pyipay',],
    url='http://pypi.python.org/pypi/pyipay/',
    license='LICENSE.txt',
    description='A Python library for accessing the Auction iPay API',
    long_description=open('README.md').read(),
    install_requires=[
        "suds >= 0.4",
    ],
)
