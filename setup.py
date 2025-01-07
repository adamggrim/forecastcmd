from setuptools import find_packages, setup

setup(
    name='forecast-command',
    version='1.0',
    description='Package for retrieving weather forecasts from NOAA',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='weather, forecast, celsius, fahrenheit',
    url='https://github.com/adamggrim/forecast-command',
    author='Adam Grim',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    package_data={'forecast_command': ['data/zip_codes_forecast_urls.json']},
    install_requires=[
        'beautifulsoup4',
        'requests',
        'setuptools'
    ],
    entry_points={
        'console_scripts': [
            'forecast=forecast_command.__main__:main'
        ]
    },
)
