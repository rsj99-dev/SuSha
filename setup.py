from setuptools import setup, find_packages

setup(
    name="SuSha",
    version="1.0.0",
    author="rsj99",
    description="A multimodal ensemble learning prediction tool for microbial salinity adaptation based on genome-wide amino acid composition features.",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "susha": ["models/*.pkl"],
    },
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "biopython",
        "shap",
        "openpyxl"
    ],
    entry_points={
        "console_scripts": [
            "SuSha=susha.cli:main",
        ],
    },
)
