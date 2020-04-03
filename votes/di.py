import inject # type: ignore

from votes.repository import VotesRepository


def my_config(binder):
    binder.bind(VotesRepository, VotesRepository())


inject.configure(my_config)
