
from selenium import webdriver,common
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class SearchBot():

    def __init__(self,entity):
        self.entity = entity
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get("https://google.com/search?q=" + ''.join(entity))

        self.driver.maximize_window()
        print("Success")


#Entity = input("Who do you want to search for?")

#Bot = SearchBot(Entity)
