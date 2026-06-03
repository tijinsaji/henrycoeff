from setuptools import setup, find_packages

setup(
    name="henrycoeff",
    version="0.1.0",
    author="Tijin Saji",
    author_email="tijinsaji97@gmail.com",
    description="A Python utility to compute Henry coefficients directly.",
    #long_description="A longer description of your calculation tool.",
    #long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "numpy>=1.20.0",
    ],
    entry_points={
        'console_scripts': [
            'henrycoeff=henrycoeff:main',
        ],
    },
)
