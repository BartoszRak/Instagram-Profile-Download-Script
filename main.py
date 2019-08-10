# libraries
import pprint

# modules
from queries import QUERIES
from user_setup import UserSetup

# init
pp = pprint.PrettyPrinter(indent=4)

# main
pp.pprint(QUERIES)
user_setup = UserSetup()
user_setup.load_by_user_input()