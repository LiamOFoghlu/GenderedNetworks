from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'selector_intro'
    players_per_group = None
    num_rounds = 1
    participation_fee = "£2.60"
    selector_reward = "£0.40"  # reward per decision
    num_decisions_per_task = 4
    max_reward = (2*num_decisions_per_task)*float(selector_reward[1:len(selector_reward)]) + 1   # including belief bonus
    max_reward = "£" + str(max_reward)
    if len(max_reward) == 4:
        max_reward = max_reward + "0"
    max_selection_reward = (2*num_decisions_per_task)*float(selector_reward[1:len(selector_reward)])  
    max_selection_reward = "£" + str(max_selection_reward)
    if len(max_selection_reward) == 4:
        max_selection_reward = max_selection_reward + "0"
    referrer_punishment = "£0.20"
    referrer_no_refer_bonus = "£0.50"
    referrer_neither = "£0.60"
    referrer_reward = "£0.80"
    practice_performer_a = "Jennifer"
    practice_performer_b = "William"
    practice_referrer_a = "Andrew"
    practice_referrer_b = "Rachel"
    practice_performer_score = 0.8
    sixty_percent = round(0.6*float(selector_reward[1:len(selector_reward)]), 2)
    sixty_percent = "£" + str(sixty_percent)
    if len(sixty_percent) == 4:
        sixty_percent = sixty_percent + "0"


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

    def vars_for_template(player):
        template = "_static/consent_template.html"
        return dict(
            template = template,
            study_specific = ""
        )

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
        selector_reward_num = float(Constants.selector_reward[1:len(Constants.selector_reward)])
        practice_payoff = str(round(selector_reward_num * Constants.practice_performer_score, 2))
        if len(practice_payoff) < 4:
            practice_payoff = practice_payoff + "0"
        practice_payoff = "£" + practice_payoff
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
