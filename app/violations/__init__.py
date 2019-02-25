from flask import Blueprint

bp = Blueprint('violations', __name__)

from app.violations import routes
