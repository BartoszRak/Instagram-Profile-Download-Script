# libraries
import pprint

def input_true_or_false(message):
  pp = pprint.PrettyPrinter(indent=4)
  user_answer_case_sensitive = input(message)
  user_answer = user_answer_case_sensitive.lower()
  if user_answer == 'y':
    return True
  if user_answer == 'n':
    return False
  pp.pprint('Only "y" or "n" are available as answers')
  return input_true_or_false(message)