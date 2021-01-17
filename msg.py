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
whale = ["Stay up to date on whale bubbles!",
         '\nPro plan is in development',
         '\nRecomended plan sends a notification when a new whale bubble is formed. Bubble is now an important level for Bitcoins price 🏓']

sopr = ["Customise your SOPR",
        '\nPro plan is in development',
        '\nRecomended plan sends a notification when SOPR falls below 1. SOPR < 1 signifies more upside potential for Bitcoin 🔼']

volumes = ["Customise HODLer volumes plan!",
           '\nPro plan is in development',
           '\nRecomended plan sends a notification when HODLer volumes exceed 100BTC per block. High HODLer volumes usually predict higher volatility 🌊']

txes = ["Customise your large transactions plan",
        '\nPro plan is in development',
        '\nRecomended plan sends a notification when more than 5 $20M+ transactions happen on the blockchain. These are time when more volatility can be expected 🌊']
# ----
