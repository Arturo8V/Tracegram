from setuptools import setup, find_packages

setup(
    name="tracegram",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["checker"],
    install_requires=[
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "tracegram = checker:main"
        ]
    },
    author="YourName",
    description="OSINT tool to trace Instagram follower intersections",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
)
