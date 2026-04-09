from flask import Blueprint
from flask import request
from app.controllers.etcController import calcular
from app.controllers.mainController import MainController

maincontroller = MainController()

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return maincontroller.main_page()

@bp.route('/compute')
def compute():
    return maincontroller.compute_page()

@bp.route('/test', methods=['POST'])
def test():
    return maincontroller.test_page()