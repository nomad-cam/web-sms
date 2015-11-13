from flask import Flask
from flask_bootstrap import Bootstrap
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
Bootstrap(app)

import websms.views