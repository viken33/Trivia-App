from flask import Blueprint
restricted_bp = Blueprint('restricted', __name__, template_folder='templates')
from . import routes