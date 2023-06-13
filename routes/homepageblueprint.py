from flask import Blueprint
from controllers.homepagecontroller import HomePageController

controller = HomePageController()

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(controller.render_home)