from flask import render_template
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

    # guide page
    def guide_page(self):
        return render_template('guide.html')
