'''
    Author : Sang Han
    Year   : 2015
    License: Apache 2.0
'''
from __future__ import print_function

import requests
import sys
import logging
import string
import os

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from operator import itemgetter

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


__all__ = [
    'connect',
    'departments`',
    'to_db',
    'department',
    'geberate_table',
    'calculate_percentage',
    'calculate_grades',
    l'calculate_grades'
]

def connect(prot='http', **q):
    """
    Makes a connection with CAPE.
    Required that at least one query is made.

    Parameters
    ----------
    :params prot: Either HTTP or HTTPS
    :params    q: Query Dictionary

    Returns
    -------
    :return: Request
    :rtype : request.Request
    """
    host   = 'cape.ucsd.edu'
    inputs = 'Name', 'courseNumber', 'department'
    prot   = prot.lower()
    base   = '%s://%s/responses/Results.aspx' % (prot, host)

    assert prot in ['http', 'https']
    assert any(val in inputs for val in q)

    headers = {           "Host": host,
                        "Accept": ','.join([
                                    "text/html",
                                    "application/xhtml+xml",
                                    "application/xml;q=0.9,*/*;q=0.8"]),
               "Accept-Language": "en-US,en;q=0.5",
                    "User-Agent":  ' '.join([
                                    "Mozilla/5.0]",
                                    "(Macintosh; Intel Mac OS X 10_10_2)",
                                    "AppleWebKit/600.3.18",
                                    "(KHTML, like Gecko)",
                                    "Version/8.0.3 Safari/600.3.18"]),
                 "Cache-Control": "no-cache"
    }
    queries = '&'.join(
        [
            '{key}={value}'.format(key=key, value=value)
                for key, value in q.items()
                if  key in inputs
        ]
    )
    req = requests.get('?'.join([base, queries]), headers=headers)

    if not req.ok:
        print("Request didn't make it", file=sys.stderr)
        req.raise_for_status()

    return req

def departments():
    """
    Gets a mapping of all the deparments by key.
    """
    logging.info('Grabbing a list of Departments')
    prototype = connect("http", department="CHEM")
    soup      = BeautifulSoup(prototype.content, 'lxml')
    options   = list(reversed(soup.find_all('option')))

    options.pop()

    # Initial Course Mapping
    mapping = dict(option.text.split(' - ') for option in options)

    # Cleanup
    for dept in ['BIOL', 'SOC', 'HIST', 'LING', 'LIT', 'NENG', 'RSM ', 'SOE', 'THEA']:
        mapping.pop(dept)

    # Actual Departments
    mapping.update({
        'BIBC': 'Biology Biochemistry',
        'BILD': 'Biology Lower Division',
        'BIMM': 'Biology Molecular, Microbiology',
        'BIPN': 'Biology Physiology and Neuroscience',
        'SOCA': 'Sociology Theory & Methods',
        'SOCB': 'Sociology Cult, Lang, & Soc Interact',
        'SOCC': 'Sociology Organiz & Institutions',
        'SOCD': 'Sociology Comparative & Historical',
        'SOCE': 'Sociology Ind Research & Honors Prog',
        'SOCI': 'Sociology',
        'SOCL': 'Sociology Lower Division',
        'HILD': 'History Lower Division',
        'HIAF': 'History of Africa',
        'HIEA': 'History of East Asia',
        'HIEU': 'History of Europe',
        'HINE': 'History of Near East',
        'HILA': 'History of Latin America',
        'HISC': 'History of Science',
        'HIUS': 'History of the United States',
        'HITO': 'History Topics',
        'LTAF': 'Literature African',
        'LTAM': 'Literature of the Americas',
        'LTCH': 'Literature Chinese',
        'LTCS': 'Literature Cultural Studies',
        'LTEA': 'Literature East Asian',
        'LTEU': 'Literature European/Eurasian',
        'LTFR': 'Literature French',
        'LTGM': 'Literature General',
        'LTGK': 'Literature Greek',
        'LTGM': 'Literature German',
        'LTIT': 'Literature Italian',
        'LTKO': 'Literature Korean',
        'LTLA': 'Literature Latin',
        'LTRU': 'Literature Russian',
        'LTSP': 'Literature Spanish',
        'LTTH': 'Literature Theory',
        'LTWL': 'Literature of the World',
        'LTWR': 'Literature Writing',
        'RELI': 'Literature Study of Religion',
        'TWS' : 'Literature Third World Studies',
        'NANO': 'Nano Engineering',
        'MGT' : 'Rady School of Management',
        'ENG' : 'Jacobs School of Engineering',
        'LIGN': 'Linguistics',
        'TDAC': 'Theatre Acting',
        'TDCH': 'Theatre Dance Choreography',
        'TDDE': 'Theatre Design',
        'TDDR': 'Theatre Directing/Stage Management',
        'TDGE': 'Theatre General',
        'TDHD': 'Theatre Dance History',
        'TDHT': 'Theatre History',
        'TDMV': 'Theatre Dance Movement',
        'TDPF': 'Theatre Dance Performance',
        'TDPW': 'Theatre Playwriting',
        'TDTR': 'Theatre Dance Theory',
    })

    # Create Categorical Series
    dep = pd.Series(name='department_name', data=mapping)

    # Reindexing
    dep = dep.map(lambda x: np.nan if x == '' else x)
    dep = dep.dropna()
    dep.index.name = 'Departments'

    return dep


