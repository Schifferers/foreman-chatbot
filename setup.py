from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="foreman",
    install_requires=[
        "slackclient",
        "python-dotenv",
        "pyyaml",
        "jsonpath-rw",
        "requests",
        "sentry-sdk",
    ],
    extras_require={},
)
