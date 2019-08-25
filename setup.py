from distutils.core import setup

setup(
    name='tfl-tree',
    version='0.0.1',
    packages=['tfltree', 'tfltree.raspberrypi'],
    install_requires=[
        'picamera==1.13',
        'pymediainfo==4.0',
        'requests==2.22.0'
    ],
)
