# InstAnalytics

## About

This Python script scrapes the web version of Instagram to get the number of posts, followers, and following from any **public** account. The data is then stored in a JSON file (`InstAnalytics.json`) so you can get track changes.


## Requirements

`pip install -r requirements.txt`

## Configuration

When you run the script, pass a list of accounts to track:

`python InstAnalytics.py nike,drake`

## Cronjob

If you want to run it everyday at 6am:

`crontab -e`

`0 6 * * * /usr/bin/python /path/to/InstaAnalytics.py`
