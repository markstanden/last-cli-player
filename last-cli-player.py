""" An application to play a song and retreive information
    about the song from last.fm.

    As this app is only really meant to demonstrate the use of an 
    API within my code the playback and other features are secondary.

    As such the following limitations (features?? :-)) are in place
    the script scans the ./Music directory and adds (currently all) files
    to a list an randomly chooses one to get more information about,
    displays the information, and plays the track.

    I have only tested this on Linux (Pop!_OS 20.04) which uses gstreamer
    to output the MP3 via the playsound library - this works great for me
    and apparently has good cross platform support, hench it's use here

    I really quite like the app, so may continue to develop it!

"""

import json
import os
import random

import eyed3
import playsound as ps
import requests


def play_file (path_and_file):
    """ Plays the file sent the function,
        basic player with basic mp3 fuctionality only,
        but good cross platform support
    """

    ps.playsound(path_and_file)


def get_tags(path_and_file):
    """ Gets tags from the file, this is to identify
        the song to last.fm for API information
    """

    musicfile = eyed3.load(path_and_file)

    tags = {'Title':musicfile.tag.title,
            'Artist':musicfile.tag.artist,
            'Album':musicfile.tag.album,
            'Track':musicfile.tag.track_num[0]
    }

    return tags

def make_last_request(method, tag_dict):
    """ From last.fm api examples:
        http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=YOUR_API_KEY&artist=cher&track=believe&format=json
        The API requires the request to be sent in this format.  Source (https://www.last.fm/api/show/album.getInfo)
        I have found through experimentation you can send artist, album, and track name
        to last.fm and they choose what they need from it, which simplify's our code:
    """

    # The applications public API key
    api_key = "9508bed5c4e8d5e91c63fc1d91c4702e"

    # The URL to send the request to
    last_url = 'http://ws.audioscrobbler.com/2.0/'

    # The parameters to send to last.fm, I have found you can send everyhting,
    # which means we just have to change the method to get the 
    # different returned JSON files
    params = {
              'method':method,
              'api_key':api_key,
              'artist':tag_dict['Artist'],
              'album':tag_dict['Album'],
              'track':tag_dict['Title'],
              'format':'json',
    }

    # Requests sends the http for us: requests.get(url, params={key: value}, args) 
    return requests.get(last_url, params=params)

def last_get_trackinfo(tag_dict):
    """ Calls make last.fm request function, using the track.getInfo method
        This returns a dict containing current track information.
    """
    track_info_request = make_last_request(method='track.getInfo', tag_dict=tag_dict)
    
    # Return a dict with the information retreived from last.fm
    return track_info_request.json()
    

def last_get_similar(tag_dict):
    """ Calls make last.fm request function, using the track.getSimilar method
        This returns a dict file containing similar track information.
    """

    similar_track_request = make_last_request(method='track.getSimilar', tag_dict=tag_dict)
    similar_tracks_dict = similar_track_request.json()
    
    # Return a list of dicts with the similar track information retreived from last.fm
    return similar_tracks_dict['similartracks']['track']


def lastfm_to_screen(last_track_info, last_similar):
    """Display the retreived data from last.fm in a 'beautiful' way
    """
    # The number of similar tracks to display
    similars_to_display = 5

    # As the information is held within dicts inside dicts, inside dicts
    # A little more complicated to get what we need
    print('Track Title:\t', last_track_info['track']['name'])
    print('Artist:\t\t', last_track_info['track']['artist']['name'])
    print('From Album:\t', last_track_info['track']['album']['title'])
    print()

    # The list is 100 tracks long by default, which is not in the spirit of
    # the minimal player
    for count in range(similars_to_display):
        # I have found this stops the error appearing, i need to find out why
        try:
            similars = last_similar.pop(0)
            print('Similar to:\t', similars['name'], 'by', similars['artist']['name'])  
        #not sure what goes here either
        except:
            pass
    print()
    print()

# Set the path to the music directory
music_path = 'Music/'

# Check the provided directory for files, add them to music_files list
# Currently all files in the directory should be tagged MP3 files...
music_files = os.listdir(music_path)

#How many files are in the music_path directory?
number_of_files = len(music_files)

# Iterate the list of files.
for count in range(number_of_files):

    # Choose a random file from the list
    # Allows track to play twice
    # music_file_choice = random.choice(music_files)

    # Randomly choose an integer as a file from the list
    random_file_choice = random.randint(0, (number_of_files - 1))
    
    #choose it, and pop it off, so it can't play again.
    music_file_choice = music_files.pop(random_file_choice)
    number_of_files -= 1
    
    # Get the ID3 tags from the file
    id3_tags = get_tags(music_path + music_file_choice)

    # Put a request in to last.fm for the track information they have 
    # on file:
    track_info = last_get_trackinfo(id3_tags)

    # now find me some similar sounding tracks:
    similar_info = last_get_similar(id3_tags)

    # lets print something nice to the screen instead:
    lastfm_to_screen(track_info, similar_info)
    
    # Play the file.
    play_file(music_path + music_file_choice)
