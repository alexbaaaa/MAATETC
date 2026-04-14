from flask import request, jsonify
from app.services.handlerETC import HandlerETC
from dataclasses import dataclass

# This decorate is provisional 
@dataclass
class EtcController:
    def getJSON(self):
        handlerETC = HandlerETC()

        return handlerETC.getElement()
