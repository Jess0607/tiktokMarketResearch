from flask import Blueprint
from controllers.controller import Controller

controller = Controller()

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(controller.render_home)
blueprint.route('/upload', methods=['GET'])(controller.upload_next_video)
blueprint.route('/uploading_video', methods=['POST', 'GET'])(controller.uploading_video)
blueprint.route('/transcribe', methods=['GET'])(controller.transcribe_next_video)
blueprint.route('/transcribing_video', methods=['GET'])(controller.transcribing_video)
blueprint.route('/finished', methods=['GET'])(controller.finished)