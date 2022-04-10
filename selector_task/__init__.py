from otree.api import *
from otree.models import subsession


doc = """
Your app description
"""

# CONSTANTS

class Constants(BaseConstants):
    name_in_url = 'selector_task'
    players_per_group = None
    tasks = ['maths', 'childcare']
    rounds_per_task = 4
    num_rounds = len(tasks) * rounds_per_task # this the total number of rounds that will be done by the player (so, if they do 3 rounds of Task A and 3 rounds of Task B, then they will do 3 + 3 = 6 rounds overall)
    selector_reward = "£0.40"  # reward per decision
    referrer_punishment = "£0.20"
    referrer_neither = "£0.60"
    referrer_reward = "£0.80"

    # referral data
    import pandas as pd
    df_cnf = pd.read_csv("_static/df_cnf.csv")
    df_cnf_index = list(range(len(df_cnf)))
    df_cDff = pd.read_csv("_static/df_cDff.csv")
    df_cDff_index = list(range(len(df_cDff)))
    df_cff = pd.read_csv("_static/df_cff.csv")
    df_cff_index = list(range(len(df_cff)))
    df_cfm = pd.read_csv("_static/df_cfm.csv")
    df_cfm_index = list(range(len(df_cfm)))
    df_cnm = pd.read_csv("_static/df_cnm.csv")
    df_cnm_index = list(range(len(df_cnm)))
    df_cDmm = pd.read_csv("_static/df_cDmm.csv")
    df_cDmm_index = list(range(len(df_cDmm)))
    df_cmm = pd.read_csv("_static/df_cmm.csv")
    df_cmm_index = list(range(len(df_cmm)))
    df_cmf = pd.read_csv("_static/df_cmf.csv")
    df_cmf_index = list(range(len(df_cmf)))
    df_mnf = pd.read_csv("_static/df_mnf.csv")
    df_mnf_index = list(range(len(df_mnf)))
    df_mDff = pd.read_csv("_static/df_mDff.csv")
    df_mDff_index = list(range(len(df_mDff)))
    df_mff = pd.read_csv("_static/df_mff.csv")
    df_mff_index = list(range(len(df_mff)))
    df_mfm = pd.read_csv("_static/df_mfm.csv")
    df_mfm_index = list(range(len(df_mfm)))
    df_mnm = pd.read_csv("_static/df_mnm.csv")
    df_mnm_index = list(range(len(df_mnm)))
    df_mDmm = pd.read_csv("_static/df_mDmm.csv")
    df_mDmm_index = list(range(len(df_mDmm)))
    df_mmm = pd.read_csv("_static/df_mmm.csv")
    df_mmm_index = list(range(len(df_mmm)))
    df_mmf = pd.read_csv("_static/df_mmf.csv")
    df_mmf_index = list(range(len(df_mmf)))


    # treatment
    num_participants = 6000          # note this doesn't really have to be the number of participants, it just indirectly determines the number of blocks. Still, good practice to set it hgiher than expected number of participants
    num_blocks = -1*( -num_participants // 2) # I'm gonna create blocks within which the treatment is exactly balanced ==> half in maths and half in childcare
    generic_treatment_block = list(range(1,3)) # this is the block: there are two elements, 1 = maths, 2 = childcare
    generic_treatment_assignment = [] # a ist of all append treatment blocks
    for i in range(num_blocks):
        generic_treatment_assignment = generic_treatment_assignment + generic_treatment_block # create a list of appended treatment blocks
    import random    
    random.shuffle(generic_treatment_assignment) 


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    if subsession.round_number == 1:
        import itertools, random
        print('restart')

        #randomise task order
        task_order = itertools.cycle([1, 2]) # 1 = maths, 2 = childcare
        generic_treatment_assignment = itertools.cycle(Constants.generic_treatment_assignment) 
        gender_A_list = list(range(Constants.num_rounds)) # a list to determine the performer gender of Profile A
        for i in gender_A_list:
            gender_A_list[i] = (gender_A_list[i] % 2) + 1
            
        for player in subsession.get_players(): # iterate through the players

            # create dictionary that links task to round number, based on task_order 
            player.participant.selector_task_order = next(task_order)
            round_numbers = list(range(1, Constants.num_rounds + 1))
            if player.participant.selector_task_order == 2:
                round_numbers.reverse() 
            middle_index = int((len(round_numbers)/2)) # note this approach assumes two tasks
            round_numbers_list1 = round_numbers[:middle_index]
            round_numbers_list2 = round_numbers[middle_index:]
            round_numbers_list = [round_numbers_list1, round_numbers_list2]
            player.participant.selector_task_rounds = dict(zip(Constants.tasks, round_numbers_list))

            # R1: selector_homo_order, 1 = homo first, hetero second; 2 = hetero first, homo second
            player.participant.selector_homo_order = next(generic_treatment_assignment)  

            # R2: selector_dummy_gender, 1 = male, 2 = female
            player.participant.selector_dummy_gender = next(generic_treatment_assignment)  

            # R3: selector_gender_A, gender of player A, 1 = male, 2 = female
            player.participant.selector_gender_A = random.sample(gender_A_list, Constants.num_rounds)

            # R4: sample profile pair for each treatment condition
            player.participant.selector_r_cnf = random.sample(Constants.df_cnf_index, 1)[0]
            player.participant.selector_r_cDff = random.sample(Constants.df_cDff_index, 2)
            player.participant.selector_r_cff = random.sample(Constants.df_cff_index, 1)[0]
            player.participant.selector_r_cfm = random.sample(Constants.df_cfm_index, 1)[0]
            player.participant.selector_r_cnm = random.sample(Constants.df_cnm_index, 1)[0]
            player.participant.selector_r_cDmm = random.sample(Constants.df_cDmm_index, 2)
            player.participant.selector_r_cmm = random.sample(Constants.df_cmm_index, 1)[0]
            player.participant.selector_r_cmf = random.sample(Constants.df_cmf_index, 1)[0]
            player.participant.selector_r_mnf = random.sample(Constants.df_mnf_index, 1)[0]
            player.participant.selector_r_mDff = random.sample(Constants.df_mDff_index, 2)
            player.participant.selector_r_mff = random.sample(Constants.df_mff_index, 1)[0]
            player.participant.selector_r_mfm = random.sample(Constants.df_mfm_index, 1)[0]
            player.participant.selector_r_mnm = random.sample(Constants.df_mnm_index, 1)[0]
            player.participant.selector_r_mDmm = random.sample(Constants.df_mDmm_index, 2)
            player.participant.selector_r_mmm = random.sample(Constants.df_mmm_index, 1)[0]
            player.participant.selector_r_mmf = random.sample(Constants.df_mmf_index, 1)[0]      
            
            print(player.participant.selector_r_cnf,
                player.participant.selector_r_cDff,
                player.participant.selector_r_cff,
                player.participant.selector_r_cfm,
                player.participant.selector_r_cnm,
                player.participant.selector_r_cDmm,
                player.participant.selector_r_cmm,
                player.participant.selector_r_cmf,
                player.participant.selector_r_mnf,
                player.participant.selector_r_mDff,
                player.participant.selector_r_mff,
                player.participant.selector_r_mfm,
                player.participant.selector_r_mnm,
                player.participant.selector_r_mDmm,
                player.participant.selector_r_mmm,
                player.participant.selector_r_mmf)

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    ## Performer profiles
    referrer_name_a = models.StringField()
    referral_code_a = models.StringField()
    performer_name_a = models.StringField() 
    performer_age_a = models.IntegerField()
    performer_score_a = models.IntegerField()
    referrer_name_b = models.StringField()
    referral_code_b = models.StringField()
    performer_name_b = models.StringField() 
    performer_age_b = models.IntegerField()
    performer_score_b = models.IntegerField()
    select = models.StringField(label = "",
        choices = ['Performer A','Performer B'],
        widget=widgets.RadioSelectHorizontal)
    task_in_this_round = models.StringField()

    referrer_feedback2 = models.StringField(label = "",
        choices = ['Decrease referrer payoff', 'Do not change referrer payoff', 'Increase referrer payoff',],
        widget=widgets.RadioSelectHorizontal)
    referrer_feedback3 = models.StringField(label = "",
        choices = ['Decrease referrer payoff', 'Do not change referrer payoff', 'Increase referrer payoff',],
        widget=widgets.RadioSelectHorizontal)
    referrer_feedback4 = models.StringField(label = "",
        choices = ['Decrease referrer payoff', 'Do not change referrer payoff', 'Increase referrer payoff',],
        widget=widgets.RadioSelectHorizontal)

    ## practice questions
    # maths questions
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

    # childcare questions
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
        return (player.round_number == 1 or player.round_number == ((Constants.num_rounds)/2) + 1)

    def get_form_fields(player: Player):
        if player.round_number in player.participant.selector_task_rounds['maths']:
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
        if player.round_number in player.participant.selector_task_rounds['maths']:
            template = 'selector_task/practice_maths_template.html'
            task = "maths"
            Task = "Maths"
            task_player_num_qs = "five"
        elif player.round_number in player.participant.selector_task_rounds['childcare']:
            template = 'selector_task/practice_childcare_template.html'
            task = "childcare"
            Task = "Childcare"
            task_player_num_qs = "five"
        if player.round_number == 1:
                page_order = "first"       
        elif player.round_number == ((Constants.num_rounds)/2 + 1):
                page_order = "second"
        return dict(
                    task = task,
                    Task = Task,
                    template = template,
                    page_order = page_order, 
                    task_player_num_qs = task_player_num_qs   #  number of questions answered
            )


class select_task(Page):  
    form_model = 'player'
    form_fields = [
        'select'
    ]

    def vars_for_template(player):
        current_round = player.round_number
        player_task_order = player.participant.selector_task_order

        ## maths
        if current_round in player.participant.selector_task_rounds['maths']: 
            # task
            task = "maths"

            # profile_selector index
            if player_task_order == 1:
                profile_selector = current_round       # profile_selector is just a way to account for the fact that the second task's "first" round is actually the 5th one
            else:
                profile_selector = current_round - Constants.rounds_per_task
            
            # select profile pairs
            if profile_selector == 1: # {nm, nf}
                if player.participant.selector_gender_A[current_round - 1] == 1: # male performer = A
                    df_A = Constants.df_mnm # A profile
                    r_A = player.participant.selector_r_mnm
                    df_B = Constants.df_mnf # B profile
                    r_B = player.participant.selector_r_mnf
                else: # female performer = A
                    df_A = Constants.df_mnf # A profile
                    r_A = player.participant.selector_r_mnf
                    df_B = Constants.df_mnm # B profile
                    r_B = player.participant.selector_r_mnm
            if profile_selector == 2: # {dummy}
                if player.participant.selector_dummy_gender == 1: # males only
                    df_A = Constants.df_mDmm # A profile
                    r_A = player.participant.selector_r_mDmm[0]
                    df_B = Constants.df_mDmm # B profile
                    r_B = player.participant.selector_r_mDmm[1]
                else: # females only
                    df_A = Constants.df_mDff # A profile
                    r_A = player.participant.selector_r_mDff[0]
                    df_B = Constants.df_mDff # B profile
                    r_B = player.participant.selector_r_mDff[1]
            if profile_selector == 3: # {homo/hetero}
                if player.participant.selector_gender_A[current_round - 1] == 1: # male performer = A
                    if player.participant.selector_homo_order == 1: # homo first
                        df_A = Constants.df_mmm # A profile
                        r_A = player.participant.selector_r_mmm
                        df_B = Constants.df_mff # B profile
                        r_B = player.participant.selector_r_mff
                    else: # hetero first
                        df_A = Constants.df_mfm # A profile
                        r_A = player.participant.selector_r_mfm
                        df_B = Constants.df_mmf # B profile
                        r_B = player.participant.selector_r_mmf                       
                else: # female performer = A
                    if player.participant.selector_homo_order == 1: # homo first
                        df_A = Constants.df_mff # A profile
                        r_A = player.participant.selector_r_mff
                        df_B = Constants.df_mmm # B profile
                        r_B = player.participant.selector_r_mmm
                    else: # hetero first
                        df_A = Constants.df_mmf # A profile
                        r_A = player.participant.selector_r_mmf
                        df_B = Constants.df_mfm # B profile
                        r_B = player.participant.selector_r_mfm  
            if profile_selector == 4: # {homo/hetero}
                if player.participant.selector_gender_A[current_round - 1] == 1: # male performer = A
                    if player.participant.selector_homo_order == 2: # homo second
                        df_A = Constants.df_mmm # A profile
                        r_A = player.participant.selector_r_mmm
                        df_B = Constants.df_mff # B profile
                        r_B = player.participant.selector_r_mff
                    else: # hetero second
                        df_A = Constants.df_mfm # A profile
                        r_A = player.participant.selector_r_mfm
                        df_B = Constants.df_mmf # B profile
                        r_B = player.participant.selector_r_mmf                       
                else: # female performer = A
                    if player.participant.selector_homo_order == 2: # homo second
                        df_A = Constants.df_mff # A profile
                        r_A = player.participant.selector_r_mff
                        df_B = Constants.df_mmm # B profile
                        r_B = player.participant.selector_r_mmm
                    else: # hetero second
                        df_A = Constants.df_mmf # A profile
                        r_A = player.participant.selector_r_mmf
                        df_B = Constants.df_mfm # B profile
                        r_B = player.participant.selector_r_mfm 

        # childcare
        if current_round in player.participant.selector_task_rounds['childcare']: 
            # task
            task = "childcare"

            # profile_selector index
            if player_task_order == 1:
                profile_selector = current_round - Constants.rounds_per_task       # profile_selector is just a way to account for the fact that the second task's "first" round is actually the 5th one
            else:
                profile_selector = current_round 

            if profile_selector == 1: # {nm, nf}
                if player.participant.selector_gender_A[current_round - 1] == 1: # male performer = A
                    df_A = Constants.df_cnm # A profile
                    r_A = player.participant.selector_r_cnm
                    df_B = Constants.df_cnf # B profile
                    r_B = player.participant.selector_r_cnf
                else: # female performer = A
                    df_A = Constants.df_cnf # A profile
                    r_A = player.participant.selector_r_cnf
                    df_B = Constants.df_cnm # B profile
                    r_B = player.participant.selector_r_cnm
            if profile_selector == 2: # {dummy}
                if player.participant.selector_dummy_gender == 1: # males only
                    df_A = Constants.df_cDmm # A profile
                    r_A = player.participant.selector_r_cDmm[0]
                    df_B = Constants.df_cDmm # B profile
                    r_B = player.participant.selector_r_cDmm[1]
                else: # females only
                    df_A = Constants.df_cDff # A profile
                    r_A = player.participant.selector_r_cDff[0]
                    df_B = Constants.df_cDff # B profile
                    r_B = player.participant.selector_r_cDff[1]
            if profile_selector == 3: # {homo/hetero}
                if player.participant.selector_gender_A[current_round - 1] == 1: # male performer = A
                    if player.participant.selector_homo_order == 1: # homo first
                        df_A = Constants.df_cmm # A profile
                        r_A = player.participant.selector_r_cmm
                        df_B = Constants.df_cff # B profile
                        r_B = player.participant.selector_r_cff
                    else: # hetero first
                        df_A = Constants.df_cfm # A profile
                        r_A = player.participant.selector_r_cfm
                        df_B = Constants.df_cmf # B profile
                        r_B = player.participant.selector_r_cmf                       
                else: # female performer = A
                    if player.participant.selector_homo_order == 1: # homo first
                        df_A = Constants.df_cff # A profile
                        r_A = player.participant.selector_r_cff
                        df_B = Constants.df_cmm # B profile
                        r_B = player.participant.selector_r_cmm
                    else: # hetero first
                        df_A = Constants.df_cmf # A profile
                        r_A = player.participant.selector_r_cmf
                        df_B = Constants.df_cfm # B profile
                        r_B = player.participant.selector_r_cfm  
            if profile_selector == 4: # {homo/hetero}
                if player.participant.selector_gender_A[current_round - 1] == 1: # male performer = A
                    if player.participant.selector_homo_order == 2: # homo second
                        df_A = Constants.df_cmm # A profile
                        r_A = player.participant.selector_r_cmm
                        df_B = Constants.df_cff # B profile
                        r_B = player.participant.selector_r_cff
                    else: # hetero second
                        df_A = Constants.df_cfm # A profile
                        r_A = player.participant.selector_r_cfm
                        df_B = Constants.df_cmf # B profile
                        r_B = player.participant.selector_r_cmf                       
                else: # female performer = A
                    if player.participant.selector_homo_order == 2: # homo second
                        df_A = Constants.df_cff # A profile
                        r_A = player.participant.selector_r_cff
                        df_B = Constants.df_cmm # B profile
                        r_B = player.participant.selector_r_cmm
                    else: # hetero second
                        df_A = Constants.df_cmf # A profile
                        r_A = player.participant.selector_r_cmf
                        df_B = Constants.df_cfm # B profile
                        r_B = player.participant.selector_r_cfm 

        ## define dictionary
        return dict(
            task = task,
            display_round = profile_selector,
            performer_name_a = df_A.loc[r_A, 'performer_name'],
            referrer_name_a = df_A.loc[r_A, 'referrer_name'],
            performer_age_a = df_A.loc[r_A, 'performer_age'],
            performer_name_b = df_B.loc[r_B, 'performer_name'],
            referrer_name_b = df_B.loc[r_B, 'referrer_name'],
            performer_age_b = df_B.loc[r_B, 'performer_age'],
            select_table_template = 'selector_task/select_table_template.html'
        )


    def before_next_page(player, timeout_happened): # need to include "timout_happned" since otherwise it crashes. This is a useless var so should be ignored. But seems to be necessary to avoid crashing.

        current_round = player.round_number
        player_task_order = player.participant.selector_task_order

        ## maths
        if current_round in player.participant.selector_task_rounds['maths']: 
            # task
            player.task_in_this_round = "maths"

            # profile_selector index
            if player_task_order == 1:
                profile_selector = current_round       # profile_selector is just a way to account for the fact that the second task's "first" round is actually the 5th one
            else:
                profile_selector = current_round - Constants.rounds_per_task
            
            # select profile pairs
            if profile_selector == 1: # {nm, nf}
                if player.participant.selector_gender_A[current_round - 1] == 1: # male performer = A
                    df_A = Constants.df_mnm # A profile
                    r_A = player.participant.selector_r_mnm
                    df_B = Constants.df_mnf # B profile
                    r_B = player.participant.selector_r_mnf
                else: # female performer = A
                    df_A = Constants.df_mnf # A profile
                    r_A = player.participant.selector_r_mnf
                    df_B = Constants.df_mnm # B profile
                    r_B = player.participant.selector_r_mnm
            if profile_selector == 2: # {dummy}
                if player.participant.selector_dummy_gender == 1: # males only
                    df_A = Constants.df_mDmm # A profile
                    r_A = player.participant.selector_r_mDmm[0]
                    df_B = Constants.df_mDmm # B profile
                    r_B = player.participant.selector_r_mDmm[1]
                else: # females only
                    df_A = Constants.df_mDff # A profile
                    r_A = player.participant.selector_r_mDff[0]
                    df_B = Constants.df_mDff # B profile
                    r_B = player.participant.selector_r_mDff[1]
            if profile_selector == 3: # {homo/hetero}
                if player.participant.selector_gender_A[current_round - 1] == 1: # male performer = A
                    if player.participant.selector_homo_order == 1: # homo first
                        df_A = Constants.df_mmm # A profile
                        r_A = player.participant.selector_r_mmm
                        df_B = Constants.df_mff # B profile
                        r_B = player.participant.selector_r_mff
                    else: # hetero first
                        df_A = Constants.df_mfm # A profile
                        r_A = player.participant.selector_r_mfm
                        df_B = Constants.df_mmf # B profile
                        r_B = player.participant.selector_r_mmf                       
                else: # female performer = A
                    if player.participant.selector_homo_order == 1: # homo first
                        df_A = Constants.df_mff # A profile
                        r_A = player.participant.selector_r_mff
                        df_B = Constants.df_mmm # B profile
                        r_B = player.participant.selector_r_mmm
                    else: # hetero first
                        df_A = Constants.df_mmf # A profile
                        r_A = player.participant.selector_r_mmf
                        df_B = Constants.df_mfm # B profile
                        r_B = player.participant.selector_r_mfm  
            if profile_selector == 4: # {homo/hetero}
                if player.participant.selector_gender_A[current_round - 1] == 1: # male performer = A
                    if player.participant.selector_homo_order == 2: # homo second
                        df_A = Constants.df_mmm # A profile
                        r_A = player.participant.selector_r_mmm
                        df_B = Constants.df_mff # B profile
                        r_B = player.participant.selector_r_mff
                    else: # hetero second
                        df_A = Constants.df_mfm # A profile
                        r_A = player.participant.selector_r_mfm
                        df_B = Constants.df_mmf # B profile
                        r_B = player.participant.selector_r_mmf                       
                else: # female performer = A
                    if player.participant.selector_homo_order == 2: # homo second
                        df_A = Constants.df_mff # A profile
                        r_A = player.participant.selector_r_mff
                        df_B = Constants.df_mmm # B profile
                        r_B = player.participant.selector_r_mmm
                    else: # hetero second
                        df_A = Constants.df_mmf # A profile
                        r_A = player.participant.selector_r_mmf
                        df_B = Constants.df_mfm # B profile
                        r_B = player.participant.selector_r_mfm 

        # childcare
        if current_round in player.participant.selector_task_rounds['childcare']: 
            # task
            player.task_in_this_round = "childcare"

            # profile_selector index
            if player_task_order == 1:
                profile_selector = current_round - Constants.rounds_per_task       # profile_selector is just a way to account for the fact that the second task's "first" round is actually the 5th one
            else:
                profile_selector = current_round 

            if profile_selector == 1: # {nm, nf}
                if player.participant.selector_gender_A[current_round - 1] == 1: # male performer = A
                    df_A = Constants.df_cnm # A profile
                    r_A = player.participant.selector_r_cnm
                    df_B = Constants.df_cnf # B profile
                    r_B = player.participant.selector_r_cnf
                else: # female performer = A
                    df_A = Constants.df_cnf # A profile
                    r_A = player.participant.selector_r_cnf
                    df_B = Constants.df_cnm # B profile
                    r_B = player.participant.selector_r_cnm
            if profile_selector == 2: # {dummy}
                if player.participant.selector_dummy_gender == 1: # males only
                    df_A = Constants.df_cDmm # A profile
                    r_A = player.participant.selector_r_cDmm[0]
                    df_B = Constants.df_cDmm # B profile
                    r_B = player.participant.selector_r_cDmm[1]
                else: # females only
                    df_A = Constants.df_cDff # A profile
                    r_A = player.participant.selector_r_cDff[0]
                    df_B = Constants.df_cDff # B profile
                    r_B = player.participant.selector_r_cDff[1]
            if profile_selector == 3: # {homo/hetero}
                if player.participant.selector_gender_A[current_round - 1] == 1: # male performer = A
                    if player.participant.selector_homo_order == 1: # homo first
                        df_A = Constants.df_cmm # A profile
                        r_A = player.participant.selector_r_cmm
                        df_B = Constants.df_cff # B profile
                        r_B = player.participant.selector_r_cff
                    else: # hetero first
                        df_A = Constants.df_cfm # A profile
                        r_A = player.participant.selector_r_cfm
                        df_B = Constants.df_cmf # B profile
                        r_B = player.participant.selector_r_cmf                       
                else: # female performer = A
                    if player.participant.selector_homo_order == 1: # homo first
                        df_A = Constants.df_cff # A profile
                        r_A = player.participant.selector_r_cff
                        df_B = Constants.df_cmm # B profile
                        r_B = player.participant.selector_r_cmm
                    else: # hetero first
                        df_A = Constants.df_cmf # A profile
                        r_A = player.participant.selector_r_cmf
                        df_B = Constants.df_cfm # B profile
                        r_B = player.participant.selector_r_cfm  
            if profile_selector == 4: # {homo/hetero}
                if player.participant.selector_gender_A[current_round - 1] == 1: # male performer = A
                    if player.participant.selector_homo_order == 2: # homo second
                        df_A = Constants.df_cmm # A profile
                        r_A = player.participant.selector_r_cmm
                        df_B = Constants.df_cff # B profile
                        r_B = player.participant.selector_r_cff
                    else: # hetero second
                        df_A = Constants.df_cfm # A profile
                        r_A = player.participant.selector_r_cfm
                        df_B = Constants.df_cmf # B profile
                        r_B = player.participant.selector_r_cmf                       
                else: # female performer = A
                    if player.participant.selector_homo_order == 2: # homo second
                        df_A = Constants.df_cff # A profile
                        r_A = player.participant.selector_r_cff
                        df_B = Constants.df_cmm # B profile
                        r_B = player.participant.selector_r_cmm
                    else: # hetero second
                        df_A = Constants.df_cmf # A profile
                        r_A = player.participant.selector_r_cmf
                        df_B = Constants.df_cfm # B profile
                        r_B = player.participant.selector_r_cfm 

        player.performer_name_a = df_A.loc[r_A, 'performer_name']
        player.referral_code_a = df_A.loc[r_A, 'referral_code']
        player.referrer_name_a = df_A.loc[r_A, 'referrer_name']
        player.performer_age_a = int(df_A.loc[r_A, 'performer_age'])
        player.performer_score_a = int(df_A.loc[r_A, 'score_rd2'])
        player.performer_name_b = df_B.loc[r_B, 'performer_name']
        player.referral_code_b = df_B.loc[r_B, 'referral_code']
        player.referrer_name_b = df_B.loc[r_B, 'referrer_name']
        player.performer_age_b = int(df_B.loc[r_B, 'performer_age'])
        player.performer_score_b = int(df_B.loc[r_B, 'score_rd2'])



class referrer_feedback(Page):
    form_model = 'player'
    form_fields = [
        'referrer_feedback2',
        'referrer_feedback3',
        'referrer_feedback4',
    ]

    def is_displayed(player):
        return (player.round_number == 4 or player.round_number == 8)

    def vars_for_template(player):
        selector_reward_num = float(Constants.selector_reward[1:len(Constants.selector_reward)]) # this is just the selector's max payoff per round

        # get data from rounds 2 and 3 and 4
        round1 = player.in_round(player.round_number - 3)
        if round1.select == "Performer A":
            performer_name1 = round1.performer_name_a
            performer_letter1 = "Performer A"
            performer_score1 = (round1.performer_score_a)/5 
        else:
            performer_name1 = round1.performer_name_b
            performer_letter1 = "Performer B"
            performer_score1 = (round1.performer_score_b)/5
        round2 = player.in_round(player.round_number - 2)
        if round2.select == "Performer A":
            performer_name2 = round2.performer_name_a
            performer_letter2 = "Performer A"
            performer_score2 = (round2.performer_score_a)/5 
        else:
            performer_name2 = round2.performer_name_b
            performer_letter2 = "Performer B"
            performer_score2 = (round2.performer_score_b)/5
        round3 = player.in_round(player.round_number - 1)
        if round3.select == "Performer A":
            performer_name3 = round3.performer_name_a
            performer_letter3 = "Performer A"
            performer_score3 = (round3.performer_score_a)/5 
        else:
            performer_name3 = round3.performer_name_b
            performer_letter3 = "Performer B"
            performer_score3 = (round3.performer_score_b)/5
        if player.select == "Performer A": # round 4 [i.e. currrent round]
            performer_name4 = player.performer_name_a
            performer_letter4 = "Performer A"
            performer_score4 = (player.performer_score_a)/5 
        else:
            performer_name4 = player.performer_name_b
            performer_letter4 = "Performer B"
            performer_score4 = (player.performer_score_b)/5

        # Payoffs
        payoff1 = str(round(selector_reward_num*performer_score1, 2))
        if len(payoff1) < 4:  # this is just so the payoff is rendered in euro denom with two decimal points
            payoff1 = payoff1 + "0"
        payoff1 = "£" + payoff1
        payoff2 = str(round(selector_reward_num*performer_score2, 2))
        if len(payoff2) < 4:  # this is just so the payoff is rendered in euro denom with two decimal points
            payoff2 = payoff2 + "0"
        payoff2 = "£" + payoff2
        payoff3 = str(round(selector_reward_num*performer_score3, 2))
        if len(payoff3) < 4:  # this is just so the payoff is rendered in euro denom with two decimal points
            payoff3 = payoff3 + "0"
        payoff3 = "£" + payoff3
        payoff4 = str(round(selector_reward_num*performer_score4, 2))
        if len(payoff4) < 4:  # this is just so the payoff is rendered in euro denom with two decimal points
            payoff4 = payoff4 + "0"
        payoff4 = "£" + payoff4

        # referrer feedback
        if round1.select == "Performer A":
            referrer_name1 = round1.referrer_name_a
        else:
            referrer_name1 = round1.referrer_name_b
        if round2.select == "Performer A":
            referrer_name2 = round2.referrer_name_a
        else:
            referrer_name2 = round2.referrer_name_b
        if round3.select == "Performer A":
            referrer_name3 = round3.referrer_name_a
        else:
            referrer_name3 = round3.referrer_name_b
        if player.select == "Performer A":
            referrer_name4 = player.referrer_name_a
        else:
            referrer_name4 = player.referrer_name_b

        # calculate display round
        player_task_order = player.participant.selector_task_order
        if player.round_number in player.participant.selector_task_rounds['maths']: 
            player.task_in_this_round = "maths"
            if player_task_order == 1:
                profile_selector = player.round_number - 1
            else:
                profile_selector = player.round_number - Constants.rounds_per_task - 1
        elif player.round_number in player.participant.selector_task_rounds['childcare']:
            if player_task_order == 1:
                profile_selector = player.round_number - Constants.rounds_per_task - 1
            else:
                profile_selector = player.round_number - 1

        # send variables to page
        return dict(
                task = player.task_in_this_round,
                display_round = profile_selector + 1,
                performer_name1 = performer_name1,
                performer_name2 = performer_name2,
                performer_name3 = performer_name3,
                performer_name4 = performer_name4,
                performer_letter1 = performer_letter1,
                performer_letter2 = performer_letter2,
                performer_letter3 = performer_letter3,
                performer_letter4 = performer_letter4,
                referrer_name1 = referrer_name1,
                referrer_name2 = referrer_name2,
                referrer_name3 = referrer_name3,
                referrer_name4 = referrer_name4,
                payoff1 = payoff1,
                payoff2 = payoff2,
                payoff3 = payoff3,
                payoff4 = payoff4,
                performer_score1 = str(round(performer_score1*100)) + "%",
                performer_score2 = str(round(performer_score2*100)) + "%",
                performer_score3 = str(round(performer_score3*100)) + "%",
                performer_score4 = str(round(performer_score4*100)) + "%",
        )


page_sequence = [practice_task, select_task, referrer_feedback]
