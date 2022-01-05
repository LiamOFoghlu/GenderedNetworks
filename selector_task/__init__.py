from otree.api import *
from otree.models import subsession


doc = """
Your app description
"""

# CONSTANTS

class Constants(BaseConstants):
    name_in_url = 'selector_task'
    players_per_group = None
    tasks = ['maths', 'empathy']
    rounds_per_task = 2
    num_rounds = len(tasks) * rounds_per_task # this the total number of rounds that will be done by the player (so, if they do 3 rounds of Task A and 3 rounds of Task B, then they will do 3 + 3 = 6 rounds overall)
    employer_reward = "€1.00"
    referrer_punishment = "€0.90"
    referrer_neither = "€1.25"
    referrer_reward = "€1.50"

    # practice questions
    player_maths_qs = 5 # these are the total number of questions answered by the performer per round
    player_empathy_qs = 5
    maths_labels = [
        'Items bought by a trader for £80 are sold for £100. The profit expressed as a percentage of cost price is: ', 
        'A man bought a shirt at a sale. He saves £30 on the normal price when he paid £120 for the shirt. What was the percentage discount on the shirt?', 
        'How many subsets does {a,b,c,d,e} have?', 
        'What is the median of the given data: 13, 16, 12, 14, 19, 14, 13, 14', 
        'In coordinate geometry, what is the equation of the x-axis?']
    maths_a1 = [
        [2.5, "2.5%"],
        [20, "20%"],
        [2,"2"],
        [14,"14"],
        [1, "y = 0 "]
    ]
    maths_a2 = [
        [20, "20%"],
        [25,"25%"],
        [4,"4"],
        [19,"19"],
        [2,"x = y"]
    ]
    maths_a3 = [
        [25,"25%"],
        [33.33,"33.33%"],
        [10,"10"],
        [12,"12"],
        [3,"3x = 0"]
    ]
    maths_a4 = [
        [50, "50%"],
        [80, "80%"],
        [32,"32"],
        [14.5,"14.5"],
        [4, "y = 1"]
    ]

    # referral data
    import pandas as pd
    df_maths = pd.read_csv("_static/referrals_df_maths.csv")
    df_empathy = pd.read_csv("_static/referrals_df_empathy.csv")

# FUNCTIONS
def make_maths_field(label,a1,a2,a3,a4):
    return models.FloatField(label = label,
    choices = [a1,a2,a3,a4],
    widget=widgets.RadioSelectHorizontal,
    )

def record_profile_info(df, r, column):
    return df.loc[r,column]

