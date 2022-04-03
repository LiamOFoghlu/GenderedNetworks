from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'performer_task'
    players_per_group = None
    participation_fee = "£3.25"
    total_reward = 3
    tasks = ['maths', 'childcare']
    rounds_per_task = 2
    num_rounds = len(tasks) * rounds_per_task # this the total number of rounds that will be done by the player (so, if they do 3 rounds of Task A and 3 rounds of Task B, then they will do 3 + 3 = 6 rounds overall)
    questions_per_round = 5
    reward_per_q = "£" + str(total_reward/(questions_per_round*num_rounds))
    if len(reward_per_q) == 2:
        reward_per_q = reward_per_q + ".00"
    elif len(reward_per_q) == 4:
        reward_per_q = reward_per_q + "0"
    maths_timeout_seconds = 5*60    
    childcare_timeout_seconds = 2*60   


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    if subsession.round_number == 1:
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


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    task_order = models.IntegerField()
    timeout_occured = models.BooleanField()
    correct_answers = models.IntegerField()

    ## maths questions
    # round 1
    maths_question_1_1 = models.StringField(
        label = "A shop has an offer: buy 8 kiwis, and every extra kiwi after that is half price. A customer goes to the shop and pays £4.50 for some kiwis. The full price of a kiwi is £0.50. How many does the customer buy?",
        choices = [
            "9",
            "12",
            "10",
            "15"
        ],
        widget = widgets.RadioSelectHorizontal
    ) 
    maths_question_1_2 = models.StringField(
        label="A worker's regular pay is £20 per hour up to 30 hours. Overtime is twice the payment for regular time. If the worker was paid £720, how many hours overtime did they work?",
        choices = [
            "34",
            "32",
            "28",
            "33"
        ],
        widget = widgets.RadioSelectHorizontal
    )
    maths_question_1_3 = models.StringField(
        label="3 and 4/5 expressed as a decimal is:",
        choices = [
            "3.40",
            "3.45",
            "3.80",
            "3.50"
        ],
        widget = widgets.RadioSelectHorizontal
    )
    maths_question_1_4 = models.StringField(
        label="Which of the following is the highest common factor of 18, 24, and 36?",
        choices = [
            "6",
            "18",
            "36",
            "3"
        ],
        widget = widgets.RadioSelectHorizontal  
    )    
    maths_question_1_5 = models.StringField(
        label="Which of the following is equal to 3y(x + 3) - 2(x + 3) ?",
        choices = [
            "(x - 3)(x - 3)",
            "2y(x + 3)",
            "(x + 3)(3y - 2)",
            "3y(x + 3)"
        ],
        widget = widgets.RadioSelectHorizontal  
    )    

    # round 2
    maths_question_2_1 = models.StringField(
       label="Items bought by a trader for £80 are sold for £100. The profit expressed as a percentage of cost price is: ",
    choices = [
        "100%",
        "20%",
        "25%",
        "50%"
    ],
    widget = widgets.RadioSelectHorizontal
    )
    maths_question_2_2 = models.StringField(
        label="A shopper bought five pineapples which cost £2 each, and 4 lemons which cost £0.75 each. How much did they spend?",
    choices = [
        "£10",
        "£16",
        "£20",
        "£13"
    ],
    widget = widgets.RadioSelectHorizontal
    )
    maths_question_2_3 = models.StringField(
        label = "A hairdresser has an offer: every third visit is free. They charge £48 for a haircut. Last year Sarah paid £144 for a haircut. How many times did she go?",
        choices = [
            "Two times",
            "Three times",
            "Four times",
            "Five times"
        ],
         widget = widgets.RadioSelectHorizontal
    )     
    maths_question_2_4 = models.StringField(
        label="What is the average of these numbers: 5, 9, 7",
        choices = [
            "7",
            "9",
            "6",
            "5"
        ],
        widget = widgets.RadioSelectHorizontal
    )    
    maths_question_2_5 = models.StringField(
        label= "A woman walks from the bottom to the top of a hill. She starts at 9.40am and arrives at the top at 10.20 am. She takes a rest for ten minutes. Then she walks back down. On the way down she walks twice as fast as she did on the way up. What time is it when she reaches the bottom of the hill?",
        choices = [
            "11.20",
            "10.40",
            "10.50",
            "11.10"
        ],
        widget = widgets.RadioSelectHorizontal
    )      

    ## childcare questions
    # round 1
    childcare_question_1_1 = models.StringField(
        label= "Babies should be bathed...",
        choices = [
            "Once a day",
            "Once a week",
            "Two to three times a week"
        ],
        widget = widgets.RadioSelectHorizontal
    )      
    childcare_question_1_2 = models.StringField(
        label= "Women should continue on-demand, frequent breastfeeding until the child is:",
        choices = [
            "One year old",
            "Two years old",
            "One and a half years old"
        ],
        widget = widgets.RadioSelectHorizontal
    )      
    childcare_question_1_3 = models.StringField(
        label= "Newborn babies…",
        choices = [
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
            "The first six months of their lives"
        ],
        widget = widgets.RadioSelectHorizontal
    )        
    childcare_question_1_5 = models.StringField(
        label= "Babies can be calmed by...",
        choices = [
            "Moistening their ears",
            "Stroking their back",
            "Tickling their feet"
        ],
        widget = widgets.RadioSelectHorizontal
    )      

    # round 2
    childcare_question_2_1 = models.StringField(
        label= "Toddlers who can walk...",
        choices = [
            "Shouldn't be active for more than one hour a day",
            "Should be active at least three hours a day",
            "Shouldn't jump or skip too much"
        ],
        widget = widgets.RadioSelectHorizontal
    ) 
    childcare_question_2_2 = models.StringField(
        label= "Two-year old toddlers can...",
        choices = [
            "Combine multiple words",
            "Speak in full sentences",
            "Only use nouns"
        ],
        widget = widgets.RadioSelectHorizontal
    )      
    childcare_question_2_3 = models.StringField(
        label= "Two year old toddlers...",
        choices = [
            "Usually can't run yet",
            "Can't grip objects",
            "Can walk backwards"
        ],
        widget = widgets.RadioSelectHorizontal
    )      
    childcare_question_2_4 = models.StringField(
        label= "Two-year old toddlers can...",
        choices = [
            "Ask questions",
            "Use pronouns for themselves and others",
            "Understand instructions"
        ],
        widget = widgets.RadioSelectHorizontal
    )           
    childcare_question_2_5 = models.StringField(
        label= "Toddlers who meet other toddlers...",
        choices = [
            "Completely ignore them",
            "Like to interact and play with them",
            "Play alongside but separate to them"
        ],
        widget = widgets.RadioSelectHorizontal
    )      


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
        if current_round in player.participant.performer_task_rounds['maths']: 
            template = "performer_task/maths_instructions_template.html"  
            task = "Maths"
            timeout = round(Constants.maths_timeout_seconds/60)
        elif current_round in player.participant.performer_task_rounds['childcare']: 
            template = "performer_task/childcare_instructions_template.html"  
            task = "Childcare"
            timeout = round(Constants.childcare_timeout_seconds/60)
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
        elif player.round_number in player.participant.performer_task_rounds['childcare']:
            timeout_seconds = Constants.childcare_timeout_seconds
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
        if current_round in player.participant.performer_task_rounds['childcare']: 
            if (current_round == 1 or current_round == 3):
                form_fields = [
                            'childcare_question_1_1',
                            'childcare_question_1_2',
                            'childcare_question_1_3',
                            'childcare_question_1_4',
                            'childcare_question_1_5'
                            ]
                return form_fields
            elif (current_round == 2 or current_round == 4):
                form_fields = [
                            'childcare_question_2_1',
                            'childcare_question_2_2',
                            'childcare_question_2_3',
                            'childcare_question_2_4',
                            'childcare_question_2_5'
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
        elif current_round in player.participant.performer_task_rounds['childcare']:
            task = 'Childcare'
            timeout = round(Constants.childcare_timeout_seconds/60)
            if (current_round == 1 or current_round == 3):
                template = "performer_task/childcare_round_1_template.html"  
                display_round = 1
            elif (current_round == 2 or current_round == 4):            
                template = "performer_task/childcare_round_2_template.html"  
                display_round = 2     
        return dict(
            template = template,
            display_round = display_round,
            task = task,
            timeout = timeout
            )

    def before_next_page(player, timeout_happened):
        current_round = player.round_number

        ## correct answers
        correct_answers = 0

        # maths - round 1
        if current_round in player.participant.performer_task_rounds['maths']: 
            if (current_round == 1 or current_round == 3):
                if player.maths_question_1_1 == "10":
                    correct_answers = correct_answers + 1
                if player.maths_question_1_2 == "33":
                    correct_answers = correct_answers + 1       
                if player.maths_question_1_3 == "3.80":
                    correct_answers = correct_answers + 1 
                if player.maths_question_1_4 == "6":
                    correct_answers = correct_answers + 1  
                if player.maths_question_1_5 == "(x + 3)(3y - 2)":
                    correct_answers = correct_answers + 1  
                player.correct_answers = correct_answers

        # maths - round 2
            elif (current_round == 2 or current_round == 4):
                if player.maths_question_2_1 == "25%":
                    correct_answers = correct_answers + 1
                if player.maths_question_2_2 == "£13":
                    correct_answers = correct_answers + 1       
                if player.maths_question_2_3 == "Four times":
                    correct_answers = correct_answers + 1 
                if player.maths_question_2_4 == "7":
                    correct_answers = correct_answers + 1  
                if player.maths_question_2_5 == "10.50":
                    correct_answers = correct_answers + 1  
                player.correct_answers = correct_answers

        # childcare - round 1
        if current_round in player.participant.performer_task_rounds['childcare']: 
            if (current_round == 1 or current_round == 3):
                if player.childcare_question_1_1 == "Two to three times a week":
                    correct_answers = correct_answers + 1
                if player.childcare_question_1_2 == "Two years old":
                    correct_answers = correct_answers + 1       
                if player.childcare_question_1_3 == "Sleep in cycles that last about one hour":
                    correct_answers = correct_answers + 1 
                if player.childcare_question_1_4 == "The first six months of their lives":
                    correct_answers = correct_answers + 1  
                if player.childcare_question_1_5 == "Stroking their back":
                    correct_answers = correct_answers + 1  
                player.correct_answers = correct_answers
        # childcare - round 2
            elif (current_round == 2 or current_round == 4):
                if player.childcare_question_2_1 == "Should be active at least three hours a day":
                    correct_answers = correct_answers + 1
                if player.childcare_question_2_2 == "Combine multiple words":
                    correct_answers = correct_answers + 1       
                if player.childcare_question_2_3 == "Can walk backwards":
                    correct_answers = correct_answers + 1 
                if player.childcare_question_2_4 == "Understand instructions":
                    correct_answers = correct_answers + 1  
                if player.childcare_question_2_5 == "Play alongside but separate to them":
                    correct_answers = correct_answers + 1  
                player.correct_answers = correct_answers

        if timeout_happened:
            player.timeout_occured = True
        


page_sequence = [instructions, task_page]
