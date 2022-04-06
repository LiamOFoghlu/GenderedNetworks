from otree.api import *

doc = """
Your app description
"""

# CONSTANTS
class Constants(BaseConstants):
    name_in_url = 'referrer_task'
    players_per_group = None
    num_rounds = 4

    ## get referral data
    import pandas as pd
    df_maths = pd.read_csv("_static/performer_df_maths.csv")
    df_index_maths = list(range(len(df_maths))) 
    df_childcare = pd.read_csv("_static/performer_df_childcare.csv")
    df_index_childcare = list(range(len(df_childcare))) 

    ## create a vector to randomise treatment
    num_participants = 500          # note this doesn't really have to be the number of participants, it just indirectly determines the number of blocks. Still, good practice to set it hgiher than expected number of participants
    num_blocks = -1*( -num_participants // 2) # I'm gonna create blocks within which the treatment is exactly balanced ==> half in maths and half in childcare
    treatment_block = list(range(1,3)) # this is the block: there are two elements, 1= maths, 2 = childcare
    treatment_assignment = [] # a ist of all append treatment blocks
    for i in range(num_blocks):
        treatment_assignment = treatment_assignment + treatment_block # create a list of appended treatment blocks
    import random    
    random.shuffle(treatment_assignment) 
    for i in range(len(treatment_assignment)):
            if treatment_assignment[i] == 1:
                treatment_assignment[i] = "maths"
            else:
                treatment_assignment[i] = "childcare"


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    if subsession.round_number == 1:
        print("executing referral task subsession")
        import itertools, random
        treatment_assignment = itertools.cycle(Constants.treatment_assignment) # 1 = maths; 2 = childcare
        for player in subsession.get_players(): # iterate through the players

            # set referrers to false (takes a value of true if any referral is made)
            player.participant.referrer_num_referrals = 0

            # treatment assignment
            player.participant.referrer_treatment = next(treatment_assignment)

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

            # assign peformers to review
            player.participant.referrer_maths_r = random.sample(list(range(len(Constants.df_index_maths))), Constants.num_rounds)      # randomly sample performers
            player.participant.referrer_childcare_r = random.sample(list(range(len(Constants.df_index_childcare))), Constants.num_rounds)   # randomly sample performers
            print(player.participant.code, player.participant.referrer_treatment, "maths index: ",  player.participant.referrer_maths_r, "childcare index: ", player.participant.referrer_childcare_r)


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
    performer_score = models.IntegerField()
    performer_age = models.IntegerField()
    performer_profile_index = models.IntegerField()
    performer_participant_code = models.StringField()

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
            "(x + 3)(3y - 2",
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
        # display practice page only in first round
        return (player.round_number == 1)

    def get_form_fields(player: Player):
        if player.participant.referrer_treatment == "maths":
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
        if player.participant.referrer_treatment == "maths":
            practice_template = 'referrer_task/maths_template.html'
            task = "maths"
            timer = "!!"
        else:
            practice_template = 'referrer_task/childcare_template.html'
            task = "childcare"
            timer = "!!"
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
        refer_table_template = 'referrer_task/refer_table_template.html'
        if player.participant.referrer_treatment == "maths":
            df = Constants.df_maths
            r = player.participant.referrer_maths_r[player.round_number - 1]
            refer_table_template = 'referrer_task/refer_table_template.html'
            task = "maths"
        else: 
            df = Constants.df_childcare
            r = player.participant.referrer_childcare_r[player.round_number - 1]
            task = "childcare"
        return dict(
            task = task,
            performer_name = df.loc[r,'performer_name'],
            score = int(df.loc[r, 'performer_score']),
            age = df.loc[r, 'performer_age'],
            refer_table_template = refer_table_template
        )

    def before_next_page(player, timeout_happened): # need to include "timout_happned" since otherwise it crashes. This is a useless var so should be ignored. But seems to be necessary to avoid crashing.
        if player.participant.referrer_treatment == "maths":
            df = Constants.df_maths
            r = player.participant.referrer_maths_r[player.round_number - 1]
            player.treatment = "maths"
        else:
            df = Constants.df_childcare
            r = player.participant.referrer_childcare_r[player.round_number - 1]
            player.treatment = "childcare"
        player.performer_name = df.loc[r, 'performer_name']
        player.performer_score = int(df.loc[r, 'performer_score'])
        player.performer_age = int(df.loc[r, 'performer_age'])
        player.performer_participant_code = df.loc[r, 'performer_participant_code']
        player.performer_profile_index = r
        if player.performer_refer == "Yes":
            player.participant.referrer_num_referrals += 1    
            print(player.participant.referrer_num_referrals)    


page_sequence = [practice_task, refer_task]
