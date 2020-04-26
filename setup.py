from setuptools import find_packages, setup


def get_version():
    with open('mkpatcher/__meta__.py', 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.strip().split('=')[1].strip(' \'"')


def get_long_description():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='mkpatcher',
    version=get_version(),
    description='Python-Markdown extension allowing arbitrary scripts to modify MkDocs input files',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    keywords=['markdown', 'extensions', 'mkdocs', 'plugins'],
    url='https://github.com/ofek/mkpatcher',
    project_urls={
        'Documentation': 'https://github.com/ofek/mkpatcher#readme',
        'Source Code': 'https://github.com/ofek/mkpatcher',
        'Bug Tracker': 'https://github.com/ofek/mkpatcher/issues',
    },
    author='Ofek Lev',
    author_email='ofekmeister@gmail.com',
    license='Apache-2.0 OR MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    packages=find_packages(include=['mkpatcher', 'mkpatcher.*']),
    python_requires='>=3.6',
    install_requires=['Markdown>=3.2.1'],
)
