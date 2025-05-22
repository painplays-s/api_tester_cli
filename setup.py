from setuptools import setup, find_packages

setup(
    name='api-tester-cli',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'api-tester=main:main',  # Adjust this if your main function is located elsewhere
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A command line interface for testing APIs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/api-tester-cli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)