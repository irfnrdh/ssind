from setuptools import setup, find_packages

# Read the contents of README file
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='ssind',
    version='0.1.4',
    description='Take Unlimited ScreenShot Automation and make a report',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/irfnrdh/ssind/issues',
    author='Irfannur Diah',
    author_email='irfnrdh@gmail.com',
    license='AGPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='sample setuptools development',
    project_urls={
        'Documentation': 'https://github.com/irfnrdh/ssind/wiki',
        'Source Code': 'https://github.com/irfnrdh/ssind',
        'Issue Tracker': 'https://github.com/irfnrdh/ssind/issues',
    },
    packages=find_packages(),
    install_requires=[
        'Flask',
        'pdfkit',
        'tqdm',
        'click',
        'selenium',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'ssind = ssind.ssind:main',
        ],
    },
    include_package_data=True,
)

