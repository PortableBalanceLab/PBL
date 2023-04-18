import setuptools

setuptools.setup(
    name='pbl',
    version='1.0',
    packages=['pbl'],
    entry_points={
        'console_scripts': [
            'pbl = pbl.__main__:main',
        ],
    },
)