# Backup Feedly
A Command Line Utility to backup saved feeds (also called as read later's) and subscriptions from feedly.

## Setup

Before using this utility the environment variables `FEEDLY_USER_ID` and `FEEDLY_ACCESS_TOKEN` needs to be set to the user's feedly user id and access token.
You can get both of them by signing up as a developer at https://feedly.com/v3/auth/dev, after which an email will be sent to your registered mail containing a link to retrieve the access token, the same page also contains your user id.

## Usage

    usage: backup-feedly.py [-h] [-v] [--no-saved] [--no-opml]
    
    A Command Line Utility to backup saved items (Read Later's) and subscriptions
    from feedly
    
    optional arguments:
      -h, --help     show this help message and exit
      -v, --verbose  Print what is being done
      --no-saved     Don't fetch and make a bookmark file of saved items
      --no-opml      Don't download OPML file containing the subscribed feeds


By Default the utility downloads and saves the saved feeds (as a bookmark file) as well as downloads the OPML file.

## Errors and Issues

1. The developer access token expires after 30 day after which the utility will give you an error with status code 401 (“token expired”), at which point you should regenerate a new token
2. Also Note that the developer access tokens have a limit of 250 API Requests per day (500 for Pro users), after which the utility gives an error with status code 429 (“API rate limit reached”)