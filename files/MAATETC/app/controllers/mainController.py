from flask import request, jsonify
from flask import render_template
from flask import request

# Controlador de los templates
# index page
def main_page():
    return render_template('index.html')
# compute page
def compute_page():
    return render_template('compute.html')
# Test page
def test_page(request):
    return render_template('test.html',names = request.form)