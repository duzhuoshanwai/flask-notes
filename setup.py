from setuptools import setup, find_packages

setup(
    name="flask-note",
    version="2025.06.12",
    packages=find_packages(),
    install_requires=[
        "Flask==3.1.1",
        "python-dotenv==1.1.0",
        "Authlib==1.6.0",
        "Flask-WTF==1.2.2",
        "PyJWT==2.10.1",
        "requests==2.32.4",
        "MarkupSafe==3.0.2",
        "mistune==3.1.3",
        "bleach==6.2.0",
    ],
)