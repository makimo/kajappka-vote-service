from .database import votes_coll


class VotesRepository:
    # XXX: Move to settings?
    VOTE_LIMIT = 3

    def get_votes_by_date(self, date: str):
        return votes_coll.find({'date': date})

    def count_votes(self, date: str):
        votes = self.get_votes_by_date(date)
        votes_count = {}

        for vote in votes:
            key = vote['game_id']
            votes_count.setdefault(key, 0)
            votes_count[key] += 1

        return votes_count

    def get_user_votes(self, date: str, user_id: int):
        votes = self.get_votes_by_date(date)
        user_votes = set()

        for vote in votes:
            if vote['user_id'] == user_id:
                user_votes.add(vote['game_id'])

        return user_votes

    def delete_vote(self, user_id: int, game_id: str, date: str) -> None:
        query = {"user_id": user_id, "game_id": game_id, "date": date}
        votes_coll.delete_one(query)

    def is_votes_limit_reached(self, date: str, user_id: int):
        voutes_count = len(votes_coll.find({
            'user_id': user_id,
            'date': date
        }).distinct('game_id'))

        return  voutes_count >= self.VOTE_LIMIT

    def already_vote(self, user_id: int, date: str, game_id: str):
        return votes_coll.find_one({
            'user_id': user_id,
            'game_id': game_id,
            'date': date
        }) != None

    def vote(self, user_id: int, date: str, game_id: str):
        obj = {
            'user_id': user_id,
            'game_id': game_id,
            'date': date
        }

        votes_coll.insert_one(obj)

        return obj
