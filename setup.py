from distutils.core import setup

setup(
    name='tfl-tree',
    version='0.0.1',
    packages=['tfltree', 'tfltree.raspberrypi'],
    install_requires=[
        'gpiozero==1.5.0',
        'pymediainfo==4.0',
        'python-dotenv==0.10.3',
        'requests==2.22.0',
        'python-twitter @ https://github.com/danielthepope/python-twitter/archive/feature/subtitles.zip',
    ],
    extras_require={
        # The following dependencies fail to install if you're not running on a Raspberry Pi.
        # It is useful to have this optional if, for example, you're writing your code on another computer.
        'pi': [
            'RPi.GPIO==0.6.5',
            'picamera==1.13',
        ]
    }
)
