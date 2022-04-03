from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'performer_intro'
    players_per_group = None
    num_rounds = 1
    participation_fee = "£3.25"
    total_reward = "£4.00"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    start_epochtime = models.IntegerField()
    start_clocktime = models.StringField()
    ProlificID = models.StringField()


# PAGES
class Consent(Page):
    def is_displayed(player):
        # record time player entered application
        import time 
        time_in = round(time.time())
        player.start_epochtime = time_in
        player.participant.performer_start_epochtime = time_in
        player.start_clocktime = time.strftime('%H:%M:%S', time.localtime(time_in))
        return 1

    def vars_for_template(player):
        template = "_static/consent_template.html"
        study_specific = " Anonymised information on your performance in this study may also be shown to participants in a future study."
        return dict(
            template = template,
            study_specific = study_specific
        )


class ProlificID(Page):
    form_model = 'player'
    form_fields = ['ProlificID']

class Introduction(Page):
    def vars_for_template(player):
        task_order = player.participant.performer_task_order
        if task_order == 1:
            template = "performer_intro/intro_maths_first.html"
        else:
            template = "performer_intro/intro_childcare_first.html"
        return dict(
            template = template,
        )

page_sequence = [Consent, ProlificID, Introduction]
