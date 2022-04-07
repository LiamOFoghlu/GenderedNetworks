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
    maths_timeout_seconds = 200   
    childcare_timeout_seconds = 70


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    if subsession.round_number == 1:
        import itertools

        #randomise task order
        t_o = itertools.cycle([1, 2]) # maths = 1, childcare = 2
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
            if t_o == 1:
                player.participant.task_order == "Maths first"
            else:
                player.participant.task_order == "Childcare first"


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    task_order = models.StringField()
    timeout_occured = models.BooleanField()
    correct_answers = models.IntegerField()

    ## maths questions
    # round 1
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

    # round 2
    maths_question_2_1 = models.StringField(
       label="A trader takes out a loan of £120 with 10 percent interest. They buy a painting with this money and sell it for £165. What is the trader's profit as a percentage of total costs?",
    choices = [
        "15%",
        "25%", # correct
        "35%", 
        "40%" 
    ],
    widget = widgets.RadioSelectHorizontal
    )
    maths_question_2_2 = models.StringField(
        label="Tomorrow there is a one in nine chance it rains and a one in seven chance that a letter arrives in the post. What is the probability that it rains and a letter doesn't arrive in the post?",
        choices = [
            "0.968", 
            "0.095", # correct
            "0.016",
            "0.143"
        ],
        widget = widgets.RadioSelectHorizontal  
    )     
    maths_question_2_3 = models.StringField(
        label="A data company charges £12 per hour when average server load is below 250MB, with a £2 per hour surcharge when it is above 250MB. For a 24 hour period, the company charges a client £16 in surcharges. If the client randomly inspects an hour's server load, what is the chance it exceeds 250MB?",
        choices = [
            "1 in 8",
            "1 in 6", 
            "1 in 4",
            "1 in 3" # correct
        ],
        widget = widgets.RadioSelectHorizontal
    )
    maths_question_2_4 = models.StringField(
        label="On windy days an archer hits the target two out of every five shots. On still days they hit the target three out of every five shots. On a still day they hit the target 225 times. How many shots did they take?",
        choices = [
            "325",
            "350", 
            "375", # correct
            "400"
        ],
        widget = widgets.RadioSelectHorizontal  
    )    
    maths_question_2_5 = models.StringField(
        label="When it snows a car's transmission and connecting rod will break. When it rains, a car's transmission or oil will break. When it hails a car's air duct or camshaft will break. And when there is strong wind, a car's connecting rod and camshaft will break. On one journey, the transmission and camshaft break. On the journey there was...",
        choices = [
            "rain and snow",
            "rain and hail", # correct
            "strong wind and snow",
            "hail and strong wind"
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

    # round 2
    childcare_question_2_1 = models.StringField(
        label= "Toddlers who can walk...",
        choices = [
            "Shouldn't be active for more than one hour a day",
            "Should be active at least three hours a day",
            "Shouldn't jump or skip too much",
            "Should stretch their legs three times a week"
        ],
        widget = widgets.RadioSelectHorizontal
    ) 
    childcare_question_2_2 = models.StringField(
        label= "Two-year old toddlers can...",
        choices = [
            "Combine multiple words",
            "Speak in full sentences",
            "Only use nouns",
            "Use the future tense"
        ],
        widget = widgets.RadioSelectHorizontal
    )      
    childcare_question_2_3 = models.StringField(
        label= "Two year old toddlers...",
        choices = [
            "Usually can't run yet",
            "Can't grip objects",
            "Can walk backwards",
            "Can throw small weights several metres"
        ],
        widget = widgets.RadioSelectHorizontal
    )      
    childcare_question_2_4 = models.StringField(
        label= "By the time they are two years old toddlers can...",
        choices = [
            "Ask questions",
            "Use pronouns for themselves and others",
            "Understand instructions",
            "Use relative clauses"
        ],
        widget = widgets.RadioSelectHorizontal
    )           
    childcare_question_2_5 = models.StringField(
        label= "Toddlers who meet other toddlers...",
        choices = [
            "Often fight with them",
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
            timeout = str(Constants.maths_timeout_seconds) + " seconds"
        elif current_round in player.participant.performer_task_rounds['childcare']: 
            template = "performer_task/childcare_instructions_template.html"  
            task = "Childcare"
            timeout = str(Constants.childcare_timeout_seconds) + " seconds"
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
            if (current_round == 1 or current_round == 3):
                template = "performer_task/maths_round_1_template.html"  
                display_round = 1
            elif (current_round == 2 or current_round == 4):            
                template = "performer_task/maths_round_2_template.html"
                display_round = 2
        elif current_round in player.participant.performer_task_rounds['childcare']:
            task = 'Childcare'
            if (current_round == 1 or current_round == 3):
                template = "performer_task/childcare_round_1_template.html"  
                display_round = 1
            elif (current_round == 2 or current_round == 4):            
                template = "performer_task/childcare_round_2_template.html"  
                display_round = 2     
        return dict(
            template = template,
            display_round = display_round,
            task = task            )

    def before_next_page(player, timeout_happened):
        current_round = player.round_number

        ## correct answers
        correct_answers = 0

        # maths - round 1
        if current_round in player.participant.performer_task_rounds['maths']: 
            if (current_round == 1 or current_round == 3):
                if player.maths_question_1_1 == "10.50":
                    correct_answers = correct_answers + 1
                if player.maths_question_1_2 == "0.037":
                    correct_answers = correct_answers + 1       
                if player.maths_question_1_3 == "The ranger":
                    correct_answers = correct_answers + 1 
                if player.maths_question_1_4 == "22":
                    correct_answers = correct_answers + 1  
                if player.maths_question_1_5 == "14":
                    correct_answers = correct_answers + 1  
                player.correct_answers = correct_answers

        # maths - round 2
            elif (current_round == 2 or current_round == 4):
                if player.maths_question_2_1 == "25%":
                    correct_answers = correct_answers + 1
                if player.maths_question_2_2 == "0.095":
                    correct_answers = correct_answers + 1       
                if player.maths_question_2_3 == "1 in 3":
                    correct_answers = correct_answers + 1 
                if player.maths_question_2_4 == "375":
                    correct_answers = correct_answers + 1  
                if player.maths_question_2_5 == "rain and hail":
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
