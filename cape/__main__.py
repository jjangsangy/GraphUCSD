import logging


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

if __name__ == '__main__':
    df = run_program(32)
    to_db(df, 'cape', user=os.getlogin(), db='graphucsd')
