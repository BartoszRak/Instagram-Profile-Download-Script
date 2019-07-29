import pprint
import requests
import json
import os
import time
import urllib.request

from instagram.client import InstagramAPI

# utils


def get_id_from_profile_html(response):
    search = 'profilePage_'
    profile_text = response.text
    id_index = profile_text.find(search)
    text_started_with_id = profile_text[id_index + len(search):]
    return text_started_with_id[:text_started_with_id.find('"')]


def check_directories():
    path = os.getcwd()
    result_path = f"{path}\\results"
    profile_result_path = f"{result_path}\\{PROFILE_NAME}"
    new_scrapping_path = f"{profile_result_path}\\{get_time}"

    if not os.path.exists(result_path):
        os.mkdir(result_path)

    if not os.path.exists(profile_result_path):
        os.mkdir(profile_result_path)

    if not os.path.exists(new_scrapping_path):
        os.mkdir(new_scrapping_path)

    return new_scrapping_path


def get_query_params(cursor=''):
    graphql_variables = {
        'id': ID,
        'first': 20,
        'after': cursor,
    }
    graphql_variables_json = json.dumps(graphql_variables)
    graphql_query_hash = 'f2405b236d85e8296cf30347c9f08c2a'

    return {
        'query_hash': graphql_query_hash,
        'variables': graphql_variables_json,
    }


def scrap_profile(endCursor=''):
    graphql_url = f"{INSTAGRAM_BASE_URL}graphql/query/"
    query_params = get_query_params(endCursor)
    pictures_get_response = requests.get(graphql_url, params=query_params)
    pictures_get_response_json = pictures_get_response.json()
    user = pictures_get_response_json['data']['user']
    page_info = user['edge_owner_to_timeline_media']['page_info']
    posts = user['edge_owner_to_timeline_media']['edges']

    new_scrapping_path = check_directories()

    for index, post in enumerate(posts):
        post_node = post['node']
        urllib.request.urlretrieve(
            post_node['display_url'], f"{new_scrapping_path}\\{post_node['id']}.jpg")

    pp.pprint(f"# {len(posts)} pictures have been saved.")

    if page_info['has_next_page']:
        scrap_profile(page_info['end_cursor'])


# init
pp = pprint.PrettyPrinter(indent=4)

# main
INSTAGRAM_BASE_URL = 'https://www.instagram.com/'
PROFILE_NAME = input('Instagram profile NAME: ')
profile_url = f"{INSTAGRAM_BASE_URL}{PROFILE_NAME}/"
pp.pprint(profile_url)
html_response = requests.get(profile_url)

ID = get_id_from_profile_html(html_response)
get_time = time.strftime('%Y.%m.%d-%H%M%S')

try:
    scrap_profile()
except:
    pp.pprint('[ERROR] Scrapping failed.')

pp.pprint('[SUCCESS] Scrapping finished.')
