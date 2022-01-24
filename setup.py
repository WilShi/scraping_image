"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['run.py']
DATA_FILES = ['image.py', 'Ui_appView.py']
OPTIONS = {'includes' : ['requests', 'sys', 'PyQt5', 'pathlib', 'qdarkstyle', 'selenium', 'webdriver_manager', 'time', 'zipfile', 'base64', 're']}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
