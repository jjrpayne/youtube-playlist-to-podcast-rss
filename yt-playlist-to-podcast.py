from feedgen.feed import FeedGenerator
from pyyoutube import Api
from isodate import parse_duration
from dotenv import load_dotenv
import os
import argparse

def main():
	load_dotenv()
	API_KEY = os.getenv('API_KEY')
	SECONDS_TO_BYTES = 16181
	YOUTUBE_PREFIX = 'https://youtube.com/playlist?list='
	PODTUBE_PREFIX = 'https://podtube.me/episode/'

	fg = FeedGenerator()
	fg.load_extension('podcast')

	try:
		api = Api(api_key=API_KEY)
	except Exception as e:
		print('Error: ' + e.message)

	parser = argparse.ArgumentParser(description='argument parser')
	parser.add_argument('playlist_id')
	parser.add_argument('output', nargs='?', default='podcast.xml')
	args = parser.parse_args()

	playlist_results = api.get_playlist_by_id(playlist_id=args.playlist_id)
	if (len(playlist_results.items) == 0):
		raise Exception("No playlist found with this id")
	playlist_by_id = playlist_results.items[0]
	playlist_items = api.get_playlist_items(playlist_id=args.playlist_id, count=None).items

	print('Playlist found. Title: ' + playlist_by_id.snippet.title)
	fg.title(playlist_by_id.snippet.title)
	fg.author({'name': playlist_by_id.snippet.channelTitle})
	fg.podcast.itunes_author(playlist_by_id.snippet.channelTitle)
	fg.logo(playlist_by_id.snippet.thumbnails.default.url)
	# description is mandatory so put a placeholder if blank
	if (playlist_by_id.snippet.description):
		fg.description(playlist_by_id.snippet.description)
	else:
		fg.description('No description provided.')
	fg.link(href=YOUTUBE_PREFIX + args.playlist_id, rel='alternate')

	for item in playlist_items:
		video_id = item.snippet.resourceId.videoId
		video_item = api.get_video_by_id(video_id=video_id)
		# check if video is available/not deleted
		if (len(video_item.items) != 0):
			fe = fg.add_entry()
			fe.id(video_id)
			fe.title(item.snippet.title)
			fe.author({'name': item.snippet.channelTitle})
			fe.description(item.snippet.description)
			fe.published(item.snippet.publishedAt)
			duration = parse_duration(video_item.items[0].contentDetails.duration)
			size_in_bytes = int(duration.total_seconds()*SECONDS_TO_BYTES)
			fe.enclosure(PODTUBE_PREFIX + item.snippet.resourceId.videoId + '.m4a', size_in_bytes, 'audio/mp4')
			fe.podcast.itunes_duration(int(duration.total_seconds()))
			fe.podcast.itunes_image(item.snippet.thumbnails.default.url)

	fg.rss_str(pretty=True)
	fg.rss_file(args.output)
	print('Success! File created at ' + args.output)

if __name__ == "__main__":
	main()
