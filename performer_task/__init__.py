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


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    task_order = models.IntegerField()
    timeout_occured = models.BooleanField()
    correct_answers = models.IntegerField()

    ## maths questions
    # round 1
    maths_question_1_1 = models.StringField(
        label = "A driver travels 12 miles in fifteen minutes. They accelerate and travel another 24 miles in thirty minutes. Reaching difficult terrain, they slow down and travel 8 miles for a further fifteen minutes. What is their average speed in miles per hour over this section of the journey?",
        choices = [
            "19",
            "12",
            "17", # correct
            "21"
        ],
        widget = widgets.RadioSelectHorizontal
    ) 
    maths_question_1_2 = models.StringField(
        label="An inefficient factory produces 50 cars per week. On average, 10 per 50 has a fault. An inspector picks 2 cars per week to check. What is the probability both have faults?",
        choices = [
            "0.037", # correct
            "0.025",
            "0.029",
            "0.040"
        ],
        widget = widgets.RadioSelectHorizontal
    )
    maths_question_1_3 = models.StringField(
        label = "A wizard has a 1 in 7 chance of killing a troll with a fireball, and can throw two fireballs a minute. A hobbit has a 1 in 4 chance of killing the troll with his sword and can strike the troll once every 2 minutes. An elf has a 1 in 9 chance of killing the troll with his spear and can strike every minute. A ranger has a 1 in 8 chance of killing a troll with his fists and can punch 4 times a minute. Who will kill the troll first?",
        choices = [
            "The wizard",
            "The hobbit",
            "The elf",
            "The ranger" # correct
        ],
         widget = widgets.RadioSelectHorizontal
    )   
    maths_question_1_4 = models.StringField(
        label="Manchester United have a two in three chance of winning when Rashford plays and a two in five chance of winning when he doesn't. Rashford plays 33 matches out of 38 in a season. About how many matches should Manchester United win?",
        choices = [
            "22",
            "24", # correct
            "21", 
            "27"
        ],
        widget = widgets.RadioSelectHorizontal
    ) 
    maths_question_1_5 = models.StringField(
        label="Salah can try and dribble past the defender and then shoot the ball, or he can try and shoot past the defender. If he successfully dribbles past the defender he will certainly score, if he shoots past the defender he has a 4 in 5 chance of scoring. If the defender is left-footed, Salah can dribble past him for sure if he tries. If the defender is right-footed, Salah will have a 1 in 2 chance of losing the ball if he tries to dribble past him. Salah should try to dribble past the defender if the chances of the defender being left-footed is no less than...",
        choices = [
            "8 in 10",
            "6 in 10", # correct
            "5 in 10", 
            "7 in 10"
        ],
        widget = widgets.RadioSelectHorizontal  
    )    

    # round 2
    maths_question_2_1 = models.StringField(
       label="A trader takes out a loan of £120 with 5 percent interest. They buy a painting with this money and sell it for £238. There is a £10 transaction fee. What is the trader's profit as a percentage of total costs?",
    choices = [
        "79%",
        "75%", # correct
        "72%", 
        "70%" 
    ],
    widget = widgets.RadioSelectHorizontal
    )
    maths_question_2_2 = models.StringField(
        label="Tomorrow there is a one in nine chance it rains and a one in seven chance that a letter arrives in the post. What is the probability that it rains and a letter doesn't arrive in the post?",
        choices = [
            "0.095", # correct
            "0.968",
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
        label="When it snows a car's transmission and connecting rod will break. When it rains, a car's transmission or oil will break. When it hails a car's air duct or camshaft will break. And when there is strong wind, a car's connecting rod and camshaft will break. On one journey, the transmission and camshaft break. On the journey there was...",
        choices = [
            "rain and snow",
            "rain and hail", # correct
            "strong wind and snow",
            "hail and strong wind"
        ],
        widget = widgets.RadioSelectHorizontal
    )    
    maths_question_2_5 = models.StringField(
        label= "Messi cares only about winning, but Neymar is a glory hunter. Messi has the ball at the edge of the box. If he shoots now, he has a 3 in 10 chance of scoring. If he passes to Neymar, Neymar might shoot even though he has only a 1 in 8 chance of scoring. But if Neymar passes back to Messi, then Messi will definitely score. Messi should pass the ball if the chance of Neymar passing it back is at least…",
        choices = [
            "1 in 4",
            "1 in 2",
            "1 in 5", # correct
            "3 in 10"
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
            timeout = Constants.maths_timeout_seconds
        elif current_round in player.participant.performer_task_rounds['childcare']: 
            template = "performer_task/childcare_instructions_template.html"  
            task = "Childcare"
            timeout = Constants.childcare_timeout_seconds
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
                if player.maths_question_1_1 == "17":
                    correct_answers = correct_answers + 1
                if player.maths_question_1_2 == "0.037":
                    correct_answers = correct_answers + 1       
                if player.maths_question_1_3 == "The ranger":
                    correct_answers = correct_answers + 1 
                if player.maths_question_1_4 == "24":
                    correct_answers = correct_answers + 1  
                if player.maths_question_1_5 == "6 in 10":
                    correct_answers = correct_answers + 1  
                player.correct_answers = correct_answers

        # maths - round 2
            elif (current_round == 2 or current_round == 4):
                if player.maths_question_2_1 == "75%":
                    correct_answers = correct_answers + 1
                if player.maths_question_2_2 == "0.095":
                    correct_answers = correct_answers + 1       
                if player.maths_question_2_3 == "1 in 3":
                    correct_answers = correct_answers + 1 
                if player.maths_question_2_4 == "rain and hail":
                    correct_answers = correct_answers + 1  
                if player.maths_question_2_5 == "1 in 5":
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