def creating_session(subsession):
    if subsession.round_number == 1:
        print("executing subsession")
        import itertools, random

        #randomise task order
        t_o = itertools.cycle([1, 2])

        for player in subsession.get_players(): # iterate through the players

            # create dictionary that links task to round number, based on task_order 
            player.participant.selector_task_order = next(t_o)
            round_numbers = list(range(1, Constants.num_rounds + 1))
            if player.participant.selector_task_order == 2:
                round_numbers.reverse() 
            middle_index = int((len(round_numbers)/2)) # note this approach assumes two tasks
            round_numbers_list1 = round_numbers[:middle_index]
            round_numbers_list2 = round_numbers[middle_index:]
            round_numbers_list = [round_numbers_list1, round_numbers_list2]
            player.participant.selector_task_rounds = dict(zip(Constants.tasks, round_numbers_list))

            # determine which practice maths questions the player answers
            maths_qs = list(range(Constants.player_maths_qs))
            random.shuffle(maths_qs)
            player.participant.selector_maths_practice_qs = maths_qs[0:2]


            # determine which practice empathy questions the player answers
            empathy_qs = list(range(Constants.player_empathy_qs))
            random.shuffle(empathy_qs)
            player.empathypractice_q1 = empathy_qs[0]
            player.empathypractice_q2 = empathy_qs[1]

            # randomly assign profiles -- NB: will need to edit this section when I get the real data
            maths_num_list = list(range(len(Constants.df_maths)))
            random.shuffle(maths_num_list)
            player.participant.selector_maths_r = maths_num_list # this creates a list with the index of the dataset in random order
            empathy_num_list = list(range(len(Constants.df_empathy)))
            random.shuffle(empathy_num_list)
            player.participant.selector_empathy_r = empathy_num_list  # this creates a list with the index of the dataset in random order

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    task_order = models.IntegerField()
    mathspractice_q1 = models.IntegerField() # this and the below fields are simply numbers which record which of the N candidate questions are selected as practice questions
    mathspractice_q2 = models.IntegerField()
    empathypractice_q1 = models.IntegerField()
    empathypractice_q2 = models.IntegerField()
    question1 = make_maths_field(            # this uses the custom make_maths_field function defined above to create the question details (question text and possible answers) for the maths practice questions. Below, under the practice_mathstask page get_form_fields function, some subset of these questions will be randomly selected, depending on the values of the mathspractice_q1/2 variables above.
                label = Constants.maths_labels[0],
                a1 = Constants.maths_a1[0],
                a2 = Constants.maths_a2[0],
                a3 = Constants.maths_a3[0],
                a4 = Constants.maths_a4[0],
            )
    question2 = make_maths_field(
                label = Constants.maths_labels[1],
                a1 = Constants.maths_a1[1],
                a2 = Constants.maths_a2[1],
                a3 = Constants.maths_a3[1],
                a4 = Constants.maths_a4[1],
            )
    question3 = make_maths_field(
                label = Constants.maths_labels[2],
                a1 = Constants.maths_a1[2],
                a2 = Constants.maths_a2[2],
                a3 = Constants.maths_a3[2],
                a4 = Constants.maths_a4[2],
            )
    question4 = make_maths_field(
                label = Constants.maths_labels[3],
                a1 = Constants.maths_a1[3],
                a2 = Constants.maths_a2[3],
                a3 = Constants.maths_a3[3],
                a4 = Constants.maths_a4[3],
            )
    question5 = make_maths_field(
                label = Constants.maths_labels[4],
                a1 = Constants.maths_a1[4],
                a2 = Constants.maths_a2[4],
                a3 = Constants.maths_a3[4],
                a4 = Constants.maths_a4[4],
            )
    candidate_name_a = models.StringField() 
    referrer_name_a = models.StringField()
    candidate_education_a = models.StringField()
    candidate_age_a = models.IntegerField()
    candidate_score_a = models.IntegerField()
    candidate_name_b = models.StringField() 
    referrer_name_b = models.StringField()
    candidate_education_b = models.StringField()
    candidate_age_b = models.IntegerField()
    candidate_score_b = models.IntegerField()
    candidate_profile_index = models.IntegerField()   # remember, the data is in wide format so index is same for both candidates 
    select = models.StringField(label = "",
        choices = ['Performer A','Performer B'],
        widget=widgets.RadioSelectHorizontal)
    referrer_feedback = models.StringField(label = "",
        choices = ['Increase referrer payoff','Decrease referrer payoff', 'Do not change referrer payoff'],
        widget=widgets.RadioSelectHorizontal)
    task_in_this_round = models.StringField()

# PAGES
class practice_task(Page):
    form_model = 'player'

    def is_displayed(player):
        return (player.round_number == 1 or player.round_number == ((Constants.num_rounds)/2) + 1)

    def get_form_fields(player: Player):
        if player.round_number in player.participant.selector_task_rounds['maths']:
            questions = ['question1','question2','question3','question4','question5']
            form_fields = [                                  # here I can insert a question from the questions list above by subsetting wiht a numerical index [player.mathspractice_1/2]. The get_form_fields function then "draws" the particular question's details from the information provided under the class Player(BasePlayer) part above.
                        questions[player.participant.selector_maths_practice_qs[0]],
                        questions[player.participant.selector_maths_practice_qs[1]],
                        ]
            return form_fields
        if player.round_number in player.participant.selector_task_rounds['empathy']:
            pass

    def vars_for_template(player):
        if player.round_number in player.participant.selector_task_rounds['maths']:
            task = "maths"
            task_player_num_qs = Constants.player_maths_qs
        elif player.round_number in player.participant.selector_task_rounds['empathy']:
            task = "empathy"
            task_player_num_qs = Constants.player_empathy_qs
        if player.round_number == 1:
                page_order = "first"       
        elif player.round_number == ((Constants.num_rounds)/2 + 1):
                page_order = "second"
        return dict(
                    task = task,
                    page_order = page_order, 
                    task_player_num_qs = task_player_num_qs   #  number of questions answered
            )


