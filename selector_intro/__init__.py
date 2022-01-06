from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'selector_intro'
    players_per_group = None
    num_rounds = 1
    participation_fee = "€3.50"
    employer_reward = "€0.50"
    max_reward = 4*float(employer_reward[1:len(employer_reward)])   # assuming 4 rounds
    max_reward = "€" + str(max_reward)
    if len(max_reward) == 4:
        max_reward = max_reward + "0"
    referrer_punishment = "€0.90"
    referrer_no_refer_bonus = "€1.00"
    referrer_neither = "€1.25"
    referrer_reward = "€1.50"
    practice_performer_a = "Jenni"
    practice_performer_b = "Ulrich"
    practice_referrer_a = "Andreas"
    practice_referrer_b = "Ulrika"
    practice_performer_score = 0.5
    fifty_percent = 0.5*float(employer_reward[1:len(employer_reward)])
    fifty_percent = "€" + str(fifty_percent)
    if len(fifty_percent) == 4:
        fifty_percent = fifty_percent + "0"


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    start_epochtime = models.IntegerField()
    start_clocktime = models.StringField()
    ProlificID = models.StringField()
    select = models.StringField(label = "",
    choices = ['Performer A','Performer B'],
    widget=widgets.RadioSelectHorizontal)
    referrer_feedback = models.StringField(label = "",
    choices = ['Increase referrer payoff','Decrease referrer payoff', 'Do not change referrer payoff'],
    widget=widgets.RadioSelectHorizontal)


# PAGES
class Consent(Page):
    def is_displayed(player):
        # record time player entered application
        import time 
        time_in = round(time.time())
        player.start_epochtime = time_in
        player.participant.selector_start_epochtime = time_in
        player.start_clocktime = time.strftime('%H:%M:%S', time.localtime(time_in))
        return 1

class ProlificID(Page):
    form_model = 'player'
    form_fields = ['ProlificID']

class Instructions(Page):
    pass 

class Practice_select(Page):
    form_model = 'player'
    form_fields = ['select']

class Practice_feedback(Page):
    form_model = 'player'
    form_fields = ['referrer_feedback']

    def vars_for_template(player):
        employer_reward_num = float(Constants.employer_reward[1:len(Constants.employer_reward)])
        practice_payoff = str(employer_reward_num * Constants.practice_performer_score)
        if len(practice_payoff) < 4:
            practice_payoff = practice_payoff + "0"
        practice_payoff = "€" + practice_payoff
        practice_performer_score = str(round(Constants.practice_performer_score*100)) + "%"
        if player.select == "Performer A":
            performer_name = Constants.practice_performer_a
            performer_letter = "Performer A"
            referrer_name = Constants.practice_referrer_a
        else:
            performer_name = Constants.practice_performer_b
            performer_letter = "Performer B"
            referrer_name = Constants.practice_referrer_b
        return dict(
                performer_name = performer_name,
                performer_letter = performer_letter,
                referrer_name = referrer_name,
                practice_payoff = practice_payoff,
                practice_performer_score = practice_performer_score
        )



page_sequence = [Consent, ProlificID, Instructions, Practice_select, Practice_feedback]
