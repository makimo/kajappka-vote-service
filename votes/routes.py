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


@bp.route('/<string:date>', methods=['DELETE'])
@inject.autoparams()
def delete_vote(repository: VotesRepository, date: str):
    try:
        user_id = get_user_id(request)
        game_id = request.json.get('game_id')

        if not repository.already_vote(user_id, date, game_id):
            return _bad_request_response(
                message=f"Vote doesn't exists. Did you vote for the game at {date}?")

        repository.delete_vote(user_id, game_id, date)
        return '', 204
    except AuthenticationError:
        abort(403)
