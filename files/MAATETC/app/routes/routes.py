from flask import Blueprint
from flask import request
from app.controllers.etcController import getJSON
from app.controllers.mainController import MainController

maincontroller = MainController()
etcController = EtcController()

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return maincontroller.main_page()

@bp.route('/compute')
def compute():
    return maincontroller.compute_page()

@bp.route('/etc')
def etc():
    return etcController.getJSON()



# Rutas de pruebas
@bp.route('/test', methods=['POST'])
def test():
    return maincontroller.test_page()

@bp.route('/testAjax', methods=['POST'])
def ajax():
    return maincontroller.test_ajax()