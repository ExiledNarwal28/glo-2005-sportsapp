# TODO : Delete this outdated file

import sys
import os

print('Creating database tables for SportsApp...')

if os.path.abspath(os.curdir) not in sys.path:
    print('...missing directory in PYTHONPATH... added!')
    sys.path.append(os.path.abspath(os.curdir))

from project import db
from project.models import User, Sport, PracticeCenter, PracticeCenterRecommendations

db.drop_all()

db.create_all()

user1 = User(username='fabienroy28', email='fabienroy28@gmail.com', plaintext_password='12341234')
user2 = User(username='test123', email='test123@hotmail.ca', plaintext_password='password')
db.session.add(user1)
db.session.add(user2)

db.session.commit()

sport1 = Sport(name='Randonnee')
sport2 = Sport(name='Escalade')
sport3 = Sport(name='Natation')
db.session.add(sport1)
db.session.add(sport2)
db.session.add(sport3)

db.session.commit()

center1 = PracticeCenter(name='Mont-Orford National Park',
                         email='parc.mont-orford@sepaq.com',
                         web_site='https://www.sepaq.com/pq/mor/',
                         phone_number='819 843-9855')
center2 = PracticeCenter(name='Parc des Montagnards',
                         email='info@censhefford.ca',
                         web_site='https://www.cantonsdelest.com/quoi-faire/980/parc-des-montagnards')
center3 = PracticeCenter(name='Gault Nature Reserve of McGill University')
db.session.add(center1)
db.session.add(center2)
db.session.add(center3)

db.session.commit()

# TODO : Add Practice Center recommandations
'''
practice_center_recommendation1 = PracticeCenterRecommendations(username='fabienroy28',
                                                                id_practice_center='abcd1234',
                                                                comment='Pas pire pantoute',
                                                                date=datetime.date(2020, 2, 20),
                                                                note=7
                                                                )

practice_center_recommendation2 = PracticeCenterRecommendations(username='mikmik123',
                                                                id_practice_center='3456defg',
                                                                comment='Good job les boys',
                                                                date=datetime.date(2020, 1, 12),
                                                                note=8
                                                                )

db.session.add(practice_center_recommendation1)

db.session.commit()
'''

print('...done!')
