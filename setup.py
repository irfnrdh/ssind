from setuptools import setup, find_packages

setup(
    name='ssind',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'pdfkit',
        # Add any other dependencies required by your application
    ],
    entry_points={
        'console_scripts': [
            'ssind = ssind.ssind:main',
        ],
    },
    include_package_data=True,
)
