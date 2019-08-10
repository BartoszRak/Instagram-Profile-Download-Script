import pprint
import requests
import json
import os
import time
import urllib.request
import decimal

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
    posts_path = f"{new_scrapping_path}\\posts"
    tags_path = f"{new_scrapping_path}\\tags"
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    if not os.path.exists(profile_result_path):
        os.mkdir(profile_result_path)

    if not os.path.exists(new_scrapping_path):
        os.mkdir(new_scrapping_path)

    if not os.path.exists(posts_path):
        os.mkdir(posts_path)

    if not os.path.exists(tags_path):
        os.mkdir(tags_path)

    return {
        'posts': posts_path,
        'tags': tags_path,
    }


def get_query_params(graphql_query_hash, cursor=''):
    graphql_variables = {
        'id': ID,
        'first': 20,
        'after': cursor,
    }
    graphql_variables_json = json.dumps(graphql_variables)

    return {
        'query_hash': graphql_query_hash,
        'variables': graphql_variables_json,
    }


def save_node(node, save_path, dotVersion=None):
    version = f".{dotVersion}" if dotVersion is not None else ''
    save_name = f"Resource{TOTAL - COUNTER + 1}{version}"
    typename = node['__typename']
    mime = ''
    resource_url = ''

    if typename == "GraphImage":
        mime = "jpg"
        resource_url = 'display_url'
        urllib.request.urlretrieve(
            node[resource_url], f"{save_path}\\{save_name}.{mime}")

    if typename == 'GraphVideo':
        mime = "mp4"
        resource_url = 'video_url'
        urllib.request.urlretrieve(
            node[resource_url], f"{save_path}\\{save_name}.{mime}")

    if typename == 'GraphSidecar':
        sidecar = node.get('edge_sidecar_to_children')
        if sidecar == None:
            mime = 'jpg'
            resource_url = 'display_url'
            if node['is_video'] == True:
                mime = 'mp4'
                resource_url = 'video_url'
            urllib.request.urlretrieve(
                node[resource_url], f"{save_path}\\{save_name}.{mime}")
            return
        for index, post in enumerate(sidecar['edges']):
            save_node(post['node'], save_path, index + 1)


def scrap_profile(query_hash, save_path, end_cursor=''):
    global COUNTER
    global TOTAL
    if end_cursor == '':
        COUNTER = 0
    query_params = get_query_params(query_hash, end_cursor)
    pictures_get_response = requests.get(GRAPHQL_URL, params=query_params)
    pictures_get_response_json = pictures_get_response.json()
    user = pictures_get_response_json['data']['user']
    data = user[list(user.keys())[0]]
    page_info = data['page_info']
    posts = data['edges']
    TOTAL = data['count']
    for index, post in enumerate(posts):
        COUNTER = COUNTER + 1
        post_node = post['node']
        save_node(post_node, save_path)
        pp.pprint(
            f"{round(COUNTER/TOTAL * 100, 2)}% - Item {COUNTER}/{TOTAL} saved.")

    if page_info['has_next_page']:
        scrap_profile(query_hash, save_path, page_info['end_cursor'])


# init
pp = pprint.PrettyPrinter(indent=4)

# main
INSTAGRAM_BASE_URL = 'https://www.instagram.com/'
GRAPHQL_URL = f"{INSTAGRAM_BASE_URL}graphql/query/"
POSTS_QUERY_HASH = 'f2405b236d85e8296cf30347c9f08c2a'
TAGGED_QUERY_HASH = 'ff260833edf142911047af6024eb634a'
PROFILE_NAME = input('Instagram profile NAME: ')
COUNTER = 0
TOTAL = 0
profile_url = f"{INSTAGRAM_BASE_URL}{PROFILE_NAME}/"
pp.pprint(profile_url)
html_response = requests.get(profile_url)

ID = get_id_from_profile_html(html_response)
get_time = time.strftime('%Y.%m.%d-%H%M%S')
PATHS = check_directories()
try:
    pp.pprint('=== POSTS ===')
    scrap_profile(POSTS_QUERY_HASH, PATHS['posts'])
    pp.pprint('=== TAGS ===')
    scrap_profile(TAGGED_QUERY_HASH, PATHS['tags'])
except Exception as exc:
    pp.pprint(f"[ERROR] Scrapping failed.{str(exc)}")

pp.pprint('[SUCCESS] Scrapping finished.')
