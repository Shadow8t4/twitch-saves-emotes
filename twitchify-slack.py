#!/usr/bin/python3
import json
import requests
import slack
from os import mkdir, environ
from os.path import exists

emote_api_link = 'https://api.twitchemotes.com/api/v4/channels/0'
emote_file_tmpl = 'https://static-cdn.jtvnw.net/emoticons/v1/'


def grab_id(n):
    return [f'{n["id"]}', f'{n["code"]}']


def request_twitch_emote_ids():
    headers = {
        'accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': 'x9pe1nhx03034xssm1kcla36unubrc'
    }
    req = requests.get(emote_api_link, headers=headers)
    req_dict = json.loads(req.content)
    req.close()
    return list(map(grab_id, req_dict['emotes']))


def save_twitch_emotes_metadata(dirpath, emote_array):
    metadata_file = open(f'{dirpath}/emote_metadata.txt')
    for x in emote_array:
        metadata_file.write(f'id:{x[0]}\tcode:{x[1]}\n')
    metadata_file.close()


def save_twitch_emotes_images(dirpath, emote_array):
    if(not exists(dirpath)):
        mkdir(dirpath)

    for emote_index in emote_array:
        headers = {
            'accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': 'x9pe1nhx03034xssm1kcla36unubrc'
        }
        req = requests.get(f'{emote_file_tmpl}{emote_index[0]}/1.0', headers=headers)
        emote_file = open(f'{dirpath}/{emote_index[0]}.png', 'bw+')
        emote_file.write(req.content)
        emote_file.close()


def main():
    print("Hello, world!")
    emotes_array = request_twitch_emote_ids()
    save_twitch_emotes_images('out', emotes_array)
    save_twitch_emotes_metadata('out', emotes_array)


if(__name__ == "__main__"):
    main()
