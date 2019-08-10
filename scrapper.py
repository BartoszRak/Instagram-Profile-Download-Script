# libraries
import pprint
import json
import requests
import time

# modules
from queries import QUERIES
from utils import get_absolute_path

pp = pprint.PrettyPrinter(indent=4)

class Scrapper:
  __posts = []
  __tagged_posts = []
  __paths = {}

  def __init__(self, user_setup):
    self.__user_setup = user_setup

  @property
  def user_setup(self):
    return self.__user_setup

  def prepare_directories(self):
    relative_base_path = 'results'
    relative_user_path = f"{relative_base_path}/{self.user_setup.profile_name}"
    relative_scrapping_path = f"{relative_user_path}/{time.strftime('%Y.%m.%d-%H%M%S')}"
    relative_posts_path = f"{relative_scrapping_path}/posts"
    relative_tagged_posts_path = f"{relative_scrapping_path}/tagged-posts"

    results_path = get_absolute_path(relative_base_path)
    user_path = get_absolute_path(relative_user_path)
    scrapping_path = get_absolute_path(relative_scrapping_path)
    posts_path = get_absolute_path(relative_posts_path)
    tagged_posts_path = get_absolute_path(relative_tagged_posts_path)

    paths = {
      results_path,
      user_path,
      scrapping_path,
      posts_path,
      tagged_posts_path,
    }
    self.__paths = paths
    return paths

  def get_query_params(self, query_hash, cursor=None):
    variables = {
        'id': self.user_setup.profile_id,
        'first': 20,
    }
    if cursor is not None:
      variables['after'] = cursor
    return {
        'query_hash': query_hash,
        'variables': json.dumps(variables),
    }

  def map_response(self, response, data_key):
    parsed_response = response.json()
    data = parsed_response.get('data', {})
    user = data.get('user', {})
    payload = user.get(data_key, {})
    count = payload.get('count', 0)
    page_info = payload.get('page_info', {})
    cursor = page_info.get('end_cursor', None)
    has_next_page = page_info.get('has_next_page', False)
    nodes = payload.get('edges', [])
    items = list(map(lambda node: node.get('node'), nodes))
    return {
      'items': items,
      'next_page': has_next_page,
      'cursor': cursor,
      'count': count,
    }

  def save(self):
    self.prepare_directories()

  def fetch(self):
    if self.user_setup.posts == True:
      self.fetch_posts(0)
      pp.pprint(f"# RESULT: {len(self.__posts)} posts fetched.")
    if self.user_setup.tagged_posts == True:
      self.fetch_tagged_posts(0)
      pp.pprint(f"# RESULT: {len(self.__tagged_posts)} tagged posts fetched.")

  def fetch_posts(self, counter=None, cursor=None):
    new_counter = counter + 1
    if cursor is None:
      pp.pprint(f"==> Fetching posts...")
    pp.pprint(f"- {new_counter} part fetched.")
    params = self.get_query_params(QUERIES['get_posts']['hash'], cursor)
    response = requests.get('https://www.instagram.com/graphql/query/', params=params)
    mapped_response = self.map_response(response, QUERIES['get_posts']['data_key'])
    self.__posts.extend(mapped_response.get('items', []))
    if mapped_response.get('next_page', False) == True:
      self.fetch_posts(counter=new_counter, cursor=mapped_response.get('cursor', None))
    return True

  def fetch_tagged_posts(self, counter=None, cursor=None):
    new_counter = counter + 1
    if cursor is None:
      pp.pprint(f"==> Fetching tagged posts...")
    pp.pprint(f"- {new_counter} part fetched.")
    params = self.get_query_params(QUERIES['get_tagged_posts']['hash'], cursor)
    response = requests.get('https://www.instagram.com/graphql/query/', params=params)
    mapped_response = self.map_response(response, QUERIES['get_tagged_posts']['data_key'])
    self.__tagged_posts.extend(mapped_response.get('items', []))
    if mapped_response.get('next_page', False) == True:
      self.fetch_tagged_posts(counter=new_counter, cursor=mapped_response.get('cursor', None))
    return True
