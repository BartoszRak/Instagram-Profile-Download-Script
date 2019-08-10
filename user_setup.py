from utils import input_true_or_false

class UserSetup:
  profile_name = None
  posts = None
  tagged_posts = None

  def load_by_user_input(self):
    self.profile_name = input('1. Instagram profile name?: ')
    self.posts = input_true_or_false('2. Do you want posts to be downloaded? [y/n]: ')
    self.profile_name = input_true_or_false('3. Do you want tagged posts to be downloaded? [y/n]: ')
