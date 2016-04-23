import os

import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from multiprocessing.dummy import Pool as ThreadPool

from . utils import get_departments
from . scrape import create_table


class CAPECrawler:
    """
    Concrete implementation of a crawler
    """
    def __init__(self, max_threads=32):
        self.max_threads = max_threads

    def run(self):
        """
        Get all departments
        """
        # Get Departments
        deps  = get_departments()
        keys  = [department.strip() for department in deps.keys()]

        # Run Scraper Concurrently Using ThreadPool
        pool  = ThreadPool(self.max_threads)
        table = pool.map(create_table, keys)

        pool.close()
        pool.join()

        return pd.concat(table).groupby(level=0).first()

    def to_df(self):
        return self.collect()

    def get_engine(self, url):

        if not database_exists(url):
            create_database(url)

        return create_engine(url)

    def to_db(self, table, user='postgres', db='graphucsd', resolve='replace', **kwargs):
        """
        Helper databasse exporter for Postgres
        """
        url = 'postgresql+psycopg2://{user}@localhost/{db}'.format(
            user=user, db=db
        )
        engine = self.get_engine(url)
        self.df.to_sql(
            table, engine,
            if_exists=resolve,
            **kwargs
        )


def main(**k):
    crawlerk = CAPECrawler(max_threads=os.env.get(''))

    to_db(df, k.get('db', 'capee'),
        user=os.getlogin(),
        db=k.get('DBNAME', 'UCSDCape'),
    )


if __name__ == '__main__':
    print("Starting the Crawl")
    main(**os.envs)
