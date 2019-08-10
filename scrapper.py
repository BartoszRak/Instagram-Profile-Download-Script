# libraries
import pprint
pp = pprint.PrettyPrinter(indent=4)

class Scrapper:
  def __init__(self, user_setup):
    self.__user_setup = user_setup

  @property
  def user_setup(self):
    return self.__user_setup

  def start(self):
    if self.user_setup.posts == True:
      self.scrap_posts()
    if self.user_setup.tagged_posts == True:
      self.scrap_tagged_posts()

  def scrap_posts(self):
    pp.pprint('scrap posts')

  def scrap_tagged_posts(self):
    pp.pprint('scrap tagged posts')
