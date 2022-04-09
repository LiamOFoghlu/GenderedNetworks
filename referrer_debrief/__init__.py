import re
from otree.api import *


doc = """
Your app description
"""

class Constants(BaseConstants):
    name_in_url = 'referrer_debrief'
    players_per_group = None
    num_rounds = 1
    session_gender = "female" # toggle this between genders depending on the session


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
        import random
        # study name ==> these names are taken from the top 100 baby names in England and Wales in 1994. They are the even-ranked names (1, 3, 5, etc) -- the performer name list is the even-ranked (2, 4, 6 etc)
        if Constants.session_gender == "female":
            names = ["Charlotte", "Sophie", "Emily", "Emma", "Sarah", "Jade", "Alice", "Samantha", "Holly", "Olivia", "Elizabeth", "Natasha", "Zoe", "Eleanor", "Paige", "Gemma", "Chelsea", "Alexandra", "Jennifer", "Louise", "Jodie", "Anna", "Amber", "Kayleigh", "Harriet", "Naomi", "Abbie", "Leanne", "Rosie", "Ellie", "Kimberley", "Heather", "Helen", "Robyn", "Demi", "Gabrielle", "Lily", "Maria", "Imogen", "Caitlin", "Isabel"]
        if Constants.session_gender == "male":
            names = ["James", "Daniel", "Ryan", "Luke", "Michael", "Christopher", "Joseph", "Jake", "Andrew", "Lewis", "David", "Connor", "Harry", "Aaron", "Bradley", "Kieran", "Nicholas", "Charles", "Stephen", "Dominic", "Rhys", "Anthony", "Paul", "Jason", "Ross", "Max", "Henry", "Timothy", "Joel", "Carl", "Brandon", "Toby", "Gareth", "Christian", "Declan", "Jay", "Darren", "Frank", "Kevin", "Adrian"]        
        for player in subsession.get_players():
            random.shuffle(names)
            choices = names[0:5]
            random.shuffle(choices)
            player.participant.referrer_name_choices = choices


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comment = models.LongStringField()
    stop_epochtime = models.IntegerField()
    stop_clocktime = models.StringField()
    total_time_to_completion = models.IntegerField()
    study_name = models.StringField()

def study_name_choices(player):
    choices = player.participant.referrer_name_choices
    return choices


# PAGES
class study_name(Page):
    form_model = Player
    form_fields = ['study_name']
    
    def is_displayed(player):
        return player.participant.referrer_num_referrals > 0

    def vars_for_template(player):
        num_referrals = player.participant.referrer_num_referrals
        if num_referrals == 1:
            num_referrals = "referral"
        else:
            num_referrals = str(num_referrals) + " referrals"
        return dict(
            num_referrals = num_referrals
        )

class end(Page):
    form_model = Player
    form_fields = ['comment']

    def is_displayed(player):
        # record time player finished application
        import time 
        time_out = round(time.time())
        player.stop_epochtime = time_out
        player.total_time_to_completion = time_out - player.participant.referrer_start_epochtime
        player.stop_clocktime = time.strftime('%H:%M:%S', time.localtime(time_out))
        return 1


class comment_submitted(Page):
    def is_displayed(player):
        # record time player finished application - updates the time details if they submit comment
        import time 
        time_out = round(time.time())
        player.stop_epochtime = time_out
        player.total_time_to_completion = time_out - player.participant.referrer_start_epochtime
        player.stop_clocktime = time.strftime('%H:%M:%S', time.localtime(time_out))
        return 1

page_sequence = [study_name, end, comment_submitted]
