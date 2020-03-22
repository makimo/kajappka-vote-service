import json
import os
import requests

from flask import Blueprint, jsonify


class AuthenticationError(Exception):
    pass


def get_user_id(request):
    auth_url = os.environ['AUTH_URL']

    token = request.headers.get('Authorization')
    headers = {'Authorization': token}

    response = requests.get(auth_url)

    if response.status_code == 200:
        return json.loads(response.text)['id']

    raise AuthenticationError


auth_bp = Blueprint('mock_auth', __name__, url_prefix='/mock-auth')


@auth_bp.route('/token-response', methods=['GET'])
def mock_auth():
    return jsonify(id=1)
