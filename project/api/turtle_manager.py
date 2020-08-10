from os import getenv
from dateutil.relativedelta import relativedelta
from datetime import datetime

import pandas as pd

import pyarrow as pa

from project.api.metrics import timing

CHUNKSIZE = 1000
URL = 'https://s3-us-west-2.amazonaws.com/cool-turtles/turtles.csv'
ALL_TURTLES = 'all_turtles_5'
PERIOD_YEAR = 'period_year_12'
PERIOD_START_TO_END = 'period_start_to_end_2'
REDIS_EXPIRE = 604800  # one week


class Turtle_Manager():
    def __init__(self, redis):

        self.context = pa.default_serialization_context()
        self.redis = redis
        self.df_all = None

        # TODO refactor redis pattern
        if not redis.exists(ALL_TURTLES):
            print("Loading Turtles from file")
            self.df_all = self.get_df_all()
            redis.set(ALL_TURTLES, self.context.serialize(self.df_all).to_buffer().to_pybytes())
            redis.expire(ALL_TURTLES, REDIS_EXPIRE)
        else:
            print("Loading Turtles from Redis")
            self.df_all = self.context.deserialize(redis.get(ALL_TURTLES))

    @timing
    def get_df_all(self):
        location = getenv('csv_location', URL)
        # TODO logging
        print("Reading from", location)
        reader = pd.read_csv(location, chunksize=CHUNKSIZE, iterator=True)
        df = pd.concat(reader, ignore_index=True)
        df = df[df['Weight'] != 0]
        df = df[df['Carapace'] != 0]
        df = df[df['Plastron'] != 0]
        df = df[df['Species'] == 'Cpb']
        # df['Month'] = df.Date.map(lambda x: x.strftime('%B'))
        df.Date = pd.to_datetime(df.Date)
        df['Month'] = df.Date.map(lambda x: x.month)
        df['Year'] = df.Date.map(lambda x: x.year)
        df.Gravid = df.Gravid.map({True: 'Y', False: ''})
        latLong = {
            'Mason Flats': ('45.520933', '-122.674101'),
            'Whitaker Ponds': ('45.573749', '-122.613542'),
            'Gresham': ('45.507347', '-122.433480'),
        }
        df['lat'] = df['Capture Location'].map(lambda x: latLong[x][0]).astype('float32')
        df['long'] = df['Capture Location'].map(lambda x: latLong[x][1]).astype('float32')
        return df

    def _get_count_per_period_and_year(self, period='M', locations=[]):
        df = self.df_all.copy()
        if len(locations) > 0:
            df = df[df['Capture Location'].isin(locations)]
        print("data service count ", df.shape)
        if period == 'M':
            df['Period'] = df.Date.map(lambda x: x.month_name())
        elif period == 'Q':
            df['Period'] = df.Date.map(lambda x: 'Q' + str(x.quarter))
        elif period == 'S':
            df['Period'] = df.Date.dt.month.map(lambda x: 'Early' if x < 9 else 'Late')
        df = df[['Period', 'Year', 'ID']].sort_values('Period').copy()
        df = df.groupby(['Period', 'Year']).count().reset_index()
        df.columns = ['Period', 'Year', 'Count']
        return df

    @timing
    def get_count_per_period_and_year(self, period='M', locations=[]):

        # TODO refactor redis pattern
        locations.sort()
        redisKey = PERIOD_YEAR + period + str(locations)
        if not self.redis.exists(redisKey):
            print(f"REBUILD Count Per {period} and year, locationfilter {locations}")
            try:
                df = self._get_count_per_period_and_year(period, locations)
            except KeyError:
                raise ValueError(f"Invalid period {period}")
            self.redis.set(redisKey, self.context.serialize(df).to_buffer().to_pybytes())
            self.redis.expire(redisKey, REDIS_EXPIRE)
            return df
        else:
            print(f"FROM REDIS Count Per {period} and year, locationfilter {locations}")
            return self.context.deserialize(self.redis.get(redisKey))

    def _get_periodStart_to_endDate(self, period, endDate):
        df = self.df_all.sort_values('Date').copy()
        endDate = datetime.strptime(endDate, '%Y-%m-%d')
        startDate = None
        if period == 'D':
            startDate = str(endDate - relativedelta(days=1))
        if period == 'W':
            startDate = str(endDate - relativedelta(weeks=1))
        if period == 'M':
            startDate = str(endDate - relativedelta(months=1))
        if period == 'Q':
            startDate = str(endDate - relativedelta(months=4))
        if period == 'A':
            startDate = str(endDate - relativedelta(years=1))
        if not startDate:
            raise ValueError(f"Invalid period {period}")
        return df[(df['Date'] > startDate) & (df['Date'] <= endDate)]

    @timing
    def get_periodStart_to_endDate(self, period='M', endDate='2012-06-30'):

        # TODO refactor redis pattern
        redisKey = PERIOD_START_TO_END + period + endDate
        if not self.redis.exists(redisKey):
            print(f"Rebuild data by period and start to end date {period} {endDate}")
            df = self._get_periodStart_to_endDate(period, endDate)
            self.redis.set(redisKey, self.context.serialize(df).to_buffer().to_pybytes())
            self.redis.expire(redisKey, REDIS_EXPIRE)
            return df
        else:
            print("Loading period start to end date from Redis: ", redisKey)
            return self.context.deserialize(self.redis.get(redisKey))


if __name__ == '__main__':
    import os
    from redis import from_url as redis_from_url

    redis = redis_from_url(os.environ.get("REDIS_URL"))
    tm = Turtle_Manager(redis)
    df = tm.df_all
