from otree.api import *
from otree.models import subsession


doc = """
Your app description
"""

# CONSTANTS
class Constants(BaseConstants):
    name_in_url = 'referrer_task'
    players_per_group = None
    tasks = ['maths', 'childcare']
    num_rounds = len(tasks)

    # referral data
    import pandas as pd
    df_maths = pd.read_csv("_static/candidate_df_maths.csv")
    df_index_maths = list(range(len(df_maths))) 
    df_childcare = pd.read_csv("_static/candidate_df_childcare.csv")
    df_index_childcare = list(range(len(df_childcare))) 


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
            maths_qs = list(range(5))
            random.shuffle(maths_qs)
            player.participant.referrer_mathspractice_q1 = maths_qs[0]
            player.participant.referrer_mathspractice_q2 = maths_qs[1]

            # childcare questions
            childcare_qs = list(range(5))
            random.shuffle(childcare_qs)
            player.participant.referrer_childcarepractice_q1 = childcare_qs[0]
            player.participant.referrer_childcarepractice_q2 = childcare_qs[1]

            # load profile
            player.participant.referrer_maths_r = random.choice(list(range(len(Constants.df_index_maths))))      # randomly choose a SINGLE profile (i.e. row in data frame)
            player.participant.referrer_childcare_r = random.choice(list(range(len(Constants.df_index_childcare))))  # randomly choose a SINGLE profile (i.e. row in data frame)
        

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    task_order = models.StringField()
    task_in_round = models.StringField()
    candidate_refer = models.StringField(
        label = "",
        choices = ['Yes','No'],
        widget=widgets.RadioSelectHorizontal
    )

    # candidate attributes
    candidate_name = models.StringField()
    candidate_score = models.IntegerField()
    candidate_age = models.IntegerField()
    candidate_profile_index = models.IntegerField()

    ## maths questions
    maths_question_1 = models.StringField(
        label = "A shop has an offer: buy 8 kiwis, and every extra kiwi after that is half price. A customer goes to the shop and pays £4.50 for some kiwis. The full price of a kiwi is £0.50. How many does the customer buy?",
        choices = [
            "9",
            "12",
            "10",
            "15"
        ],
        widget = widgets.RadioSelectHorizontal
    ) 
    maths_question_2 = models.StringField(
        label="A worker's regular pay is £3 per hour up to 40 hours. Overtime is twice the payment for regular time. If the worker was paid £168, how many hours overtime did they work?",
        choices = [
            "8",
            "16",
            "28",
            "48"
        ],
        widget = widgets.RadioSelectHorizontal
    )
    maths_question_3 = models.StringField(
        label="3 and 4/5 expressed as a decimal is:",
        choices = [
            "3.40",
            "3.45",
            "3.80",
            "3.50"
        ],
        widget = widgets.RadioSelectHorizontal
    )
    maths_question_4 = models.StringField(
        label="Which of the following is the highest common factor of 18, 24, and 36?",
        choices = [
            "6",
            "18",
            "36",
            "72"
        ],
        widget = widgets.RadioSelectHorizontal  
    )    
    maths_question_5 = models.StringField(
        label="Which of the following is equal to 3y(x + 3) -2(x + 3) ?",
        choices = [
            "(x - 3)(x - 3)",
            "2y(x + 3)",
            "(x + 3)(3y – 2",
            "3y(x + 3)"
        ],
        widget = widgets.RadioSelectHorizontal  
    )    

    ## childcare questions
    # round 1
    childcare_question_1 = models.StringField(
        label= "Children should be exclusively breastfed for:",
        choices = [
            "The first month of their lives",
            "The first three months of their lives",
            "The first six months of their lives"
        ],
        widget = widgets.RadioSelectHorizontal
    )      
    childcare_question_2 = models.StringField(
        label= "Women should continue on-demand, frequent breastfeeding until the child is:",
        choices = [
            "One year old",
            "Two years old",
            "One and a half years old"
        ],
        widget = widgets.RadioSelectHorizontal
    )      
    childcare_question_3 = models.StringField(
        label= "Newborn babies…",
        choices = [
            "Do not move about much when they sleep",
            "Wake up about once a night",
            "Sleep in cycles that last about one hour"
        ],
        widget = widgets.RadioSelectHorizontal
    )      
    childcare_question_4 = models.StringField(
        label= "Babies should be bathed...",
        choices = [
            "Once a day",
            "Once a week",
            "Two to three times a week"
        ],
        widget = widgets.RadioSelectHorizontal
    )      
    childcare_question_5 = models.StringField(
        label= "Babies can be calmed by...",
        choices = [
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
        if player.round_number == player.participant.referrer_task_rounds['maths']: 
            questions = ['maths_question_1','maths_question_2','maths_question_3','maths_question_4','maths_question_5']
            form_fields = [                                  
                        questions[player.participant.referrer_mathspractice_q1], # an index, range 1:5 which subsets from the questions list above
                        questions[player.participant.referrer_mathspractice_q2],
                        ]
            return form_fields
        else:
            questions = ['childcare_question_1','childcare_question_2','childcare_question_3','childcare_question_4','childcare_question_5']
            form_fields = [                                  
                        questions[player.participant.referrer_childcarepractice_q1], # an index, range 1:5 which subsets from the questions list above
                        questions[player.participant.referrer_childcarepractice_q2],
                        ]
            return form_fields

    def vars_for_template(player):
        if player.round_number == 1:
            page_order = "first"
        else: 
            page_order = "second"
        if player.round_number == player.participant.referrer_task_rounds['maths']: 
            practice_template = 'referrer_task/maths_template.html'
            task = "maths"
            timer = "five"
        else:
            practice_template = 'referrer_task/childcare_template.html'
            task = "childcare"
            timer = "three"
        return dict(
                task = task,
                practice_template = practice_template,
                page_order = page_order, 
                timer = timer
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
        if current_round ==  player.participant.referrer_task_rounds['childcare']: 
            df = Constants.df_childcare
            r = player.participant.referrer_childcare_r
            task = "childcare"
        return dict(
            task = task,
            candidate_name = record_profile_info(df, r, 'candidate_name'),
            score = int(record_profile_info(df, r, 'candidate_score')),
            age = record_profile_info(df, r, 'candidate_age'),
            refer_table_template = refer_table_template
        )


    def before_next_page(player, timeout_happened): # need to include "timout_happned" since otherwise it crashes. This is a useless var so should be ignored. But seems to be necessary to avoid crashing.
        if player.round_number == player.participant.referrer_task_rounds['maths']: 
            df = Constants.df_maths
            r = player.participant.referrer_maths_r
            player.task_in_round = "maths"
        else:
            df = Constants.df_childcare
            r = player.participant.referrer_childcare_r
            player.task_in_round = "childcare"
        player.candidate_name = record_profile_info(df, r, 'candidate_name')
        player.candidate_score = int(record_profile_info(df, r, 'candidate_score'))
        player.candidate_age = int(record_profile_info(df, r, 'candidate_age'))
        player.candidate_profile_index = r
        if player.participant.referrer_task_order == 1:
            player.task_order = "maths_first"
        else:
            player.task_order = "childcare_first"
        if player.candidate_refer == "Yes":
            player.participant.referrer_any_referral = True
        print(player.participant.referrer_any_referral)
        


page_sequence = [practice_task, refer_task]
