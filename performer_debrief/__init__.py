from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'performer_debrief'
    players_per_group = None
    num_rounds = 1
    session_gender = "male" # toggle this between genders depending on the session
    

class Subsession(BaseSubsession):
    pass 

def creating_session(subsession):
        import random

        # study name ==> these names are taken from the top 100 baby names in England and Wales in 1994. They are the odd-ranked names (1, 3, 5, etc) -- the referrer name list is the even-ranked (2, 4, 6 etc)
        if Constants.session_gender == "female":
            names = ["Rebecca", "Jessica", "Hannah", "Amy", "Laura", "Chloe", "Lucy", "Bethany", "Megan", "Rachel", "Danielle", "Abigail", "Stephanie", "Victoria", "Georgia", "Natalie", "Shannon", "Nicole", "Kirsty", "Melissa", "Hayley", "Catherine", "Grace", "Molly", "Jasmine", "Kelly", "Leah", "Francesca", "Kate", "Claire", "Sian", "Lydia", "Stacey", "Amelia", "Lisa", "Chantelle", "Daisy", "Rhiannon", "Joanna", "Phoebe"]
        if Constants.session_gender == "male":
            names = ["Thomas", "Jack", "Matthew", "Joshua", "Samuel", "Adam", "Alexander", "Benjamin", "William", "George", "Oliver", "Robert", "Nathan", "Jonathan", "Callum", "Jacob", "Scott", "John", "Kyle", "Mark", "Edward", "Richard", "Peter", "Lee", "Craig", "Dale", "Cameron", "Dean", "Shane", "Patrick", "Shaun", "Simon", "Mitchell", "Philip", "Dylan", "Martin", "Greg", "Ian", "Fred", "Rory"]
        for player in subsession.get_players():
            random.shuffle(names)
            choices = names[0:5]
            random.shuffle(choices)
            player.participant.performer_name_choices = choices


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    stop_epochtime = models.IntegerField()
    stop_clocktime = models.StringField()
    total_time_to_completion = models.IntegerField()
    comment = models.LongStringField()
    study_name = models.StringField()
    maths_gender_performance = models.StringField(
        label = "Who had a higher average score in the maths task, males or females?",
        choices = ['males', 'females'],
        widget = widgets.RadioSelectHorizontal
    )
    childcare_gender_performance = models.StringField(
        label = "Who had a higher average score in the childcare task, males or females?",
        choices = ['males', 'females'],
        widget = widgets.RadioSelectHorizontal
    )
def study_name_choices(player):
    choices = player.participant.performer_name_choices
    return choices


# PAGES
class general_performance(Page):
    form_model = Player
    form_fields = ['maths_gender_performance', 'childcare_gender_performance']

class study_name(Page):
    form_model = Player
    form_fields = ['study_name']
    
class end(Page):
    form_model = 'player'
    form_fields = ['comment']

    def is_displayed(player):
        # record time player finished application
        import time 
        time_out = round(time.time())
        player.stop_epochtime = time_out
        player.total_time_to_completion = time_out - player.participant.performer_start_epochtime
        player.stop_clocktime = time.strftime('%H:%M:%S', time.localtime(time_out))
        return 1

class comment_submitted(Page):
    def is_displayed(player):
        # record time player finished application - updates the time details if they submit comment
        import time 
        time_out = round(time.time())
        player.stop_epochtime = time_out
        player.total_time_to_completion = time_out - player.participant.performer_start_epochtime
        player.stop_clocktime = time.strftime('%H:%M:%S', time.localtime(time_out))
        return 1


page_sequence = [general_performance, study_name, end, comment_submitted]
