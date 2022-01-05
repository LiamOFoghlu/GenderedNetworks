from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'referrer_intro'
    players_per_group = None
    num_rounds = 1
    participation_fee = "€2.50"
    no_refer_bonus = "€1.00"
    refer_bonus = "€1.25"
    punishment_bonus = "€0.90"
    reward_bonus = "€1.50"


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    start_epochtime = models.IntegerField()
    start_clocktime = models.StringField()
    ProlificID = models.StringField()
    Refer = models.StringField(label = "",
    choices = ['Yes','No'],
    widget=widgets.RadioSelectHorizontal)


# PAGES
class Consent(Page):
    def is_displayed(player):
        # record time player entered application
        import time 
        time_in = round(time.time())
        player.start_epochtime = time_in
        player.participant.referrer_start_epochtime = time_in
        player.start_clocktime = time.strftime('%H:%M:%S', time.localtime(time_in))
        return 1

class ProlificID(Page):
    form_model = 'player'
    form_fields = ['ProlificID']

class Instructions(Page):
    pass

class Practice_referral(Page):
    form_model = 'player'
    form_fields = ['Refer']

    def vars_for_template(player):
        import random
        refer_table_template = 'referrer_intro/refer_table_template.html'
        return dict(
            candidate_name = random.choice(["Ulrika","Ulrich"]),
            score = random.choice(list(range(10,90))),
            education = random.choice(["University","Gymnasium"]),
            age = random.choice(list(range(20,30))),
            refer_table_template = refer_table_template
        )


page_sequence = [Consent, ProlificID, Instructions, Practice_referral]
