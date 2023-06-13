from flask import request, session
from views.dashboardview import DashboardView

class DashboardController:
    def __init__(self):
        self.view = DashboardView()

    def render_dashboard(self):
        return self.view.render_dashboard()
