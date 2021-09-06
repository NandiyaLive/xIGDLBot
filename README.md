<h1>Instagram Media Downloader Bot</h1>

<h3>What is this repo about?</h3>
<p>This is a telegram bot writen in python for downloading media from Instagram.<p>

<h3>Features supported:</h3>
<ul>
  <li>Download Stories</li>
  <li>Download Media from the feed as a zip file</li>
  <li>Download IGTV Videos</li>
</ul>

<h3>Upcoming features (TODOs):</h3>
<ul>
  <li>Add highlights download support</li>
</ul>

<h3>How to deploy?</h3>

<h4>Installing requirements</h4>

- Clone this repo:
```
git clone https://github.com/NandiyaLive/xIGDLBot
cd xIGDLBot
```

- Install requirements
For Debian based distros
```
sudo apt install python3
```
For Arch and it's derivatives:
```
sudo pacman -S docker python
```

Install Docker by following the [official docker docs](https://docs.docker.com/engine/install/debian/)

<h4>Edit bot token</h4>

```
sudo nano bot.py
```

Get a bot token from @BotFather and paste it inside "".

<h4>Deploying</h4>

- Start docker daemon (skip if already running):
```
sudo dockerd
```
- Build Docker image:
```
sudo docker build . -t xigdlbot
```
- Run the image:
```
sudo docker run xigdlbot
```
<br>
© Neranjana Prasad 2020.
