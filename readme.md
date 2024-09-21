# Genshin Notifications
[![Last Commit](https://img.shields.io/github/last-commit/nitolar/genshin-notifications)](https://github.com/nitolar/genshin-notifications/commits/master)
[![Repo size](https://img.shields.io/github/repo-size/nitolar/genshin-notifications)](https://github.com/nitolar/genshin-notifications/graphs/code-frequency)
[![LICENSE](https://img.shields.io/github/license/nitolar/genshin-notifications)](https://github.com/nitolar/genshin-notifications/blob/master/LICENSE.md)


Brings resin, realm currency, parametric transformer and expedition notifications to your windows PC!

Also automatically collects your daily check-in!

[Check out Honkia: Star Rail version](https://github.com/nitolar/hsr-notifications)

## Preview

[gsnotification.webm](https://github.com/nitolar/genshin-notifications/assets/73779998/d8526fd8-5bf9-4940-87a3-67675ddaa13c)

## How to use

Install [python](https://www.python.org)

Clone the project or download it

```bash
git clone https://github.com/nitolar/genshin-notifications
```

Go to the project directory

```bash
cd genshin-notifications
```

Install requirements.txt

```bash
pip install -r requirements.txt
```

Configure the settings.env file

Run file

```bash
python notifications.py
```


## Changelog

### 22.09.2024

- Fixed Shop reminder not working

### 21.09.2024

**After this update you must reinstall requirements.txt! Or install genshin.py using: pip install git+https://github.com/thesadru/genshin.py**
- Rewrite an entire project to use `genshin.py` instead of `genshinstats`
- Added Imaginarium Theater reset notification
- Added 160 resin to `resin_milestones`
- Fixed Spiral Abyss reset notification being sent even though it wasn't reset
- Spiral Abyss and Shop reset notifications now have a separate function

### 02.06.2024

**After this update you must reinstall requirements.txt! Or install psutil using: pip install psutil**
- Added Shop and Abyss reset notification
- Added reminders when you turn on genshin
- Added errors when incorrect values are set for `set_cookies_method` (not set to `auto` or `login`), `ltuid` (set to deafult 0), `ltoken` (empty), `server` (not set to one of those `eu`, `us`, `as`)

### 20.05.2023

- Fixed spelling
- Fixed a DataNotPublic error sometimes showing up if you used to play other games made by Hoyoverse on the same account
- Changed full resin notification length from 10 seconds to 60 (as it should be)

### 12.05.2023

- Fixed video not loading in preview section in readme.md

### 28.03.2023

**After this update you must reinstall requirements.txt! Or install pytz using: pip install pytz**
- Changed some spelling
- Added auto daily check-in
- Fixed full resin and full realm currency notification not being send when milestones were turnd on
- Added time when notification was sent in console
- Added changelog to readme.md

### 22.02.2023

- Fixed resin and realm currency notification being send more than 1 time if it's full

### 21.02.2023

- First release


## Thanks to

[thesadru](https://github.com/thesadru) for creating [genshin.py](https://github.com/thesadru/genshin.py).


## Feedback

Like what you see? Give a star if you don't mind.

Found any bugs? Report them here: https://github.com/nitolar/genshin-notifications/issues


## Authors

- [@nitolar](https://www.github.com/nitolar)