def calculate_percentage(element):
    if isinstance(element, str):
        return np.float(element.strip('%').strip()) / 100
    else:
        return np.nan

def calculate_grades(element):
    if isinstance(element, str):
        return np.float(element[1:].lstrip('+-').lstrip().strip('()'))
    else:
        return np.nan

def calculate_section_id(element):
    if isinstance(element, str):
        return int(element.lower().rsplit('sectionid=')[-1].strip(string.ascii_letters))
    else:
        return np.nan


def create_table(courses):
    """
    Generates a pandas DataFrame by querying UCSD Cape Website.

    Parameters
    ==========
    :params courses: Either Course or Path to HTML File

    Returns
    =======
    :returns df:     Query Results
    :rtype:          pandas.DataFrame
    """
    header = [
        'instructor', 'course', 'term', 'enroll', 'evals',
        'recommend_class', 'recommend_instructor', 'study_hours_per_week',
        'average_grade_expected', 'average_grade_received'
    ]
    first, second = itemgetter(0), itemgetter(1)

    print('\nGrabbing Classes: {0}'.format(courses))

    # Get Data
    base  = 'http://cape.ucsd.edu/responses/'
    req   =  (
                open(courses).read()
                if   os.path.isfile(courses)
                else connect("http", courseNumber=courses).content
            )
    html  = BeautifulSoup(req, 'lxml')
    table = first(html.find_all('table'))

    # Create Dataframe
    df    = first(pd.read_html(str(table)), flavor=None, na_values=['No CAPEs submitted'])

    # Data Clean Up
    df.columns = header
    df['link']       = [
        urljoin(base, link.attrs['href']) if link.has_attr('href') else np.nan
            for link in table.find_all('a')
    ]
    df['instructor'] = df.instructor.map(
        lambda name: (
            str.title(name)
            if isinstance(name, str) else 'Unknown, Unknonwn'
        )
    )
    # Data Extraction
    df['first_name']  = df.instructor.map(lambda name:  second(name.split(',')).strip('.'))
    df['last_name']   = df.instructor.map(lambda name:   first(name.split(',')))
    df['class_id']    = df.course.map(  lambda course: first(course.split(' - ')))
    df['department']  = df.class_id.map(lambda course:  first(course.split(' ')))
    df['class_name']  = df.course.map(
        lambda course: (
            second(course.split(' - '))[:-4]
            if ' - ' in course else np.nan)
    )
    # Data Types
    df['recommend_class']        = df.recommend_class.map(calculate_percentage)
    df['recommend_instructor']   = df.recommend_instructor.map(calculate_percentage)
    df['average_grade_expected'] = df.average_grade_expected.map(calculate_grades)
    df['average_grade_received'] = df.average_grade_received.map(calculate_grades)

    # Reindexing and Transforms
    df['section_id'] = df.link.map(calculate_section_id)
    df = df.dropna(subset=['section_id'])
    df = df.drop_duplicates(subset='section_id')
    df['section_id'] = df.section_id.astype(np.int32)

    return df.set_index('section_id', drop=True)

