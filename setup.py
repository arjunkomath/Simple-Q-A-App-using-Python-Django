from setuptools import find_packages, setup

def get_long_description():
    """This function provides the content inside the readme file, keeping it
    up to date with the latest changes and reducing memory load."""
    with open('README.rst') as file:
        return file.read()

def get_requirements():
    """This function keeps the requirements up to date with the most recent
    changes in the files, and reducing the human error chance."""
    with open('requirements.txt') as file:
        return file.read()

setup(
    name='django-qa',
    version='0.10.1.1',
    description='Pluggable django app for Q&A',
    long_description=get_long_description(),
    author='arjunkomath, cdvv7788, sebastian-code, jlariza, swappsco',
    author_email='dev@swapps.co',
    url='https://github.com/swappsco/django-qa',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
    ],
    install_requires=get_requirements(),
    extras_require={
        'i18n': [
            'django-modeltranslation>=0.5b1',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
