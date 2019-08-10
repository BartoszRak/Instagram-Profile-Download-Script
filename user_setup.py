from utils import input_true_or_false

class UserSetup:
  __profile_name = None
  __posts = None
  __tagged_posts = None

  def load_by_user_input(self):
    self.__profile_name = input('1. Instagram profile name?: ')
    self.__posts = input_true_or_false('2. Do you want posts to be downloaded? [y/n]: ')
    self.__tagged_posts = input_true_or_false('3. Do you want tagged posts to be downloaded? [y/n]: ')

  @property
  def profile_name(self):
    return self.__profile_name

  @property
  def posts(self):
    return self.__posts

  @property
  def tagged_posts(self):
    return self.__tagged_posts
