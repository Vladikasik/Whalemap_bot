# Whalemap_bot
Whalemap bot allows you to customize which on-chain alerts you  
want to receive. With our bot you will never miss important  
market events by staying on top of what’s happening on the  
blockchain.
# Documentation
##### **_all this documentations have been made especially for artem))_**
### Running bot
dont care its already running
```
git clone -b dev https://github.com/Vladikasik/Whalemap_bot
cd Whalemap_bot
vim config
<token = 'bot token'>
python3 bot.py
```
### Mailing
all as simple as it is
```
from bot import Bot
a = Bot()
a.mailing('sopr', 'Pro', 'simple message')
#           |       |            |
#           1       2            3
# 1 - choose from ('whale', 'sopr', 'volumes', 'txes')
# 2 - choose from ('Pro', 'Recomended')
# 3 - your messsage
```
### Database(json) structure
all this sh*t happens because only strings can be keys in  
json and for groups it is easer for me, to make the values  
of lists int, to simply do the mailing then 
##### groups.json
all values from list of plan are integer
```
{  
    "whale": {  
        "Pro": [],  
        "Recomended": [   
            123123 <- int  
        ]  
    },  
    "sopr": {  
        "Pro": [  
            489989504  
        ], 
        "Recomended": [  
            type(id) = int,
            type(id) = int 
        ]  
    },  
    "volumes": {  
        "Pro": [  
            type(id) = int    
        ],  
        "Recomended": []  
    },  
    "txes": {  
        "Pro": [],  
        "Recomended": []  
    }   
}  
```
##### users.json
while all the keys from users.json are strings
```
{"12312312": <- string key
            ["sopr Recomended", 
            "whale Recomended", 
            "volumes Pro"]
}
```
