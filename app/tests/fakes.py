from app.climates.models import Climate
from app.practice_centers.exceptions import PracticeCenterNotFoundException
from app.practice_centers.models import PracticeCenter
from app.recommendations.models import Recommendation
from app.sports.models import Sport
from app.sports.exceptions import SportNotFoundException

# Climates
from app.users.exceptions import UserNotFoundException
from app.users.models import User

climate1 = Climate('tundra')
climate2 = Climate('savane')
climate3 = Climate('aride')

# Sports

sport1 = Sport(sport_id=1, name='Randonnee', climates=[climate1, climate2])
sport2 = Sport(sport_id=2, name='Escalade', climates=[climate2, climate3])
sport3 = Sport(sport_id=3, name='Natation', climates=[climate3])

sport1_no_climates = Sport(sport_id=1, name='Randonnee', climates=[])
sport2_no_climates = Sport(sport_id=2, name='Escalade', climates=[])
sport3_no_climates = Sport(sport_id=3, name='Natation', climates=[])


def sports(sport_id):
    return {
        '1': sport1,
        '2': sport2,
        '3': sport3
    }[sport_id]


def no_sport():
    raise SportNotFoundException


# Practice Centers

center1 = PracticeCenter(1,
                         name='Mont-Orford National Park',
                         email='parc.mont-orford@sepaq.com',
                         web_site='https://www.sepaq.com/pq/mor/',
                         phone_number='819 843-9855',
                         climates=[climate2])
center2 = PracticeCenter(2,
                         name='Parc des Montagnards',
                         email='info@censhefford.ca',
                         web_site='https://www.cantonsdelest.com/quoi-faire/980/parc-des-montagnards',
                         climates=[])
center3 = PracticeCenter(3,
                         name='Gault Nature Reserve of McGill University',
                         climates=[climate1, climate3])


def practice_centers(practice_center_id):
    return {
        '1': center1,
        '2': center2,
        '3': center3
    }[practice_center_id]


def no_practice_center():
    raise PracticeCenterNotFoundException


# Users

user1 = User(username='fabienroy28', email='fabienroy28@gmail.com', first_name='Fabien', last_name='Roy',
             phone_number='123-456-7890')
user2 = User(username='mikaelvalliant', email='mikaelvalliant@gmail.com', first_name='Mikael', last_name='Valliant')
user3 = User(username='getoutmyswamp', email='shrek@swamp.ca', first_name='Shrek', phone_number='1 800-555-0101')


def users(username):
    return {
        'fabienroy28': user1,
        'mikaelvalliant': user2,
        'getoutmyswamp': user3
    }[username]


def no_user():
    raise UserNotFoundException


# Recommendations

sport1_recommendation1_user1 = Recommendation(1, sport1.id, user1.username, 'Un super sport. J\' adore.', 5,
                                              sport1.name)
sport2_recommendation1_user3 = Recommendation(2, sport2.id, user3.username, 'Cool.', 3, sport2.name)
sport2_recommendation2_user2 = Recommendation(3, sport2.id, user2.username, 'Pourri.', 0, sport2.name)
sport3_recommendation1_user1 = Recommendation(4, sport3.id, user1.username, ':D', 5, sport3.name)
sport1.add_recommendation(sport1_recommendation1_user1)
sport2.add_recommendation(sport2_recommendation1_user3)
sport2.add_recommendation(sport2_recommendation2_user2)
sport3.add_recommendation(sport3_recommendation1_user1)

center1_recommendation1_user1 = Recommendation(1, center1.id, user1.username, 'Un super centre. J\' adore.', 5,
                                               center1.name)
center2_recommendation1_user1 = Recommendation(2, center2.id, user1.username, 'Cool.', 3, center2.name)
center2_recommendation2_user2 = Recommendation(3, center2.id, user2.username, 'Pourri, mais bon, 2 étoiles.', 2,
                                               center2.name)
center3_recommendation1_user3 = Recommendation(4, center3.id, user3.username, ':D', 0, center3.name)
center3_recommendation2_user1 = Recommendation(5, center3.id, user1.username, 'Noice.', 4, center3.name)
center1.add_recommendation(center1_recommendation1_user1)
center2.add_recommendation(center2_recommendation1_user1)
center2.add_recommendation(center2_recommendation2_user2)
center3.add_recommendation(center3_recommendation1_user3)
center3.add_recommendation(center3_recommendation2_user1)

user1.add_sport_recommendation(sport1_recommendation1_user1)
user1.add_sport_recommendation(sport3_recommendation1_user1)
user2.add_sport_recommendation(sport2_recommendation2_user2)
user3.add_sport_recommendation(sport2_recommendation1_user3)

user1.add_practice_center_recommendation(center1_recommendation1_user1)
user1.add_practice_center_recommendation(center2_recommendation1_user1)
user1.add_practice_center_recommendation(center3_recommendation2_user1)
user2.add_practice_center_recommendation(center2_recommendation2_user2)
user3.add_practice_center_recommendation(center3_recommendation1_user3)
