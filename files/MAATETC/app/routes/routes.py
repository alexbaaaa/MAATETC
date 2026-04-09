from flask import Blueprint
from flask import request
from app.controllers.etcController import calcular
from app.controllers.mainController import main_page
from app.controllers.mainController import compute_page
from app.controllers.mainController import test_page

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return main_page()

@bp.route('/compute')
def compute():
    return compute_page()

@bp.route('/test', methods=['POST'])
def test():
    return test_page(request)