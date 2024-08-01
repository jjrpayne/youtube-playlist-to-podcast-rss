# youtube-playlist-to-podcast-rss
This is a Python script that converts any YouTube playlist into an audio-only podcast RSS feed. This RSS feed can then be imported into any podcast app, allowing you to listen to the YouTube audio as a podcast.

## Requirements
This script requires Python 3 as well as the follwoing libraries:

- [feedgen](https://pypi.org/project/feedgen/)
- [isodate](https://pypi.org/project/isodate/)
- [python-dotenv](https://pypi.org/project/python-dotenv)
- [python-youtube](https://pypi.org/project/python-youtube)

Additionally, you will need a YouTube API key. See [this tutorial](https://sns-sdks.lkhardy.cn/python-youtube/getting_started/) courtesy of the python-youtube docs on how to obtain an API key.

## Setup
Install dependencies:

```python -m pip install dependencies.txt```

The script uses an environment variable to access the API key. Create a file called ".env" in the root folder. Using a text editor of your choice, edit this file so it has the following contents, replacing 'your api key' with the actual API key:

```API_KEY='your api key here'```

## Usage
To use the script run

```python yt-playlist-to-podcast.py playlist_id output_file```

The playlist id is in the playlist URL after ```youtube.com/playlist?list=```. For example if this is the playlist URL: 

```https://www.youtube.com/playlist?list=PLsQ0j1uzt5dZW12ILjb-8E0s2vw_XJtvj```

Then the playlist id would be:
```PLsQ0j1uzt5dZW12ILjb-8E0s2vw_XJtvj```

The output file can be any file. The default if not specified is podcast.xml.

So an example command would be:

```python yt-playlist-to-podcast.py PLsQ0j1uzt5dZW12ILjb-8E0s2vw_XJtvj podcast.xml```

This will generate an XML file containing the RSS feed. To use this XML file you can simply upload it to a text hosting service such as Pastebin or GitHub Gists, then enter the URL of the raw text into your podcast app.
