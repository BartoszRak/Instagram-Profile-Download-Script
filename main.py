# libraries
import pprint

# modules
from queries import QUERIES
from user_setup import UserSetup
from scrapper import Scrapper
from utils import get_image_from_url

# init
pp = pprint.PrettyPrinter(indent=4)

# main
# get_image_from_url('https://arbordayblog.org/wp-content/uploads/2018/06/oak-tree-sunset-iStock-477164218-1080x608.jpg')
setup = UserSetup()
pp.pprint('[CONFIG]')
setup.load_by_user_input()

scrapper = Scrapper(setup)
pp.pprint('[SCRAPPER]')
scrapper.fetch()
scrapper.save_fetched()
scrapper.save()