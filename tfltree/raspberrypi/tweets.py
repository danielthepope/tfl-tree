from time import sleep

import twitter
from twitter.error import TwitterError

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

        log.debug('Uploading %s to Twitter', video_file)
        video_id = api.UploadMediaChunked(video_file, media_category='TweetVideo')
        log.debug('Video ID: %s', video_id)
        log.debug('Uploading %s to Twitter', subtitle_file)
        subtitle_id = api.UploadMediaChunked(subtitle_file, media_category='Subtitles')
        log.debug('Subtitle ID: %s', subtitle_id)
        api.PostMediaSubtitlesCreate(video_id, subtitle_id, 'en', 'English')
        log.debug('Successfully associated video with subtitles')
        attempts = 0
        while attempts < 15:
            try:
                status = api.PostUpdate(tweet_text, media=video_id)
                log.info('Uploaded to Twitter successfully!')
                log.debug(status)
                return
            except TwitterError:
                attempts += 1
                log.warn('Error from Twitter after %s attempts. Trying a bit later', attempts)
                sleep(5)
        # Exceeded the maximum attempts
        log.error('Twitter upload exceeded the maximum number of attempts. Giving up.')

    else:
        log.warning('Twitter upload not enabled. Requires API tokens.')
