""" An application to play a song and retreive information
    about the song from last.fm.
    For simplicity the songs provided are used
"""

import eyed3
import playsound as ps
import io
import os
import requests
import json

API_KEY = "9508bed5c4e8d5e91c63fc1d91c4702e"

def play_file (path_and_file):
    """ Plays the file sent the function"""

    ps.playsound(path_and_file)


def get_tags(path_and_file):
    """ Gets tags from the file, this is to identify
        the song to last.fm for scrobbling"""

    musicfile = eyed3.load(path_and_file)

    tags = {'Title':musicfile.tag.title,
            'Artist':musicfile.tag.artist,
            'Album':musicfile.tag.album,
            'Track':musicfile.tag.track_num[0]
            }

    return tags


def get_lfm():
    """ Looks up relevant information about track to be played
    #     returns a list of stuff """

    

    # last_data = [artist, album, track]
    # return last_data


    # tags = get_tags(path_and_file)
    # print(tags)

def last_get_trackinfo(tag_dict):
    """ From last.fm api examples:
        http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=YOUR_API_KEY&artist=cher&track=believe&format=json
        The API requires the request to be sent in this format.  Source (https://www.last.fm/api/show/album.getInfo)
    """

    last_url = 'http://ws.audioscrobbler.com/2.0/?'

    params = {
              'method':'track.getInfo',
              'api_key':API_KEY,
              'artist':tag_dict['Artist'],
              'track':tag_dict['Title'],
              'format':'json',
    }
    
    #requests.get(url, params={key: value}, args) 
    return requests.get(last_url, params=params)

def last_get_similar(tag_dict):
    """ From last.fm api examples:
        http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist=cher&track=believe&api_key=YOUR_API_KEY&format=json
        The API requires the request to be sent in this format.  Source (https://www.last.fm/api/show/track.getSimilar)
    """

    last_url = 'http://ws.audioscrobbler.com/2.0/?'

    params = {
              'method':'track.getSimilar',
              'api_key':API_KEY,
              'artist':tag_dict['Artist'],
              'album':tag_dict['Album'],
              'format':'json',
    }
    
    #requests.get(url, params={key: value}, args) 
    return requests.get(last_url, params=params)


import json

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=1)
    print(text)
    
music_path = 'Music/'
music_files = os.listdir(music_path)
# print(arr)

# file1 = 'Gillicuddy_-_01_-_Adventure_Darling.mp3'
# file2 = 'Kevin_MacLeod_-_08_-_Slow_Burn.mp3'
id3_tags = get_tags(music_path + music_files[0])

track_info = last_get_trackinfo(id3_tags)
similar_info = last_get_similar(id3_tags)
jprint(track_info.json())
jprint(similar_info.json())
play_file(music_path + music_files.pop(0))