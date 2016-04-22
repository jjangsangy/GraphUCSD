import logging

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from multiprocessing.dummy import Pool as ThreadPool

__all__ = (
    'run_program',
    'to_db',
    'main',
)

def run_program(threads=6):
    """
    Get all departments
    """
    logging.info('Program is Starting')
    # Get Departments
    deps  = departments()
    keys  = [department.strip() for department in deps.keys()]

    # Run Scraper Concurrently Using ThreadPool
    pool  = ThreadPool(threads)
    logging.info('Initialize Scraper with {} Threads'.format(threads))
    table = pool.map(create_table, keys)
    logging.info('Scrape Complete')

    # Manage ThreadPool
    pool.close(); pool.join()
    df = pd.concat(table)
    return df.groupby(level=0).first()


def to_db(df, table, user='postgres', db='graphucsd', resolve='replace', **kwargs):
    """
    Helper Function to Push DataFrame to Postgresql Database
    """
    url = 'postgresql+psycopg2://{user}@localhost/{db}'
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url.format(user=user, db=db))
    df.to_sql(table, engine, if_exists=resolve, **kwargs)


def main(**k):
    df = run_program(k.get('diet'), 8)
    dfk(df, k.get('db','cape'), user=os.getlogin(), db='graphucsd')


if __name__ == '__main__':
    print('Downloading')
    main()
