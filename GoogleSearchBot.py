
from selenium import webdriver,common
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class SearchBot():

    def __init__(self,entity):
        self.entity = entity
        print("===================================================")
        print("Entity Received in SearchBot---", entity)
        print("===================================================")

        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        try:
            self.driver.get("https://google.com/search?q=" + ''.join(entity))
            self.driver.maximize_window()
            print("Success")
        except:
            print("Chrome Web Driver not initialized")

class OpenResume():

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get("https://themohdomar.wordpress.com")

        self.driver.maximize_window()
        print("Successfully Opened Resume")


