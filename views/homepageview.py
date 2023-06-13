from flask import render_template

class HomePageView:
    def __init__(self):
        self.empty = None

    def render_home(self):
        return render_template('homepage.html')