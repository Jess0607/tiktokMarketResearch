from flask import Blueprint
from controllers.dashboardcontroller import DashboardController

controller = DashboardController()

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(controller.render_dashboard)