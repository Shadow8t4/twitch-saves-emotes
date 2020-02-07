# Twitchify Slack

A Python script meant to utilize the https://twitchemotes.com API to import custom emojis to Slack.

## Installation

Since you're using an API you have to sign in with Twitch as a developer and "register an app".

https://dev.twitch.tv/console/apps

Once you've registered, click on manage and grab the "Client ID".

Save that to a file in the root directory of this project as `.client_id` or save as an environment variable called `TWITCH_APP_CLIENT_ID`.

Ensure you have pipenv installed (`python -m pip install pipenv`) and then install the packages in the Pipfile.

`pipenv install`

## Usage

Once you install the packages, you should be all set. Run the following command to start the script:

`pipenv run python twitchify-slack.py`

This script takes a while, but it will download all the official Twitch emotes and BTTV emotes and output them to the `out/` directory, with the names corresponding to the lowercase versions of their codes on Twitch.