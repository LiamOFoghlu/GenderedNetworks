from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'performer_debrief'
    players_per_group = None
    num_rounds = 1
    

class Subsession(BaseSubsession):
    pass 

def creating_session(subsession):
        import random
        female_names = ["Laura", "Julia", "Sarah", "Stefanie", "Lisa", "Anna",	"Vanessa", "Sabrina"]
        male_names = ["Daniel", "Michael", "Patrick", "Lukas", "Florian", "Christian", "Andreas", "Thomas"]
        for player in subsession.get_players():
            random.shuffle(female_names)
            random.shuffle(male_names)
            choices = female_names[0:4]
            choices.extend(male_names[0:4])
            random.shuffle(choices)
            player.participant.performer_name_choices = choices
            print(player.participant.code, player.participant.performer_name_choices)



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comment = models.LongStringField()
    study_name = models.StringField()

def study_name_choices(player):
    choices = player.participant.performer_name_choices
    return choices


# PAGES
class study_name(Page):
    form_model = Player
    form_fields = ['study_name']
    
class end(Page):
    form_model = 'player'
    form_fields = [
        'comment'
                  ]

class comment_submitted(Page):
    pass


page_sequence = [study_name, end, comment_submitted]
