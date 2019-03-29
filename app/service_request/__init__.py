from flask import Blueprint

bp = Blueprint('service_request', __name__)

from app.service_request import routes
