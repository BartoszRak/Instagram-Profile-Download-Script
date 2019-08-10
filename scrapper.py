# libraries
import pprint
import json
import requests

# modules
from queries import QUERIES

pp = pprint.PrettyPrinter(indent=4)

class Scrapper:
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

  def start(self):
    if self.user_setup.posts == True:
      self.scrap_posts()
    if self.user_setup.tagged_posts == True:
      self.scrap_tagged_posts()

  def scrap_posts(self, cursor=None):
    pp.pprint('scrap posts')
    params = self.get_query_params(QUERIES['get_posts']['hash'], cursor)
    pp.pprint(params)
    response = requests.get('https://www.instagram.com/graphql/query/', params=params)
    parsed_response = response.json()

  def scrap_tagged_posts(self, cursor=None):
    pp.pprint('scrap tagged posts')
