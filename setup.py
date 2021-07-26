from setuptools import setup, find_packages
from pathlib import Path

from chaintools import __version__

with Path('requirements.txt').open(encoding='utf-8') as f:
    install_requires = [
        line.strip() for line in f.readlines()
        if not line.startswith('#') and not line.startswith('--')
    ]

with Path('README.md').open(encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='chaintools',
    version=__version__,
    description='Replace nested function calls with chaining expression',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jiun Bae',
    author_email='jiunbae.dev@gmail.com',
    url='https://github.com/MaybeS/chaintools',
    download_url='https://github.com/MaybeS/chaintools/releases/latest',
    license='MIT',
    keywords=['chaintools', 'functional'],
    python_requires='>= 3.6',
    install_requires=install_requires,
    extra_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'pytest-pep8',
            'pytest-mock',
        ]
    },
    scripts=[],
    packages=find_packages(exclude=['docs', 'tests*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
