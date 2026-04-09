from flask import request, jsonify
from flask import render_template
from flask import request
from dataclasses import dataclass

# This decorate is provisional 
# Very importan "self"
@dataclass
class MainController:
    # index page
    def main_page(self):
        return render_template('index.html')
    # compute page
    def compute_page(self):
        return render_template('compute.html')
    # Test page
    def test_page(self):
        return render_template('test.html',names = request.form)