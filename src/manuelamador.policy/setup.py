# -*- coding: utf-8 -*-
"""Installer for the manuelamador.policy package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='manuelamador.policy',
    version='1.0a1',
    description="manuelamador.com policy package",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0.0a1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.1",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone CMS',
    author='Manuel Amador (Rudd-O)',
    author_email='rudd-o+plone@rudd-o.com',
    url='https://github.com/collective/manuelamador.policy',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/manuelamador.policy',
        'Source': 'https://github.com/collective/manuelamador.policy',
        'Tracker': 'https://github.com/collective/manuelamador.policy/issues',
        # 'Documentation': 'https://manuelamador.policy.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['manuelamador'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.1",
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'z3c.jbot',
        'Products.GenericSetup>=1.8.2',
        'plone.api>=1.8.4',
        'plone.restapi',
        'plone.app.dexterity',
        'plone.app.relationfield',
        'plone.app.lockingbehavior',
        'plone.schema',
        'collective.relationhelpers',
        'collective.folderishtypes[dexterity]',
        'collective.searchandreplace',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = manuelamador.policy.locales.update:update_locale
    """,
)
