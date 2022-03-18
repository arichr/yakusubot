# Yakusu Toshiko
![Main menu](https://i.ibb.co/KbbDzg1/image.png)

Translator based on Google API.
The public instance of this bot is running as [@yakusubot](https://t.me/yakusubot).

## Features
* Show an original text (add a plus to the language name)
* Instant translation with Google.Translate
* No telemetry for Google

## Screenshots
![Language](https://i.ibb.co/ykWb1Xh/image.png)
![Your text](https://i.ibb.co/HtZSDrb/image.png)

## How to use
1. Create a virtual environment _(optional)_
```bash
python3 -m venv venv
source venv/bin/activate
```
2. Install dependecies
```bash
pip install -r requirements.txt
```
3. Create `login.json`
```json
{
    "key": "TG_BOT_TOKEN_HERE"
}
```
4. Run `bot.py`