class select_task(Page):   #  Note: should randomise who is player a and who is player b
    form_model = 'player'
    form_fields = [
        'select'
    ]

    def vars_for_template(player):
        current_round = player.round_number
        player_task_order = player.participant.selector_task_order
        if current_round in player.participant.selector_task_rounds['maths']: 
            task = "maths"
            df = Constants.df_maths
            if player_task_order == 1:
                profile_selector = current_round - 1
            else:
                profile_selector = current_round - Constants.rounds_per_task - 1
            r = player.participant.selector_maths_r[profile_selector]
        elif current_round in player.participant.selector_task_rounds['empathy']:
            task = "empathy"
            df = Constants.df_empathy
            if player_task_order == 1:
                profile_selector = current_round - Constants.rounds_per_task - 1
            else:
                profile_selector = current_round - 1
            r = player.participant.selector_empathy_r[profile_selector]
        select_table_template = 'selector_task/select_table_template.html'
        return dict(
            task = task,
            display_round = profile_selector + 1,
            candidate_name_a = record_profile_info(df, r, 'candidate_name.a'),
            referrer_name_a = record_profile_info(df, r, 'referrer_name.a'),
            education_a = record_profile_info(df, r, 'education.a'),
            age_a = record_profile_info(df, r, 'age.a'),
            candidate_name_b = record_profile_info(df, r, 'candidate_name.b'),
            referrer_name_b = record_profile_info(df, r, 'referrer_name.b'),
            education_b = record_profile_info(df, r, 'education.b'),
            age_b = record_profile_info(df, r, 'age.b'),
            select_table_template = select_table_template
        )

    def before_next_page(player, timeout_happened): # need to include "timout_happned" since otherwise it crashes. This is a useless var so should be ignored. But seems to be necessary to avoid crashing.
        current_round = player.round_number
        player_task_order = player.participant.selector_task_order
        if current_round in player.participant.selector_task_rounds['maths']: 
            player.task_in_this_round = "maths"
            df = Constants.df_maths
            if player_task_order == 1:
                profile_selector = current_round - 1
            else:
                profile_selector = current_round - Constants.rounds_per_task - 1
            r = player.participant.selector_maths_r[profile_selector]
        elif current_round in player.participant.selector_task_rounds['empathy']:
            player.task_in_this_round = "empathy"
            df = Constants.df_empathy
            if player_task_order == 1:
                profile_selector = current_round - Constants.rounds_per_task - 1
            else:
                profile_selector = current_round - 1
            r = player.participant.selector_empathy_r[profile_selector]
        player.candidate_profile_index = r  
        player.candidate_name_a = record_profile_info(df, r, 'candidate_name.a')
        player.referrer_name_a = record_profile_info(df, r, 'referrer_name.a')
        player.candidate_education_a = record_profile_info(df, r, 'education.a')
        player.candidate_age_a = int(record_profile_info(df, r, 'age.a'))
        player.candidate_score_a = int(record_profile_info(df, r, 'score.a'))
        player.candidate_name_b = record_profile_info(df, r, 'candidate_name.b')
        player.referrer_name_b = record_profile_info(df, r, 'referrer_name.b')
        player.candidate_education_b = record_profile_info(df, r, 'education.b')
        player.candidate_age_b = int(record_profile_info(df, r, 'age.b'))
        player.candidate_score_b = int(record_profile_info(df, r, 'score.b'))
        print("round:", player.round_number,", selection:", player.select, "referrer a:" , player.referrer_name_a , ", referrer b:", player.referrer_name_b)

class referrer_feedback(Page):
    form_model = 'player'

    def get_form_fields(player: Player):
        if player.select == "Performer A":
            referrer_name = player.referrer_name_a
        else:
            referrer_name = player.referrer_name_b
        if referrer_name == "No referral":
            pass
        else:
            return ['referrer_feedback']
    

    def vars_for_template(player):
        employer_reward_num = int(Constants.employer_reward[1]) # this is just the employer's max payoff per round

        # get selected performer details
        if player.select == "Performer A":
            performer_name = player.candidate_name_a
            performer_letter = "Performer A"
            performer_score = (player.candidate_score_a)/100 # remember score should be percentage (may alter thsi with real data, depending on data structure)
        else:
            performer_name = player.candidate_name_b
            performer_letter = "Performer B"
            performer_score = (player.candidate_score_b)/100

        # estimate payoff
        payoff = str(employer_reward_num * performer_score)
        if len(payoff) < 4:  # this is just so the payoff is rendered in euro denom with two decimal points
            payoff = payoff + "0"
        payoff = "€" + payoff

        # referrer feedback
        if player.select == "Performer A":
            referrer_name = player.referrer_name_a
        else:
            referrer_name = player.referrer_name_b
        if referrer_name == "No referral":
            template = 'selector_task/no_referrer_payoff_template.html'
        else:
            template = 'selector_task/referrer_payoff_template.html'

        # calculate display round
        player_task_order = player.participant.selector_task_order
        if player.round_number in player.participant.selector_task_rounds['maths']: 
            player.task_in_this_round = "maths"
            if player_task_order == 1:
                profile_selector = player.round_number - 1
            else:
                profile_selector = player.round_number - Constants.rounds_per_task - 1
        elif player.round_number in player.participant.selector_task_rounds['empathy']:
            if player_task_order == 1:
                profile_selector = player.round_number - Constants.rounds_per_task - 1
            else:
                profile_selector = player.round_number - 1

        # send variables to page
        return dict(
                template = template,
                task = player.task_in_this_round,
                display_round = profile_selector + 1,
                performer_name = performer_name,
                performer_letter = performer_letter,
                referrer_name = referrer_name,
                employer_payoff = payoff,
                performer_score = str(round(performer_score*100)) + "%"
        )


page_sequence = [practice_task, select_task, referrer_feedback]
