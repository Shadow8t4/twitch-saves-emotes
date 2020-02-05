#!/usr/bin/python3
from os import mkdir, environ
from os.path import exists
import requests
import slack
import json

# Twitch emote api link for emote metadata
twitch_emote_api_link = 'https://api.twitchemotes.com/api/v4/channels/0'
# Twitch emote link for emote images
twitch_emote_file_tmpl = 'https://static-cdn.jtvnw.net/emoticons/v1/'

# BTTV emote api link for emote metadata
bttv_emote_api_link = 'https://api.betterttv.net/2/emotes'
# BTTV emote link for emote images
bttv_emote_file_tmpl = 'https://cdn.betterttv.net/emote/'


def grab_id(n):
    """Map function to extract the id and code from each dictionary entry

    Arguments:
        n {int} -- Current dictionary object

    Returns:
        arr -- Array containing the id and code
    """
    return [f'{n["id"]}', f'{n["code"]}']


def request_twitch_emote_ids(service):
    """Send the request for a json of the Twitch emote metadata
    
    Arguments:
        service {str} -- String containing either "Twitch" or "BTTV" to determine which code to use
    
    Returns:
        list -- List iterable of the ids and codes for the emotes returned by the request json
    """

    req_dict = {}

    if(service.lower() == 'twitch'):
        headers = {
            'accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': 'x9pe1nhx03034xssm1kcla36unubrc'
        }
        req = requests.get(twitch_emote_api_link, headers=headers)
        req_dict = json.loads(req.content)
        req.close()
    elif(service.lower() == 'bttv'):
        req = requests.get(bttv_emote_api_link)
        req_dict = json.loads(req.content)
        req.close()

    return list(map(grab_id, req_dict['emotes']))


def save_twitch_emotes_metadata(dirpath, emote_array):
    """Save the emote_array metadata to a text file to refer to later
    
    Arguments:
        dirpath {str} -- String containing the directory path for output
        emote_array {list} -- List iterable of the ids and code for the emotes returned by the original request json
    """

    if(not exists(f'{dirpath}/emote_metadata.txt')):
        metadata_file = open(f'{dirpath}/emote_metadata.txt', 'w+')
    else:
        metadata_file = open(f'{dirpath}/emote_metadata.txt', 'a')

    for x in emote_array:
        metadata_file.write(f'id:{x[0]}\tcode:{x[1]}\n')
    metadata_file.close()


def save_twitch_emotes_images(service, dirpath, emote_array):
    """Send a request for the emote images and save them locally to a specified directory
    
    Arguments:
        service {str} -- String contianing either "Twitch" or "BTTV" to determine which code to use
        dirpath {str} -- String containing the directory path for output
        emote_array {list} -- List iterable of the ids and codes for the emotes returned by the original request json
    """

    if(not exists(dirpath)):
        mkdir(dirpath)

    if(service.lower() == 'twitch'):
        for emote_index in emote_array:
            if(not exists(f'{dirpath}/{emote_index[1].lower()}.png')):
                headers = {
                    'accept': 'application/vnd.twitchtv.v5+json',
                    'Client-ID': 'x9pe1nhx03034xssm1kcla36unubrc'
                }
                req = requests.get(
                    f'{twitch_emote_file_tmpl}{emote_index[0]}/1.0', headers=headers)
                if('/' in emote_index[1] or '\\' in emote_index[1] or ':' in emote_index[1]):
                    pass
                else:
                    emote_file = open(f'{dirpath}/{emote_index[1].lower()}.png', 'bw+')
                    emote_file.write(req.content)
                    emote_file.close()
    elif(service.lower() == 'bttv'):
        for emote_index in emote_array:
            if(not exists(f'{dirpath}/{emote_index[1].lower()}.png')):
                req = requests.get(
                    f'{bttv_emote_file_tmpl}{emote_index[0]}/1x')
                emote_file = open(f'{dirpath}/{emote_index[1].lower()}.png', 'bw+')
                emote_file.write(req.content)
                emote_file.close()


def main():
    # Grab the Twitch official emotes
    emotes_array = request_twitch_emote_ids('twitch')
    save_twitch_emotes_images('twitch', 'out', emotes_array)
    save_twitch_emotes_metadata('out', emotes_array)

    # Grab the BTTV emotes
    emotes_array = request_twitch_emote_ids('bttv')
    save_twitch_emotes_images('bttv', 'out', emotes_array)
    save_twitch_emotes_metadata('out', emotes_array)


if(__name__ == "__main__"):
    main()
