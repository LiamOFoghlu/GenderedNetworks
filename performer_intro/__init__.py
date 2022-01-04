from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'performer_intro'
    players_per_group = None
    num_rounds = 1
    participation_fee = "€3.50"
    total_reward = "€4.00"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ProlificID = models.StringField()


# PAGES
class Consent(Page):
    pass

class ProlificID(Page):
    form_model = 'player'
    form_fields = ['ProlificID']


page_sequence = [Consent, ProlificID]
