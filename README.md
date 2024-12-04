<h1 align="center">SmartVCPlayer Telegram Bot 🎸</h1>

<p align="center">
  <a href="https://github.com/bisnuray/SmartVCPlayer/stargazers"><img src="https://img.shields.io/github/stars/bisnuray/SmartVCPlayer?color=blue&style=flat" alt="GitHub Repo stars"></a>
  <a href="https://github.com/bisnuray/SmartVCPlayer/issues"><img src="https://img.shields.io/github/issues/bisnuray/SmartVCPlayer" alt="GitHub issues"></a>
  <a href="https://github.com/bisnuray/SmartVCPlayer/pulls"><img src="https://img.shields.io/github/issues-pr/bisnuray/SmartVCPlayer" alt="GitHub pull requests"></a>
  <a href="https://github.com/bisnuray/SmartVCPlayer/graphs/contributors"><img src="https://img.shields.io/github/contributors/bisnuray/SmartVCPlayer?style=flat" alt="GitHub contributors"></a>
  <a href="https://github.com/bisnuray/SmartVCPlayer/network/members"><img src="https://img.shields.io/github/forks/bisnuray/SmartVCPlayer?style=flat" alt="GitHub forks"></a>
</p>

<p align="center">
  <em>VCPlayer bot streams videos & audio in Telegram voice chats for both groups and channels, supporting live streams, YouTube videos, Telegram media, scheduling, recording, and more.</em>
</p>

---

## Features 🌟

- **Playlist and Queue Management:** Smooth transitions with zero downtime.
- **Video Recording:** Capture moments directly from voice chats.
- **Voicechat Scheduling:** Plan and automate your streams.
- **Flexible UI:** Easy control over the player with an intuitive interface.
- **Customizable Settings:** Toggle between audio or video modes, adjust quality, and more.
- **YouTube Playlist Support:** Stream directly from YouTube playlists.
- **Live Streaming:** Support for YouTube live streams.
- **Telegram File Playback:** Play media files shared within Telegram.
- **Auto-Restart:** Reliable operation through automatic restarts, even after platform reboots.
- **Playlist Import/Export:** Easily manage your playlists.
- **Rich Customization:** Change the voice chat title to the currently playing song, and much more.
<br>
<h2 align="center">Configuration Variables</h2>
<hr>

### Mandatory Vars

