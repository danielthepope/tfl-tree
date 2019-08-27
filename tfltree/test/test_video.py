from tfltree.raspberrypi import video


def test_package_command():
    video_file = 'my_video.h264'
    audio_files = ['audio_1.wav', 'audio_2.wav', 'audio_3.wav']
    expected = ['ffmpeg', '-y', '-r', '30', '-i', 'my_video.h264', '-i', 'audio_1.wav', '-i', 'audio_2.wav', '-i',
                'audio_3.wav', '-filter_complex', '[1:0][2:0][3:0]concat=n=3:v=0:a=1[outa]', '-map', '0:0', '-map', '[outa]',
                '-c:v', 'copy', '-c:a', 'mp3', 'output.mp4']
    actual = video._generate_ffmpeg_package_command(video_file, audio_files, 'output.mp4')
    assert actual == expected


def test_burn_subtitles_command():
    video_file = 'my_video.h264'
    audio_files = ['audio_1.wav', 'audio_2.wav']
    subtitle_file = 'subs.srt'
    expected = ['ffmpeg', '-y', '-r', '30', '-i', 'my_video.h264', '-i', 'audio_1.wav', '-i', 'audio_2.wav', '-filter_complex',
                '[1:0][2:0]concat=n=2:v=0:a=1[outa]', '-map', '0:0', '-map', '[outa]', '-vf', 'subtitles=subs.srt', '-c:a',
                'mp3', 'output.mp4']
    actual = video._generate_ffmpeg_burn_subtitles_command(video_file, audio_files, subtitle_file, 'output.mp4')
    assert actual == expected
