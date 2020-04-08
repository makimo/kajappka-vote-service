import os
from datetime import datetime

from flask import abort, Blueprint, jsonify, request, make_response
import inject # type: ignore

from .auth import AuthenticationError, get_user_id
from .repository import VotesRepository

bp = Blueprint('votes', __name__, url_prefix='/')


# XXX: Validate date format
@bp.route('/<string:date>', methods=['POST'])
@inject.autoparams()
def vote(repository: VotesRepository, date: str):
    try:
        user_id = get_user_id(request)
        game_id = request.json.get('game_id')

        is_valid, msg = _is_valid_game_id(game_id)

        if not is_valid:
            return _bad_request_response(message=msg)

        if repository.already_vote(user_id, date, game_id):
            return _bad_request_response(message='User already voted for this game')

        if repository.is_votes_limit_reached(date, user_id):
            return _bad_request_response(message='Limit of votes already reached')

        vote_obj = repository.vote(user_id, date, game_id)
        # Remove internal id from dict to reponse
        vote_obj.pop('_id')

        return jsonify(vote_obj)
    except AuthenticationError:
        abort(403)


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


def _bad_request_response(**data):
    return make_response(jsonify(**data), 400)


def _is_valid_game_id(game_id):
    if not game_id:
        return False, 'game_id is required'

    # TODO: check if game_id exists

    return True, ''
