from flask import request, session
from views.homepageview import HomePageView

class HomePageController:
    def __init__(self):
        self.view = HomePageView()

    def render_home(self):
        session.permanent = True
        return self.view.render_home()
