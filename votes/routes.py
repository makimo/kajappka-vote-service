import os
from datetime import datetime

from flask import abort, Blueprint, jsonify, request
import inject # type: ignore

from .auth import AuthenticationError, get_user_id
from .repository import VotesRepository

bp = Blueprint('votes', __name__, url_prefix='/')


@bp.route('/<string:date>', methods=['GET'])
@inject.autoparams()
def get_votes(repository: VotesRepository, date: str):
    try:
        user_id = get_user_id(request)

        votes_count = repository.count_votes(date)
        user_votes = repository.get_user_votes(date, user_id)
        response = _create_votes_count_response(votes_count, user_votes)

        return jsonify(response)
    except AuthenticationError:
        abort(403)


def _create_votes_count_response(votes_count: list, user_votes: set):
    response = []

    for key, value in votes_count.items():
        response.append({
            'game_id': key,
            'vote_count': value,
            'user_vote': key in user_votes
        })

    return response
