from os import environ

SESSION_CONFIGS = [
    dict(
        name='performer_task',
        app_sequence=['performer_intro', 'performer_task', 'performer_debrief'],
        num_demo_participants=8,
    ),
    dict(
        name='referrer_task',
        app_sequence=['referrer_intro', 'referrer_task', 'referrer_debrief'],
        num_demo_participants=8,
    ),
    dict(
        name='selector_task',
        app_sequence=['selector_intro', 'selector_task', 'selector_debrief'],
        num_demo_participants=8,
    ),   
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [
    'performer_round_numbers',       # a list definining the order in which maths and empathy tasks should be shown
    'performer_start_epochtime',     # a scalar recording the epoch time the participant entered
    'performer_task_rounds',         # a dictionary with key = task and value = round in which task is displayed
    'performer_maths_r',             # random maths profile
    'performer_empathy_r',           # random empathy profile
    'performer_task_order',          # 1 = maths first; 2 = empathy first
    'performer_name_choices',        # a list with a random selection of common german first names
    'referrer_round_numbers',       # a list definining the order in which maths and empathy tasks should be shown
    'referrer_start_epochtime',     # a scalar recording the epoch time the participant entered
    'referrer_task_rounds',         # a dictionary with key = task and value = round in which task is displayed
    'referrer_maths_r',             # random maths profile
    'referrer_empathy_r',           # random empathy profile
    'referrer_task_order',          # 1 = maths first; 2 = empathy first
    'referrer_mathspractice_q1',
    'referrer_mathspractice_q2',
    'referrer_empathypractice_q1',
    'referrer_empathypractice_q2',
    'referrer_any_referral',        # did the referrer make a referral?
    'referrer_name_choices',        # a list with a random selection of common german first names
    'selector_round_numbers',       # a list definining the order in which maths and empathy tasks should be shown
    'selector_start_epochtime',     # a scalar recording the epoch time the participant entered
    'selector_task_rounds',         # a dictionary with key = task and value = round in which task is displayed
    'selector_maths_r',             # random maths profile
    'selector_empathy_r',           # random empathy profile
    'selector_task_order',          # 1 = maths first; 2 = empathy first
    'selector_maths_practice_qs'    # list of the randomsied index of maths questions
]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7243391824297'
