from .database import votes_coll


class VotesRepository:
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
