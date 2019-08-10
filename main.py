# libraries
import pprint

# modules
from queries import QUERIES
from user_setup import UserSetup
from scrapper import Scrapper

# init
pp = pprint.PrettyPrinter(indent=4)

# main
setup = UserSetup()
pp.pprint('[CONFIG]')
setup.load_by_user_input()

scrapper = Scrapper(setup)
pp.pprint('[SCRAPPER]')
scrapper.fetch()
scrapper.save()