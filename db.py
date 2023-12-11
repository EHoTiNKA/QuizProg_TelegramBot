from pony.orm import *

db = Database()

db.bind(provider='sqlite', filename='quizbot.db', create_db=True)

class Users(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    group = Required(str)
    results = Set('Results')


class Results(db.Entity):
    user = Required(Users)
    # test_id = Required(int)
    user_balls = Required(int)

db.generate_mapping(create_tables=True)


