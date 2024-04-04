from setuptools import find_packages, setup

setup(
    name='forecastcmd',
    version='1.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='weather forecast celsius fahrenheit',
    author='Adam Grim',
    url='https://github.com/adamggrim/forecastcmd',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    package_data={'forecastcmd': ['data/zip_codes_forecast_urls.json']},
    install_requires=[
        'beautifulsoup4',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'forecast=forecastcmd.__main__:main'
        ]
    },
)