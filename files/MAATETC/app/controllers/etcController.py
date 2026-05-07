from flask import request, jsonify
from app.services.handlerETC import HandlerETC
from dataclasses import dataclass

# This decorate is provisional 
@dataclass
class EtcController:
    def getJSON(self):
        data = HandlerETC.runEtc(request.get_json())
        return jsonify(data)
    
    def getGratings(self):
        gratings = HandlerETC.getGrating()
        return jsonify(gratings)
