# libraries
import requests

# modules
from utils import input_true_or_false

class UserSetup:
  __profile_name = None
  __profile_id = None
  __posts = None
  __tagged_posts = None

  def get_id_from_profile_html(self, response):
    search = 'profilePage_'
    profile_text = response.text
    id_index = profile_text.find(search)
    text_started_with_id = profile_text[id_index + len(search):]
    return text_started_with_id[:text_started_with_id.find('"')]

  def load_by_user_input(self):
    self.__profile_name = input('1. Instagram profile name?: ')
    self.__posts = input_true_or_false('2. Do you want posts to be downloaded? [y/n]: ')
    self.__tagged_posts = input_true_or_false('3. Do you want tagged posts to be downloaded? [y/n]: ')
    html = requests.get(f"https://www.instagram.com/{self.profile_name}")
    self.__profile_id = self.get_id_from_profile_html(html)


  @property
  def profile_name(self):
    return self.__profile_name

  @property
  def profile_id(self):
    return self.__profile_id

  @property
  def posts(self):
    return self.__posts

  @property
  def tagged_posts(self):
    return self.__tagged_posts
