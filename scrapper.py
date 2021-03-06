# libraries
import pprint
import json
import requests
import time
import urllib.request
import cv2
import traceback

# modules
from queries import QUERIES
from utils import get_absolute_path, get_image_from_url

pp = pprint.PrettyPrinter(indent=4)

class Scrapper:
  __posts = []
  __tagged_posts = []
  __paths = None
  
  def __init__(self, user_setup, config):
    self.__user_setup = user_setup
    self.__config = config

  @property
  def user_setup(self):
    return self.__user_setup

  @property
  def config(self):
    return self.__config

  def prepare_directories(self):
    relative_base_path = 'results'
    relative_user_path = f"{relative_base_path}/{self.user_setup.profile_name}"
    relative_scrapping_path = f"{relative_user_path}/{time.strftime('%Y.%m.%d-%H%M%S')}"
    relative_posts_path = f"{relative_scrapping_path}/posts"
    relative_tagged_posts_path = f"{relative_scrapping_path}/tagged-posts"
    relative_fetched_data_path = f"{relative_scrapping_path}/FETCHED_DATA"

    results_path = get_absolute_path(relative_base_path)
    user_path = get_absolute_path(relative_user_path)
    scrapping_path = get_absolute_path(relative_scrapping_path)
    posts_path = get_absolute_path(relative_posts_path)
    tagged_posts_path = get_absolute_path(relative_tagged_posts_path)
    fetched_data_path = get_absolute_path(relative_fetched_data_path)

    paths = {
      'results_path': results_path,
      'user_pathu': user_path,
      'scrapping_path': scrapping_path,
      'posts_path': posts_path,
      'tagged_posts_path': tagged_posts_path,
      'fetched_data_path': fetched_data_path,
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
  
  def save_resource(self, url, save_path, mime, iteration=1):
    try:
      if self.user_setup.prevent_reverse_search == True and mime == 'jpg':
        image = get_image_from_url(url)
        horizontal_image = cv2.flip(image, 1)
        cv2.imwrite(save_path, horizontal_image)
        return
      urllib.request.urlretrieve(url, save_path)
    except Exception:
      pp.pprint('(!!!) ERROR occured.')
      traceback.print_exc()
      if (iteration <= 4):
        pp.pprint('(!!!) Retrying in 3 seconds...')
        time.sleep(3)
        pp.pprint(f"(!!!) Retrying to get and save {iteration} time...")
        self.save_resource(url, save_path, mime, iteration=iteration + 1)

  def save_item(self, item, version, save_path):
    typename = item.get('__typename')
    save_name = f"{self.config.get('basename')}-{version}"

    if typename == "GraphImage":
      mime = "jpg"
      resource = item.get('display_url', None)
      if resource == None:
        return False
      self.save_resource(resource, f"{save_path}\\{save_name}.{mime}", mime)
      return True

    if typename == 'GraphVideo':
      mime = "mp4" if item.get('video_url', False) else 'jpg'
      resource = item.get('video_url', item.get('display_url', {}))
      if resource == None:
        return False
      self.save_resource(resource, f"{save_path}\\{save_name}.{mime}", mime)
      return True

    if typename == 'GraphSidecar':
      media = item.get('edge_sidecar_to_children', None)
      if media == None:
        # handle sidecar that requires fetching
        shortcode = item.get('shortcode')
        response = requests.get('https://www.instagram.com/graphql/query/', params={
          'query_hash': QUERIES.get('get_single_post').get('hash'),
          'variables': json.dumps({
            'shortcode': shortcode,
          })
        })
        parsed_response = response.json()
        sidecar = parsed_response.get('data', {}).get('shortcode_media', None)
        if sidecar == None:
          return False
        media = sidecar.get('edge_sidecar_to_children', None)
      nodes = media.get('edges', [])
      items = list(map(lambda node: node.get('node'), nodes))
      for index, sidecar_item in enumerate(items):
        self.save_item(sidecar_item, f"{version}.{index + 1}", save_path)
      return True

  def save(self):
    if self.__paths == None:
      self.prepare_directories()
    overall_counter = 0
    total_items = len(self.__posts) + len(self.__tagged_posts)
    pp.pprint(f"==> Saving all data...")
    if len(self.__posts) > 0:
      for index, post in enumerate(self.__posts):
        overall_counter += 1
        pp.pprint(f"- {round(overall_counter/total_items * 100, 2)}% - {overall_counter}/{total_items} items saved.")
        self.save_item(post,  index + 1, self.__paths.get('posts_path'))

    if len(self.__tagged_posts) > 0:
      for index, tagged_post in enumerate(self.__tagged_posts):
        overall_counter += 1
        pp.pprint(f"- {round(overall_counter/total_items * 100, 2)}% - {overall_counter}/{total_items} items saved.")
        self.save_item(tagged_post, index + 1, self.__paths.get('tagged_posts_path'))

    pp.pprint(f"# RESULT: {overall_counter} images and/or videos saved.")

  def save_fetched(self):
    pp.pprint(f"==> Saving fetched data...")
    if self.__paths == None:
      self.prepare_directories()
    counter = 0
    if len(self.__posts) > 0:
      file = open(f"{self.__paths.get('fetched_data_path')}\\posts.json", 'w+')
      json.dump(self.__posts, file)
      file.close()
      counter += 1
    if len(self.__tagged_posts) > 0:
      file = open(f"{self.__paths.get('fetched_data_path')}\\tagged-posts.json", 'w+')
      json.dump(self.__tagged_posts, file)
      file.close()
      counter += 1
    pp.pprint(f"# RESULT: {counter} json files with data saved.")
    

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
