from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'selector_debrief'
    players_per_group = None
    num_rounds = 1
    employer_reward = "€2.00"
    # employer_reward_example = "€" + str(float(employer_reward[1:len(employer_reward)])*0.5)
    # if len(employer_reward_example)<5:
    #     employer_reward_example = employer_reward_example + "0"
    employer_reward_ex = "€1.00"
    referrer_punishment = "€0.70"
    referrer_neither = "€1.70"
    referrer_reward = "€2.50"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comment = models.LongStringField()
    maths_gender_accuracy = models.StringField(
        label = "Which group had a better score, on average, in the second round of the maths task: female-referred performers, or male-referred performers?",
        choices = ['Female-referred performers', 'Male-referred performers'],
        widget = widgets.RadioSelectHorizontal)
    empathy_gender_accuracy = models.StringField(
        label = "Which group had a better score, on average, in the second round of the empathy task: female-referred performers, or male-referred performers?",
        choices = ['Female-referred performers', 'Male-referred performers'],
        widget = widgets.RadioSelectHorizontal)       
    stop_epochtime = models.IntegerField()
    stop_clocktime = models.StringField()
    total_time_to_completion = models.IntegerField()


# PAGES
class referrer_accuracy(Page):
    form_model = Player
    form_fields = ['maths_gender_accuracy', 'empathy_gender_accuracy']


class end(Page):
    form_model = Player
    form_fields = ['comment']

    def is_displayed(player):
        # record time player finished application
        import time 
        time_out = round(time.time())
        player.stop_epochtime = time_out
        player.total_time_to_completion = time_out - player.participant.selector_start_epochtime
        player.stop_clocktime = time.strftime('%H:%M:%S', time.localtime(time_out))
        return True


class comment_submitted(Page):
    def is_displayed(player):
        # record time player finished application - updates the time details if they submit comment
        import time 
        time_out = round(time.time())
        player.stop_epochtime = time_out
        player.total_time_to_completion = time_out - player.participant.selector_start_epochtime
        player.stop_clocktime = time.strftime('%H:%M:%S', time.localtime(time_out))
        return 1

page_sequence = [referrer_accuracy, end, comment_submitted]
