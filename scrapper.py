# libraries
import pprint
import json
import requests

# modules
from queries import QUERIES

pp = pprint.PrettyPrinter(indent=4)

class Scrapper:
  __posts = []
  __tagged_posts = []


  def __init__(self, user_setup):
    self.__user_setup = user_setup

  @property
  def user_setup(self):
    return self.__user_setup

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
    page_info = payload.get('page_info', {})
    cursor = page_info.get('end_cursor', None)
    has_next_page = page_info.get('has_next_page', False)
    nodes = payload.get('edges', [])
    items = list(map(lambda node: node.get('node'), nodes))
    return {
      'items': items,
      'next_page': has_next_page,
      'cursor': cursor
    }

  def fetch(self):
    if self.user_setup.posts == True:
      self.fetch_posts()
    if self.user_setup.tagged_posts == True:
      self.fetch_tagged_posts()
    pp.pprint(len(self.__posts))
    pp.pprint(len(self.__tagged_posts))

  def fetch_posts(self, cursor=None):
    params = self.get_query_params(QUERIES['get_posts']['hash'], cursor)
    response = requests.get('https://www.instagram.com/graphql/query/', params=params)
    mapped_response = self.map_response(response, QUERIES['get_posts']['data_key'])
    self.__posts.extend(mapped_response.get('items', []))
    if mapped_response.get('next_page', False) == True:
      self.fetch_posts(cursor=mapped_response.get('cursor', None))
    return True

  def fetch_tagged_posts(self, cursor=None):
    params = self.get_query_params(QUERIES['get_tagged_posts']['hash'], cursor)
    response = requests.get('https://www.instagram.com/graphql/query/', params=params)
    mapped_response = self.map_response(response, QUERIES['get_tagged_posts']['data_key'])
    self.__tagged_posts.extend(mapped_response.get('items', []))
    if mapped_response.get('next_page', False) == True:
      self.fetch_tagged_posts(cursor=mapped_response.get('cursor', None))
    return True
