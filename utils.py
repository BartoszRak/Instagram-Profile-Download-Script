# libraries
import os
import numpy
import urllib
import cv2
import pprint
import skimage

pp = pprint.PrettyPrinter(indent=4)

def input_true_or_false(message):
  user_answer_case_sensitive = input(message)
  user_answer = user_answer_case_sensitive.lower()
  if user_answer == 'y':
    return True
  if user_answer == 'n':
    return False
  pp.pprint('Only "y" or "n" are available as answers')
  return input_true_or_false(message)

def get_absolute_path(user_path):
  prepared_user_path = user_path.replace('/', '\\')
  path = os.getcwd()
  result_path = f"{path}\\{prepared_user_path}"
  if not os.path.exists(result_path):
    os.mkdir(result_path)
  return result_path

def get_image_from_url(url):
  image = skimage.io.imread(url)
  rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  return rgb_image