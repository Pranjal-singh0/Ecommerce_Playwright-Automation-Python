# pages/base_page.py

class BasePage:
    def __init__(self, page):
        self.page = page

    def goto(self, url):
        self.page.goto(url)

    def get_title(self):
        return self.page.title()
