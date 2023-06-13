from flask import render_template


class DashboardView:
    def __init__(self):
        self.empty = None

    def render_dashboard(self):
        return render_template('dashboard.html')