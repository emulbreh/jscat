from setuptools import setup, find_packages

setup(
    name='jscat',
    version='0.1',
    description='cat for javascript files',
    author='Johannes Dollinger',
    author_email='emulbreh@googlemail.com',
    url='https://github.com/emulbreh/jscat',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'jscat = jscat:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
    ]
)