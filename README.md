# FishAudio API TTS Gen Component by w-AI-fu_DEV

## What is this for?
Fishaudio API module for the jaison project

## Setup

Windows
```
conda create -n jaison-comp-ttsg-fishaudio-api python=3.12
conda activate jaison-comp-ttsg-fishaudio-api
pip install -r requirements.txt
```

Unix
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Furthermore, create a `.env` file in the root of this project with the following:
```
FISH_API_KEY=<fishaudio api key>
```

## Testing
Assuming you are in the right virtual environment and are in the root directory:
```
python ./src/main.py --port=5000
```
If it runs, it should be fine.

## Configuration
In `config.json`, you can set your desired voice id. Also set `env` to the filepath to your `.env` file.

## Related stuff
Project J.A.I.son: https://github.com/limitcantcode/jaison-core

Join the community Discord: https://discord.gg/Z8yyEzHsYM
