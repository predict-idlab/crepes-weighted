import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crepes_weighted",
    version="0.1.1",
    author="Jef Jonkers",
    author_email="jef.jonkers@ugent.be",
    description="Weighted version of crepes: Conformal classifiers, regressors, and predictive systems (crepes)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/predict-idlab/crepes-weighted",
    # project_urls={
    #     "Bug Tracker": "https://github.com//henrikbostrom/crepes/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["numpy", "pandas"],
    python_requires=">=3.8",
)
