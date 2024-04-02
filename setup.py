from setuptools import find_packages, setup

setup(
    name='forecastcmd',
    version='1.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='weather forecast celsius fahrenheit',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests',
        'setuptools'
    ],
    entry_points={
        'console_scripts': [
            'forecast=forecastcmd.__main__:main'
        ]
    },
)