# tfl-tree

## Requirements
On your Raspberry Pi, you need to install some dependencies:
- `espeak` for speech synthesis
- `mediainfo` for getting information about generated speech

```bash
sudo apt install espeak mediainfo
```

`ffmpeg` should already be installed. This is required to package the video with the generated audio

You should install Python requirements in a virtual environment. This is designed to run on Python 3, so you can initialise your virtual environment using Python's built-in `venv` module, then activate the environment and install dependencies like so:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -e ".[pi]"
```

If you want to install dependencies on another computer (e.g. if you're editing the code and your IDE is trying to help you with code completion), install the dependencies from `requirements.txt` instead of that last `pip install` line above:

```bash
pip install -r requirements.txt
```
