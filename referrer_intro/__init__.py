from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'referrer_intro'
    players_per_group = None
    num_rounds = 1
    participation_fee = "£1.80"
    no_refer_bonus = "£0.50"
    refer_bonus = "£0.60"
    punishment_bonus = "£0.20"
    reward_bonus = "£0.80"
    total_max_reward_bonus = 4*float(reward_bonus[1:len(reward_bonus)]) + 1 # 4 rounds
    total_max_reward_bonus = "£" + str(total_max_reward_bonus)
    if len(total_max_reward_bonus) == 4:
        total_max_reward_bonus = total_max_reward_bonus + "0"


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    start_epochtime = models.IntegerField()
    start_clocktime = models.StringField()
    ProlificID = models.StringField()
    Practice_refer = models.StringField(
        label = "",
        choices = ['Yes','No'],
        widget=widgets.RadioSelectHorizontal
    )


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

    def vars_for_template(player):
        template = "_static/consent_template.html"
        study_specific = " Anonymised information on your performance in this study may also be shown to participants in a future study."
        return dict(
            template = template,
            study_specific = study_specific,
            task = player.participant.referrer_treatment
        )

class ProlificID(Page):
    form_model = 'player'
    form_fields = ['ProlificID']

class Instructions(Page):
    def vars_for_template(player):
        if player.participant.referrer_treatment == "maths":
            task_details = "maths task. The performers had to answer several maths questions."
            task = "maths"
            avg_score = "2.5 correct answers out of 5"
        else:
            task_details = "childcare task. The performers had to read a text describing how to care for young children and then answer questions about proper childcare practices and childhood developmental stages."
            task = "childcare"
            avg_score = "2.9 correct answers out of 5"
        return dict(
            task_details = task_details,
            task = task,
            number_of_rounds = 4,
            avg_score = avg_score
        )

class Practice_referral(Page):
    form_model = 'player'
    form_fields = ['Practice_refer']

    def vars_for_template(player):
        import random
        refer_table_template = 'referrer_intro/refer_table_template.html'
        return dict(
            candidate_name = random.choice(["John","Jane"]),
            score = random.choice(list(range(1,6))),
            age = random.choice(list(range(24,30))),
            refer_table_template = refer_table_template
        )


page_sequence = [Consent, ProlificID, Instructions, Practice_referral]
