import twitter

from tfltree import logger as log
from tfltree.raspberrypi.config import (ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET,
                                        CONSUMER_KEY, CONSUMER_SECRET)

# Twitter requires all keys
enabled = False
if all([CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET]):
    enabled = True


def post_video(tweet_text, video_file, subtitle_file):
    if enabled:
        api = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

        log.info('Uploading %s to Twitter', video_file)
        video_id = api.UploadMediaChunked(video_file, media_category='TweetVideo')
        log.info('Video ID: %s', video_id)
        log.info('Uploading %s to Twitter', subtitle_file)
        subtitle_id = api.UploadMediaChunked(subtitle_file, media_category='Subtitles')
        log.info('Subtitle ID: %s', subtitle_id)
        api.PostMediaSubtitlesCreate(video_id, subtitle_id, 'en', 'English')
        log.info('Successfully associated video with subtitles')
        api.PostUpdate(tweet_text, media=video_id)
    else:
        log.warning('Twitter upload not enabled. Requires API tokens.')
