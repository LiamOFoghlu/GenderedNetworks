from otree.api import *
from otree.models import subsession


doc = """
Your app description
"""

# CONSTANTS
class Constants(BaseConstants):
    name_in_url = 'referrer_task'
    players_per_group = None
    tasks = ['maths', 'empathy']
    num_rounds = len(tasks)

    # practice questions
    player_maths_qs = 5
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
    df_maths = pd.read_csv("_static/candidate_df_maths.csv")
    df_index_maths = list(range(len(df_maths))) 
    df_empathy = pd.read_csv("_static/candidate_df_empathy.csv")
    df_index_empathy = list(range(len(df_empathy))) 


# FUNCTIONS
def make_maths_field(label,a1,a2,a3,a4):
    return models.FloatField(label = label,
    choices = [a1,a2,a3,a4],
    widget=widgets.RadioSelectHorizontal,
    )


def record_profile_info(df, r, column):
    return df.loc[r,column]

class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    if subsession.round_number == 1:
        print("executing referral task subsession")
        import itertools, random
        t_o = itertools.cycle([1, 2])
        for player in subsession.get_players(): # iterate through the players

            # set referrers to false (takes a value of true if any referral is made)
            player.participant.referrer_any_referral = False

            # task order
            player.participant.referrer_task_order = next(t_o)
            player.participant.referrer_round_numbers = list(range(1, Constants.num_rounds + 1))
            if player.participant.referrer_task_order == 2:
                player.participant.referrer_round_numbers.reverse()
            player.participant.referrer_task_rounds = dict(zip(Constants.tasks, player.participant.referrer_round_numbers))

            # maths questions
            maths_qs = list(range(Constants.player_maths_qs))
            random.shuffle(maths_qs)
            player.participant.referrer_mathspractice_q1 = maths_qs[0]
            player.participant.referrer_mathspractice_q2 = maths_qs[1]

            # empathy questions
            empathy_qs = list(range(Constants.player_empathy_qs))
            random.shuffle(empathy_qs)
            player.participant.referrer_empathypractice_q1 = empathy_qs[0]
            player.participant.referrer_empathypractice_q2 = empathy_qs[1]

            # load profile
            player.participant.referrer_maths_r = random.choice(list(range(len(Constants.df_index_maths))))      # randomly choose a SINGLE profile (i.e. row in data frame)
            player.participant.referrer_empathy_r = random.choice(list(range(len(Constants.df_index_empathy))))  # randomly choose a SINGLE profile (i.e. row in data frame)
        

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    task_order = models.IntegerField()
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
    candidate_name = models.StringField() 
    candidate_score = models.IntegerField()
    candidate_education = models.StringField()
    candidate_age = models.IntegerField()
    candidate_profile_index = models.IntegerField()
    candidate_refer = models.StringField(label = "",
        choices = ['Yes','No'],
        widget=widgets.RadioSelectHorizontal)
    task_in_round = models.StringField()
    task_order = models.StringField()

# PAGES
class practice_task(Page):
    form_model = 'player'

    def is_displayed(player):
        return (player.round_number == 1 or player.round_number == ((Constants.num_rounds)/2) + 1)

    def get_form_fields(player: Player):
        if player.round_number == player.participant.referrer_task_rounds['maths']: 
            questions = ['question1','question2','question3','question4','question5']
            form_fields = [                                  # here I can insert a question from the questions list above by subsetting wiht a numerical index [player.mathspractice_1/2]. The get_form_fields function then "draws" the particular question's details from the information provided under the class Player(BasePlayer) part above.
                        questions[player.participant.referrer_mathspractice_q1],
                        questions[player.participant.referrer_mathspractice_q2],
                        ]
            return form_fields
        else:
            pass # for now until we get questions

    def vars_for_template(player):
        practice_template = 'referrer_task/practice_template.html'
        if player.round_number == 1:
            page_order = "first"
        else: 
            page_order = "second"
        if player.round_number == player.participant.referrer_task_rounds['maths']: 
            task_player_qs = Constants.player_maths_qs
            task = "maths"
        else:
            task_player_qs = Constants.player_empathy_qs
            task = "empathy"
        return dict(
                task = task,
                practice_template = practice_template,
                page_order = page_order, 
                task_player_qs = task_player_qs    #  number of questions answered
        )


class refer_task(Page):
    form_model = 'player'
    form_fields = [
        'candidate_refer'
    ]

    def vars_for_template(player):
        refer_table_template = 'referrer_task/refer_table_template.html'
        current_round = player.round_number 
        if current_round ==  player.participant.referrer_task_rounds['maths']: 
            df = Constants.df_maths
            r = player.participant.referrer_maths_r
            refer_table_template = 'referrer_task/refer_table_template.html'
            task = "maths"
        if current_round ==  player.participant.referrer_task_rounds['empathy']: 
            df = Constants.df_empathy
            r = player.participant.referrer_empathy_r
            task = "empathy"
        return dict(
            task = task,
            candidate_name = record_profile_info(df, r, 'candidate_name'),
            score = int(record_profile_info(df, r, 'score')),
            education = record_profile_info(df, r, 'education'),
            age = record_profile_info(df, r, 'age'),
            refer_table_template = refer_table_template
        )


    def before_next_page(player, timeout_happened): # need to include "timout_happned" since otherwise it crashes. This is a useless var so should be ignored. But seems to be necessary to avoid crashing.
        if player.round_number == player.participant.referrer_task_rounds['maths']: 
            df = Constants.df_maths
            r = player.participant.referrer_maths_r
            player.task_in_round = "maths"
        else:
            df = Constants.df_empathy
            r = player.participant.referrer_empathy_r
            player.task_in_round = "empathy"
        player.candidate_name = record_profile_info(df, r, 'candidate_name')
        player.candidate_score = int(record_profile_info(df, r, 'score'))
        player.candidate_education = record_profile_info(df, r, 'education')
        player.candidate_age = int(record_profile_info(df, r, 'age'))
        player.candidate_profile_index = r
        if player.participant.referrer_task_order == 1:
            player.task_order = "maths_first"
        else:
            player.task_order = "empathy_first"
        if player.candidate_refer == "Yes":
            player.participant.referrer_any_referral = True
        print(player.participant.referrer_any_referral)
        


page_sequence = [practice_task, refer_task]
