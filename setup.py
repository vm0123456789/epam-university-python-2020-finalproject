from setuptools import find_packages, setup

setup(
    name='departments_app',
    version='0.1',
    author='Viktor Mishyn',
    author_email='viktormishyn@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    # zip_safe=False,
    # install_requires=[
    #     'flask',
    # ],
)

# to create distribution package: `python setup.py sdist`
