from flask import request, jsonify
import io, base64
from dataclasses import dataclass
from app.services.etc.maatetc_gui import run_etc

@dataclass
class HandlerETC:
    @staticmethod
    def getElement( element, fig):
        data = {
            'element': element,
            'figure': fig
        }
        return data
    @staticmethod
    def runEtc(values):
        text_elem = Dummy()

        fig, text_elem = run_etc(values, text_elem, None)

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)

        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        resultJson = {
            "imagen": img_base64,
            "text" : text_elem.value
        }
        return resultJson
    
#Esta clase la estrere mas adelante
class Dummy:
    def __init__(self):
        self.value = ""

    def update(self, value):
        self.value = value
    def to_dict(self):
        return {"value": self.value}