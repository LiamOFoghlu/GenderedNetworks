from otree.api import *


doc = """
Your app description
"""



#___ Constants ___#

class Constants(BaseConstants):
    name_in_url = 'performer_task'
    players_per_group = None
    total_reward = 4
    tasks = ['maths', 'empathy']
    rounds_per_task = 2
    num_rounds = len(tasks) * rounds_per_task # this the total number of rounds that will be done by the player (so, if they do 3 rounds of Task A and 3 rounds of Task B, then they will do 3 + 3 = 6 rounds overall)
    participation_fee = "€3.50"
    questions_per_round = 5
    reward_per_q = "€" + str(total_reward/(questions_per_round*num_rounds))
    if len(reward_per_q) == 2:
        reward_per_q = reward_per_q + ".00"
    elif len(reward_per_q) == 4:
        reward_per_q = reward_per_q + "0"
    maths_timeout_seconds = 240     # four minutes
    empathy_timeout_seconds = 120   # two minutes


#___ Functions ___#
def make_field(label,a1,a2,a3,a4):
    answers = [a1,a2,a3,a4]
    choices = []
    for i in range(len(answers)):
        answers[i].append(i + 1)
        answers[i].reverse()
        choices.append(answers[i])
    return models.StringField(label = label,
    choices = choices,
    widget=widgets.RadioSelectHorizontal,
    )

def creating_session(subsession):
    if subsession.round_number == 1:
        print("executing subsession")
        import itertools

        #randomise task order
        t_o = itertools.cycle([1, 2])

        for player in subsession.get_players(): # iterate through the players

            # create dictionary that links task to round number, based on task_order 
            player.participant.performer_task_order = next(t_o)
            round_numbers = list(range(1, Constants.num_rounds + 1))
            if player.participant.performer_task_order == 2:
                round_numbers.reverse() 
            middle_index = int((len(round_numbers)/2)) # note this approach assumes two tasks
            round_numbers_list1 = round_numbers[:middle_index]
            round_numbers_list2 = round_numbers[middle_index:]
            round_numbers_list = [round_numbers_list1, round_numbers_list2]
            player.participant.performer_task_rounds = dict(zip(Constants.tasks, round_numbers_list))
            print(player.participant.code, player.participant.performer_task_rounds)



#______ Other classes _____#

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    task_order = models.IntegerField()
    maths_question_1_1 = make_field(label="Which of the following is a subset of {b,c,d}?",
    a1 = ["{ }"],
    a2 = ["{a}"],
    a3 = ["{1,2,3}"],
    a4 = ["{a,b,c}"]
    )
    maths_question_1_2 = make_field(label="A man’s regular pay is €3 per hour up to 40 hours. Overtime is twice the payment for regular time. If we was paid €168, how many hours overtime did he work?",
    a1 = ["8"],
    a2 = ["16"],
    a3 = ["28"],
    a4 = ["48"]
    )
    maths_question_1_3 = make_field(label="3 and 4/5 expressed as a decimal is: ",
    a1 = ["3.40"],
    a2 = ["3.45"],
    a3 = [" 3.50"],
    a4 = ["3.80"]
    )
    maths_question_1_4 = make_field(label="Which of the following is the highest common factor of 18, 24, and 36?",
    a1 = ["6"],
    a2 = ["18"],
    a3 = ["36"],
    a4 = ["72"]
    )       
    maths_question_1_5 = make_field(label="Which of the following is equal to 3y(x – 3) -2(x – 3) ?", # note this is modified from JPE because difficult to code superscripts. Taken from here: https://www.math-only-math.com/math-questions-answers.html
    a1 = ["(x – 3)(x – 3)"],
    a2 = ["2y(x – 3)"],
    a3 = ["(x – 3)(3y – 2)"],         
    a4 = ["3y(x – 3)"]
    )    
    
    maths_question_2_1 = make_field(label="Items bought by a trader for £80 are sold for £100. The profit expressed as a percentage of cost price is: ",
    a1 = ["2.5%"],
    a2 = ["20%"],
    a3 = ["25%"],
    a4 = ["50%"]
    )
    maths_question_2_2 = make_field(label="A man bought a shirt at a sale. He saves €30 on the normal price when he paid €120 for the shirt. What was the percentage discount on the shirt?",
    a1 = ["20%"],
    a2 = ["25%"],
    a3 = ["33.33%"],
    a4 = ["80%"]
    )
    maths_question_2_3 = make_field(label="How many subsets does {a,b,c,d,e} have?",
    a1 = ["2"],
    a2 = ["4"],
    a3 = ["10"],
    a4 = ["32"]
    )
    maths_question_2_4 = make_field(label="What is the median of the given data: 13, 16, 12, 14, 19, 14, 13, 14",
    a1 = ["14"],
    a2 = ["19"],
    a3 = ["12"],
    a4 = ["14.5"]
    )    
    maths_question_2_5 = make_field(label="In coordinate geometry, what is the equation of the x-axis?",
    a1 = ["y = 0 "],
    a2 = ["x = y"],
    a3 = ["3x = 0"],
    a4 = ["y = 1"]
    )       
    timeout_occured = models.BooleanField()


