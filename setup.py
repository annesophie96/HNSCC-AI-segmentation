from setuptools import setup, find_packages

setup(
    name='Tumor Detector in qupath',
    version='1.0.0',
    author='Mohammadhamed Mirbagheri',
    author_email='hamed.mirbagheri@fau.de',
    description='This package predicts tumor regions in qupath',
    url='https://github.com/Hamed-kalak/Histo_Unet.git',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum version requirement of the package
)
