# values shared between modules


# buttons
# TODO: move into controller.py?
BTN_UP = 'up'
BTN_DOWN = 'down'
BTN_LEFT = 'left'
BTN_RIGHT = 'right'
BTN_SUBMIT = 'submit'

# outcome of world actions
# TODO: move into scene.py?
OUTCOME_STAY = 'stay'
OUTCOME_MOVE = 'move' 
OUTCOME_ENCOUNTER = 'encounter'

# directions in the world scene
# TODO: move into level.py?
DIR_N = 'N'
DIR_S = 'S'
DIR_E = 'E'
DIR_W = 'W'


# window size
# TODO: move some of those into level.py? 
N_CELLS = 16  # zone width and height, in cells
BASE_CELL_SIZE = 16  # pixels
ZOOM = 2  # impacts window size
SCREEN_SIZE = N_CELLS * BASE_CELL_SIZE * ZOOM 

FPS = 60
