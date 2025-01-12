<h1 align="center">TelecastBot Telegram Bot 🎸</h1>

<p align="center">
  <a href="https://github.com/bisnuray/TelecastBot/stargazers"><img src="https://img.shields.io/github/stars/bisnuray/TelecastBot?color=blue&style=flat" alt="GitHub Repo stars"></a>
  <a href="https://github.com/bisnuray/TelecastBot/issues"><img src="https://img.shields.io/github/issues/bisnuray/TelecastBot" alt="GitHub issues"></a>
  <a href="https://github.com/bisnuray/TelecastBot/pulls"><img src="https://img.shields.io/github/issues-pr/bisnuray/TelecastBot" alt="GitHub pull requests"></a>
  <a href="https://github.com/bisnuray/TelecastBot/graphs/contributors"><img src="https://img.shields.io/github/contributors/bisnuray/TelecastBot?style=flat" alt="GitHub contributors"></a>
  <a href="https://github.com/bisnuray/TelecastBot/network/members"><img src="https://img.shields.io/github/forks/bisnuray/TelecastBot?style=flat" alt="GitHub forks"></a>
</p>

<p align="center">
  <em>TelecastBot: Streams videos & audio in Telegram voice chats for both groups and channels. It supports live streams, YouTube videos, and Telegram media. It also supports scheduling streams, recording, and more.</em>
</p>

---

## Features 🌟

- **Playlist and Queue Management:** Smooth transitions with zero downtime.
- **Video Recording:** Capture moments directly from voice chats.
- **Voicechat Scheduling:** Plan and automate your streams.
- **Spotify Track Support:** Stream music directly from Spotify track links.
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
21. `SPOTIFY_CLIENT_ID` - Your Spotify Client ID, obtain from [Spotify Developer Console](https://developer.spotify.com/dashboard/).
22. `SPOTIFY_CLIENT_SECRET` - Your Spotify Client Secret, obtain from [Spotify Developer Console](https://developer.spotify.com/dashboard/).

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
   - Update your `cookies.txt` in the `TelecastBot/ytcookies` directory of your project.

### Managing Cookies:

- **Cookie Expiry:**
  - Refresh your cookies by exporting new ones if you encounter download issues.

- **Cookie Depletion:**
  - Avoid frequent bot restarts and excessive YouTube requests to prevent early cookie expiry.

This setup should help manage YouTube content access efficiently without encountering sign-in or bot protection errors.

## System Requirements

- **Python:** Version 3.8 or higher recommended.
- **NodeJS:** Version 15.0.0 or higher.
- **FFMpeg:** Necessary for media processing.

Ensure that your environment meets these specifications to guarantee full functionality of the script.

## Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://www.heroku.com/deploy/?template=https://github.com/bisnuray/TelecastBot)

## Deploy to VPS

```sh
git clone https://github.com/bisnuray/TelecastBot
cd TelecastBot
pip3 install -r requirements.txt
# install node js
sudo bash install_node.sh
# <Create Variables appropriately (.env [optional])> Or Directly Edit Config.py
python3 main.py
```

# Project Contributors

### Main Author 🧑‍💻
- **Name:** Subin
- **Telegram:** [@subin_works](https://t.me/subin_works)

### Contributing Author 🧑‍💻
- **Name:** Bisnu Ray
- **Telegram:** [@itsSmartDev](https://t.me/itsSmartDev)

---

For inquiries or feedback, please feel free to reach out via Telegram.

## Ethical Notice 🔔
> **Ethics Reminder:** Simply modifying a few lines of code does not constitute original authorship. When forking a project, always fork responsibly and give proper credit to the original creators.

