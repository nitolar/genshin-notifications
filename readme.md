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

[thesadru](https://github.com/thesadru) for creating original [genshinstats](https://github.com/thesadru/genshinstats). [(My fork of genshinstats that is used in this project)](https://github.com/nitolar/genshinstats)


## Feedback

Like what you see? Give a star if you don't mind.

Found any bugs? Report them here: https://github.com/nitolar/genshin-notifications/issues


## Authors

- [@nitolar](https://www.github.com/nitolar)

