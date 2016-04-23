
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

from . import scrape


def get_departments():
    """
    Gets a mapping of all the deparments by key.
    """
    prototype = scrape.connect("http", department="CHEM")
    soup      = BeautifulSoup(prototype.content, 'lxml')
    options   = list(reversed(soup.find_all('option')))

    options.pop()

    mapping = dict(option.text.split(' - ') for option in options)
    for dept in ['BIOL', 'SOC', 'HIST', 'LING', 'LIT', 'NENG', 'RSM ', 'SOE', 'THEA']:
        mapping.pop(dept)

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
    dep = pd.Series(name='department_name', data=mapping)
    dep = dep.map(lambda x: np.nan if x == '' else x)
    dep = dep.dropna()
    dep.index.name = 'Departments'
    return dep

