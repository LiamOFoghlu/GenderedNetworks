from otree.api import *

doc = """
Your app description
"""

# CONSTANTS
class Constants(BaseConstants):
    name_in_url = 'referrer_task'
    players_per_group = None
    num_rounds = 4
    no_refer_bonus = "£0.50"
    refer_bonus = "£0.60"
    punishment_bonus = "£0.20"
    reward_bonus = "£0.80"

    ## get performer data
    import pandas as pd
    df_maths_f = pd.read_csv("_static/performer_df_maths_f.csv")
    df_maths_m = pd.read_csv("_static/performer_df_maths_m.csv")
    df_index_maths_f = list(range(len(df_maths_f))) 
    df_index_maths_m = list(range(len(df_maths_m))) 
    df_childcare_f = pd.read_csv("_static/performer_df_childcare_f.csv")
    df_childcare_m = pd.read_csv("_static/performer_df_childcare_m.csv")
    df_index_childcare_f = list(range(len(df_childcare_f))) 
    df_index_childcare_m = list(range(len(df_childcare_m))) 

    ## create a vector to randomise task treatment so that the sample ends up evenly balanced between maths and childcare
    num_participants = 1000          # note this doesn't really have to be the number of participants, it just indirectly determines the number of blocks. Still, good practice to set it hgiher than expected number of participants
    num_blocks = -1*( -num_participants // 2) # I'm gonna create blocks within which the treatment is exactly balanced ==> half in maths and half in childcare
    task_treatment_block = list(range(1,3)) # this is the block: there are two elements, 1 = maths, 2 = childcare
    task_treatment_assignment = [] # a ist of all append treatment blocks
    for i in range(num_blocks):
        task_treatment_assignment = task_treatment_assignment + task_treatment_block # create a list of appended treatment blocks
    import random    
    random.shuffle(task_treatment_assignment) 
    for i in range(len(task_treatment_assignment)):
            if task_treatment_assignment[i] == 1:
                task_treatment_assignment[i] = "maths"
            else:
                task_treatment_assignment[i] = "childcare"


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    if subsession.round_number == 1:
        import itertools, random
        # randomiser to assign to maths or childcare
        task_treatment_assignment = itertools.cycle(Constants.task_treatment_assignment) # 1 = maths; 2 = childcare

        # randomiser to assign order in which they see a male or female profile
        gender_order = list(range(1,5))
        for i in range(len(gender_order)):
            gender_order[i] = gender_order[i] % 2
        for i in range(len(gender_order)):
            if gender_order[i] == 0:
                gender_order[i] = "male"
            else:
                gender_order[i] = "female"  
        
        # iterate through the players
        for player in subsession.get_players(): 
            # set num_referrals to 0 (iteratively add 1 whenever a referrer refers someone)
            player.participant.referrer_num_referrals = 0

            # task treatment assignment
            player.participant.referrer_treatment = next(task_treatment_assignment)

            ## gender assignment ==> assign order in which they see male and female
            referrer_gender_order = random.sample(gender_order, Constants.num_rounds)
            player.participant.referrer_gender_order = referrer_gender_order

            # assign peformers to review ==> a index r, which is a list of randomly sample integers from the range 0:df length
            player.participant.referrer_maths_r_f = random.sample(Constants.df_index_maths_f, Constants.num_rounds)     # randomly sample performers
            player.participant.referrer_childcare_r_f = random.sample(Constants.df_index_childcare_f, Constants.num_rounds)   # randomly sample performers
            player.participant.referrer_maths_r_m = random.sample(Constants.df_index_maths_m, Constants.num_rounds)     # randomly sample performers
            player.participant.referrer_childcare_r_m = random.sample(Constants.df_index_childcare_m, Constants.num_rounds)   # randomly sample performers


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField()
    performer_refer = models.StringField(
        label = "",
        choices = ['Yes','No'],
        widget=widgets.RadioSelectHorizontal
    )

    # candidate attributes
    performer_name = models.StringField()
    performer_score_rd1 = models.IntegerField()
    performer_score_rd2 = models.IntegerField()
    performer_age = models.IntegerField()
    performer_profile_index = models.IntegerField()
    performer_participant_code = models.StringField()
    performer_gender = models.StringField()

    ## maths questions
    maths_question_1_1 = models.StringField(
        label = "A hiker walks from the bottom to the top of a hill. They start at 9.40am and arrive at the top at 10.20 am. They take a rest for ten minutes. Then they walk back down. On the way down, the hiker walks twice as fast as they did on the way up. What time is it when they reach the bottom of the hill?",
        choices = [
            "10.50", # correct
            "10.40",
            "11.00", 
            "11.10"
        ],
        widget = widgets.RadioSelectHorizontal
    )   
    maths_question_1_2 = models.StringField(
        label="An inefficient factory produces 50 cars per week. On average, 10 per 50 has a fault. An inspector picks 2 cars per week to check. What is the probability both cars have faults?",
        choices = [
            "0.012", 
            "0.037", # correct
            "0.099",
            "0.040"
        ],
        widget = widgets.RadioSelectHorizontal
    )
    maths_question_1_3 = models.StringField(
        label = "A wizard has a 1 in 16 chance of killing a troll with his fireball, and can throw one fireball every minute. A hobbit has a 1 in 12 chance of killing the troll with his sword and can strike twice per minute. An elf has a 1 in 6 chance of shooting the troll with his bow and can shoot once per minute. A ranger has a 1 in 8 chance of killing a troll with his fists and can punch twice a minute. Who will kill the troll first?",
        choices = [
            "The wizard",
            "The hobbit",
            "The elf",
            "The ranger" # correct
        ],
         widget = widgets.RadioSelectHorizontal
    )   
    maths_question_1_4 = models.StringField(
        label="Manchester United have a two in three chance of winning when Rashford plays and a one in four chance of winning when he doesn't. Rashford plays 30 matches out of 38 in a season. About how many matches should Manchester United win?",
        choices = [
            "24", 
            "22", # correct
            "20", 
            "23"
        ],
        widget = widgets.RadioSelectHorizontal
    ) 
    maths_question_1_5 = models.StringField(
        label= "A shop has an offer: buy 8 kiwis, and every extra kiwi after that is half price. A customer goes to the shop and pays £5.50 for some kiwis. The full price of a kiwi is £0.50. How many do they buy?",
        choices = [
            "10",
            "12",
            "16",
            "14"  # correct
        ],
        widget = widgets.RadioSelectHorizontal
    )      

    ## childcare questions
    # round 1
    ## childcare questions
    # round 1
    childcare_question_1_1 = models.StringField(
        label= "Babies should be bathed...",
        choices = [
            "Once a day",
            "Once a week",
            "Twice a day",
            "Two to three times a week"
        ],
        widget = widgets.RadioSelectHorizontal
    )      
    childcare_question_1_2 = models.StringField(
        label= "Women should continue on-demand, frequent breastfeeding until the child is:",
        choices = [
            "Six months old",
            "One year old",
            "Two years old",
            "One and a half years old"
        ],
        widget = widgets.RadioSelectHorizontal
    )      
    childcare_question_1_3 = models.StringField(
        label= "Newborn babies…",
        choices = [
            "Do not dream when they sleep",
            "Do not move about much when they sleep",
            "Wake up about once a night",
            "Sleep in cycles that last about one hour"
        ],
        widget = widgets.RadioSelectHorizontal
    )    
    childcare_question_1_4 = models.StringField(
        label= "Children should be exclusively breastfed for:",
        choices = [
            "The first month of their lives",
            "The first three months of their lives",
            "The first six months of their lives",
            "The first nine months of their lives"
        ],
        widget = widgets.RadioSelectHorizontal
    )        
    childcare_question_1_5 = models.StringField(
        label= "Babies can be calmed by...",
        choices = [
            "Squeezing their forearms",
            "Moistening their ears",
            "Stroking their back",
            "Tickling their feet"
        ],
        widget = widgets.RadioSelectHorizontal
    )      


# PAGES
class practice_task(Page):
    form_model = 'player'

    def is_displayed(player):
        # display practice page only in first round
        return (player.round_number == 1)

    def get_form_fields(player: Player):
        if player.participant.referrer_treatment == "maths":
            form_fields = [
                        'maths_question_1_1',
                        'maths_question_1_2',
                        'maths_question_1_3',
                        'maths_question_1_4',
                        'maths_question_1_5'
                        ]
        else: # childcare
            form_fields = [
                        'childcare_question_1_1',
                        'childcare_question_1_2',
                        'childcare_question_1_3',
                        'childcare_question_1_4',
                        'childcare_question_1_5'
                        ] 
        return form_fields           

    def vars_for_template(player):
        if player.participant.referrer_treatment == "maths":
            practice_template = 'referrer_task/maths_template.html'
            task = "maths"
            timer = "200"
        else:
            practice_template = 'referrer_task/childcare_template.html'
            task = "childcare"
            timer = "80"
        return dict(
                task = task,
                practice_template = practice_template,
                timer = timer,
                num_peformers = Constants.num_rounds
                )


class refer_task(Page):
    form_model = 'player'
    form_fields = [
        'performer_refer'
    ]

    def vars_for_template(player):
        if player.participant.referrer_treatment == "maths":
            task = "maths"
            if player.participant.referrer_gender_order[player.round_number - 1] ==  "female":
                df = Constants.df_maths_f
                r = player.participant.referrer_maths_r_f[player.round_number - 1]
            else: # male
                df = Constants.df_maths_m
                r = player.participant.referrer_maths_r_m[player.round_number - 1]                
        else:  # childcare
            task = "childcare"
            if player.participant.referrer_gender_order[player.round_number - 1] ==  "female":
                df = Constants.df_childcare_f
                r = player.participant.referrer_childcare_r_f[player.round_number - 1]
            else: # male
                df = Constants.df_childcare_m
                r = player.participant.referrer_childcare_r_m[player.round_number - 1]     
        return dict(
            task = task,
            performer_name = df.loc[r,'performer_name'],
            score = int(df.loc[r, 'performer_score_rd1']),
            age = df.loc[r, 'performer_age'],
            refer_table_template = 'referrer_task/refer_table_template.html'
        )

    def before_next_page(player, timeout_happened): # need to include "timout_happned" since otherwise it crashes. This is a useless var so should be ignored. But seems to be necessary to avoid crashing.
        if player.participant.referrer_treatment == "maths":
            player.treatment = "maths"
            if player.participant.referrer_gender_order[player.round_number - 1] ==  "female":
                df = Constants.df_maths_f
                r = player.participant.referrer_maths_r_f[player.round_number - 1]
            else: # male
                df = Constants.df_maths_m
                r = player.participant.referrer_maths_r_m[player.round_number - 1]     
        else: # childcare
            player.treatment = "childcare"
            if player.participant.referrer_gender_order[player.round_number - 1] ==  "female":
                df = Constants.df_childcare_f
                r = player.participant.referrer_childcare_r_f[player.round_number - 1]
            else: # male
                df = Constants.df_childcare_m
                r = player.participant.referrer_childcare_r_m[player.round_number - 1]    
        player.performer_name = df.loc[r, 'performer_name']
        player.performer_score_rd1 = int(df.loc[r, 'performer_score_rd1'])
        player.performer_score_rd1 = int(df.loc[r, 'performer_score_rd2'])
        player.performer_age = int(df.loc[r, 'performer_age'])
        player.performer_participant_code = df.loc[r, 'performer_participant_code']
        player.performer_profile_index = r
        player.performer_gender = player.participant.referrer_gender_order[player.round_number - 1]
        if player.performer_refer == "Yes":
            player.participant.referrer_num_referrals += 1    


page_sequence = [practice_task, refer_task]
