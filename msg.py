greeting = 'What notification do you want to receive?'

# main buttons
choose_main_text = ['🐋Whale inflows',
               '🦜Sopr',
               '👴Hodler volumes',
               '⛰Large transactions']
# main callback data
choose_main_callback = ['whale',
                        'sopr',
                        'volumes',
                        'txes']

# plan keyboard
choose_plan = ['rec',
               'pro']

def plan_choose_func(pro=False, recomended=False):
    buttons = ['❌Recomended',
               '❌Pro']
    if pro:
        buttons[1] = '✔Pro'
    if recomended:
        buttons[0] = '✔Recomended'

    return buttons

# ---- Describing all the planns
whale = ["This is plan for whale inflows",
         '*Pro plan is for pro*',
         'Recomended plan *recomendations*']

sopr = ["This is plan for sopr",
        '*Pro plan is for pro*',
        'Recomended plan sends a notification when SOPR (block resolution) falls below 1. This is usually a good time to buy.']

volumes = ["This is plan for volume hodlers",
           '*Pro plan is for pro*',
           'Recomended plan *recomendations*']

txes = ["This is plan for large transactions",
        '*Pro plan is for pro*',
        'Recomended plan *recomendations*']
# ----