# PAGES
class instructions(Page):
    
    def is_displayed(player):
        return (player.round_number == 1 or player.round_number == 3)

    def vars_for_template(player):
        current_round = player.round_number
        if current_round == 1:
            task_order_alph = "first"
            task_order_num = 1
        else:
            task_order_alph = "second"
            task_order_num = 2
        print(current_round)
        if current_round in player.participant.performer_task_rounds['maths']: 
            template = "performer_task/maths_instructions_template.html"  
            task = "Maths"
            timeout = round(Constants.maths_timeout_seconds/60)
        elif current_round in player.participant.performer_task_rounds['empathy']: 
            template = "performer_task/empathy_instructions_template.html"  
            task = "Empathy"
            timeout = round(Constants.empathy_timeout_seconds/60)
        return dict(
            template = template,
            task_order_alph = task_order_alph,
            task_order_num = task_order_num,
            task = task,
            timeout = timeout

        )



class task_page(Page):
    form_model = 'player'

    def get_timeout_seconds(player):
        if player.round_number in player.participant.performer_task_rounds['maths']: 
            timeout_seconds = Constants.maths_timeout_seconds
        elif player.round_number in player.participant.performer_task_rounds['empathy']:
            timeout_seconds = Constants.empathy_timeout_seconds
        return timeout_seconds


    def get_form_fields(player):
        current_round = player.round_number
        if current_round in player.participant.performer_task_rounds['maths']: 
            if (current_round == 1 or current_round == 3):
                form_fields = [
                            'maths_question_1_1',
                            'maths_question_1_2',
                            'maths_question_1_3',
                            'maths_question_1_4',
                            'maths_question_1_5'
                            ]
                return form_fields
            elif (current_round == 2 or current_round == 4):
                form_fields = [
                            'maths_question_2_1',
                            'maths_question_2_2',
                            'maths_question_2_3',
                            'maths_question_2_4',
                            'maths_question_2_5'
                            ]
                return form_fields

    def vars_for_template(player):
        current_round = player.round_number
        if current_round in player.participant.performer_task_rounds['maths']: 
            task = 'Maths'
            timeout = round(Constants.maths_timeout_seconds/60)
            if (current_round == 1 or current_round == 3):
                template = "performer_task/maths_round_1_template.html"  
                display_round = 1
            elif (current_round == 2 or current_round == 4):            
                template = "performer_task/maths_round_2_template.html"
                display_round = 2
        elif current_round in player.participant.performer_task_rounds['empathy']:
            task = 'Empathy'
            timeout = round(Constants.empathy_timeout_seconds/60)
            if (current_round == 1 or current_round == 3):
                template = "performer_task/empathy_round_1_template.html"  
                display_round = 1
            elif (current_round == 2 or current_round == 4):            
                template = "performer_task/empathy_round_2_template.html"  
                display_round = 2     
        return dict(
            template = template,
            display_round = display_round,
            task = task,
            timeout = timeout
            )

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.timeout_occured = True


page_sequence = [instructions, task_page]