1. `API_ID` - Obtain from [my.telegram.org](https://my.telegram.org/)
2. `API_HASH` - Obtain from [my.telegram.org](https://my.telegram.org)
3. `BOT_TOKEN` - Create a bot via [@Botfather](https://telegram.dog/BotFather)
4. `SESSION_STRING` -  Open [@SmartUtilBot](https://t.me/SmartUtilBot). Bot and use /pyro command and then follow all instructions.
5. `CHAT` - Channel/Group ID where the bot plays music.

### Recommended Optional Vars

1. `DATABASE_URI` - MongoDB database Url, recommended for full feature access, obtain from [mongodb](https://cloud.mongodb.com).
2. `HEROKU_API_KEY` - Your Heroku API key, generate [here](https://dashboard.heroku.com/account/applications/authorizations/new).
3. `HEROKU_APP_NAME` - Your Heroku app's name.
4. `FILTERS` - Customize search filters for channel play (e.g., `video document`, `video document audio`, `video`).

### Optional Vars

1. `LOG_GROUP` : Group to send Playlist, if CHAT is a Group()
2. `ADMINS` : ID of users who can use admin commands.
3. `STARTUP_STREAM` : This will be streamed on startups and restarts of bot. You can use either any STREAM_URL or a direct link of any video or a Youtube Live link.
4. `REPLY_MESSAGE` : A reply to those who message the USER account in PM. Leave it blank if you do not need this feature. (Configurable through bot if mongodb added.)
5. `ADMIN_ONLY` : Pass `True` If you want to make /play command only for admins of `CHAT`. By default /play is available for all.(Configurable through bot if mongodb added.)
6. `DATABASE_NAME`: Database name for your mongodb database.
7. `SHUFFLE` : Make it `False` if you dont want to shuffle playlists. (Configurable through bot if mongodb added.)
8. `EDIT_TITLE` : Make it `False` if you do not want the bot to edit video chat title according to playing song. (Configurable through bot if mongodb added.)
9. `RECORDING_DUMP` : A Channel ID with the USER account as admin, to dump video chat recordings.
10. `RECORDING_TITLE`: A custom title for your videochat recordings.
11. `TIME_ZONE` : Time Zone of your country, by default IST
12. `IS_VIDEO_RECORD` : Make it `False` if you do not want to record video, and only audio will be recorded.(Configurable through bot if mongodb added.)
13. `IS_LOOP` ; Make it `False` if you do not want 24 / 7 Video Chat. (Configurable through bot if mongodb added.)
14. `IS_VIDEO` : Make it `False` if you want to use the player as a musicplayer without video. (Configurable through bot if mongodb added.)
15. `PORTRAIT`: Make it `True` if you want the video recording in portrait mode. (Configurable through bot if mongodb added.)
16. `DELAY` : Choose the time limit for commands deletion. 10 sec by default.
18. `QUALITY` : Customize the quality of video chat, use one of `high`, `medium`, `low` . 
19. `BITRATE` : Bitrate of audio (Not recommended to change).
20. `FPS` : Fps of video to be played (Not recommended to change.)

## Handling YouTube Download Errors with Cookies

To avoid errors related to YouTube sign-in requirements, using a cookie file is effective. Here's how to set it up:

### Steps to Export and Use Cookies:

1. **Create a Dedicated Chrome Profile:**
   - It's recommended to create a new Chrome profile for managing your bot's cookies.

2. **Install a Cookie Management Extension:**
   - Use "Cookie Editor" or similar extensions to manage your cookies.

3. **Export Cookies from YouTube:**
   - Log into YouTube in your new browser profile and export cookies in Netscape format via the cookie extension.

4. **Save the Cookies File:**
   - Update your `cookies.txt` in the `SmartVCPlayer/ytcookies` directory of your project.

### Managing Cookies:

- **Cookie Expiry:**
  - Refresh your cookies by exporting new ones if you encounter download issues.

- **Cookie Depletion:**
  - Avoid frequent bot restarts and excessive YouTube requests to prevent early cookie expiry.

This setup should help manage YouTube content access efficiently without encountering sign-in or bot protection errors.

## Prerequisites

- Python 3.8 or higher.
- NodeJS 15.0.0 or higher.
- FFMpeg

## Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://www.heroku.com/deploy/?template=https://github.com/bisnuray/SmartVCPlayer)

## Deploy to VPS

```sh
git clone https://github.com/bisnuray/SmartVCPlayer
cd SmartVCPlayer
pip3 install -r requirements.txt
# install node js
sudo bash install_node.sh
# <Create Variables appropriately (.env [optional])> Or Directly Edit Config.py
python3 main.py
```

## 📌 Top Music Stream Live Link

- [Live Channel](https://telegra.ph/Top-Music-Stream-Live-Link-02-02).

## Main Author 🧑‍💻

- Name: Subin
- Telegram: [@subin_works](https://t.me/subin_works)

## Update Author 🧑‍💻

- Name: Bisnu Ray
- Telegram: [@SmartBisnuBio](https://t.me/SmartBisnuBio)

## Notice 🔔🔔

<b>Editing a few lines of code and claiming authorship does not make you a developer. Fork responsibly and credit original sources.</b>

## Credits 🏆

Huge thanks to the following individuals and their projects for making SmartVCPlayer possible:

- **[Laky-64](https://github.com/Laky-64)** for [py-tgcalls](https://github.com/pytgcalls/pytgcalls), enabling advanced voice chat capabilities.
- **[Dan](https://github.com/delivrance)** for [Pyrogram](https://github.com/pyrogram/pyrogram), a robust framework for Telegram bot development.

Their contributions are pivotal to the functionality and success of SmartVCPlayer.


