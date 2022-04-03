from otree.api import *


doc = """
Your app description
"""

class Constants(BaseConstants):
    name_in_url = 'referrer_debrief'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
        import random
        female_names = ["Lauren", "Charlotte", "Sophie", "Emily", "Sarah", "Katie", "Jade", "Alice"]
        male_names = ["James", "Daniel", "Ryan", "Luke", "Jordan", "Michael", "Christopher", "Joseph"]        
        for player in subsession.get_players():
            random.shuffle(female_names)
            random.shuffle(male_names)
            choices = female_names[0:5]
            choices.extend(male_names[0:5])
            random.shuffle(choices)
            player.participant.referrer_name_choices = choices
            print(player.participant.code, player.participant.referrer_name_choices)



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comment = models.LongStringField()
    stop_epochtime = models.IntegerField()
    stop_clocktime = models.StringField()
    total_time_to_completion = models.IntegerField()
    childcare_r = models.IntegerField()
    maths_r = models.IntegerField()
    study_name = models.StringField()

def study_name_choices(player):
    choices = player.participant.referrer_name_choices
    return choices


# PAGES
class study_name(Page):
    form_model = Player
    form_fields = ['study_name']
    
    def is_displayed(player):
        any_referral = player.participant.referrer_any_referral
        return any_referral


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
        player.childcare_r = player.participant.referrer_childcare_r
        player.maths_r = player.participant.referrer_maths_r
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
