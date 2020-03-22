from flask import Blueprint, jsonify


bp = Blueprint('votes', __name__, url_prefix='/')


@bp.route('/<string:date>', methods=['GET'])
def get_votes(date: str):
    return jsonify(
        test="test",
    )
