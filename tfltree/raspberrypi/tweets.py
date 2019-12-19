from time import sleep

import twitter
from twitter.error import TwitterError

from tfltree import logger as log
from tfltree.raspberrypi.config import (ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET,
                                        CONSUMER_KEY, CONSUMER_SECRET)
from tfltree.raspberrypi.speech import map_tube_id_to_name

# Twitter requires all keys
enabled = False
if all([CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET]):
    enabled = True


def flatten(list_of_lists):
    output = []
    for l in list_of_lists:
        output += l
    return sorted(list(set(output)))


def generate_tweet_text(audio_statuses):
    delayed_lines = flatten([s.affected_lines for s in audio_statuses if not s.status_codes.isdisjoint({6, 9})])
    closed_lines = flatten(
        [s.affected_lines for s in audio_statuses if not s.status_codes.isdisjoint({1, 2, 3, 4, 5, 11, 20})])
    info_lines = flatten([s.affected_lines for s in audio_statuses if not s.status_codes.isdisjoint(
        {0, 7, 8, 11, 12, 13, 14, 15, 16, 17, 18, 19})])

    output = 'London Underground status:\n'
    if delayed_lines or closed_lines or info_lines:
        if delayed_lines:
            output += 'Delays on ' + ', '.join(list(map(map_tube_id_to_name, delayed_lines))) + '\n'
        if closed_lines:
            output += 'Closures on ' + ', '.join(list(map(map_tube_id_to_name, closed_lines))) + '\n'
        if info_lines:
            output += 'Info about ' + ', '.join(list(map(map_tube_id_to_name, info_lines)))
        output = output.strip()
    else:
        output = 'Good service on all lines'
    return output


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
        twitter_error = None
        while attempts < 15:
            try:
                status = api.PostUpdate(tweet_text, media=video_id)
                log.info('Uploaded to Twitter successfully!')
                log.debug(status)
                return
            except TwitterError as e:
                attempts += 1
                log.warn('Error from Twitter after %s attempts. Trying a bit later', attempts)
                sleep(5)
                twitter_error = e
        # Exceeded the maximum attempts
        log.error('Twitter upload exceeded the maximum number of attempts. Giving up.')
        raise twitter_error

    else:
        log.warning('Twitter upload not enabled. Requires API tokens.')


if __name__ == "__main__":
    from tfltree.raspberrypi import tfl, speech
    status = tfl.TflApi().update_status()
    audio_statuses = speech.generate_phrases_for_status(status)
    tweet_text = generate_tweet_text(audio_statuses)
    log.info(tweet_text)
