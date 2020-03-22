import os
from datetime import datetime

from flask import Blueprint, jsonify

from .votes import VotesRepository

bp = Blueprint('votes', __name__, url_prefix='/')


@bp.route('/<string:date>', methods=['GET'])
def get_votes(date: str):
    repository = VotesRepository()
    votes_count = repository.count_votes(date)
    user_votes = repository.get_user_votes(date, 1)
    response = _create_votes_count_response(votes_count, user_votes)

    return jsonify(response)


def _create_votes_count_response(votes_count: list, user_votes: set):
    response = []

    for key, value in votes_count.items():
        response.append({
            'game_id': key,
            'vote_count': value,
            'user_vote': key in user_votes
        })

    return response
