from pony import orm
import datetime as dt

db = orm.Database()


class Series(db.Entity):
    ticker = orm.Required(str, unique=True)
    description = orm.Required(str)
    country = orm.Required(str)
    source = orm.Required('Source')
    observation = orm.Set('Observation')


class Observation(db.Entity):
    date = orm.Required(dt.datetime)
    obs = orm.Required(float)
    series = orm.Required(Series)


class Source(db.Entity):
    name = orm.Required(str, unique=True)
    description = orm.Required(str)
    series = orm.Set(Series)


# bootstrap db:
db.bind(provider='sqlite', filename="./database/hf_db.sqlite", create_db=True)
db.generate_mapping(create_tables=True)



