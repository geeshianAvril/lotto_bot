import urllib
import logging
import json
import os
from flask import Flask
from flask import make_response
from flask import request
#import psycopg2
from psycopg2._psycopg import cursor

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-type'] = 'application/json'
    return r


def drawdateResults(req):


    result = req.get('result')
    parameters = result.get('parameters')
    date = parameters.get('date')
    game1 = parameters.get('game-options')

    drawdate_dict = {"Double Daily Grand": ["Double Daily Grand, is played six days a week at 1:30 p.m., Monday through"
                                            "Saturday on public holidays"],

                     "Tic Tac Toe": ["Tic Tac Toe is drawn six (6) days weekly, Monday to Saturday in the evening"],

                     "1 Off": ["1 Off is played 6 days a week at 1:30 p.m. and 9:00 p.m., Monday through Saturday "
                               "with two draws each day except on public holidays."],

                     "Lucky 3": ["Lucky 3 is played 6 days a week at 1:30 p.m. and 9:00 p.m., Monday through "
                                 "Saturday with two draws each day except on public holidays."],

                     "Big 4": ["Big 4 is played 6 days a week at 9:00 p.m., Monday through  "
                               "Saturday with two draws each day except on public holidays."],

                     "Power Play": ["Power Play is played twice weekly on Wednesdays and Saturdays at 9:00 p.m."],

                     "Super Six": ["Super 6 is played twice a week every Tuesday and Friday at 10:00 p.m."]
                     }

    speech = drawdate_dict[game1][0]

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": {},
        # "contextOut": [],
        "source": "lotto-bot-test",

    }


def gameResults(req):

    result = req.get('result')
    parameters = result.get('parameters')
    date = parameters.get('date')
    game = parameters.get('game-options')
    print (result)

    if game == 'Lucky 3':
        selectstatement = ''' SELECT  FROM public.LuckyThree where "date" = %s'''
        cursor.execute(selectstatement,(date,))
        records = cursor.fetchone()


        speech = "The result for Lucky 3 is " + str(records[1:3])



        return {
           "speech": speech,
           "displayText": speech,
            # "data": {},
            # "contextOut": [],
           "source": "lotto-bot-test",

               }




    elif game == 'Power Play':
        selectstatement = '''SELECT * FROM public.PowerPlay where "date" = %s'''
        cursor.execute(selectstatement,(date,))
        records = cursor.fetchone()
        speech = "The result for Power Play is " + str(records[1:3])



        return {
           "speech": speech,
           "displayText": speech,
            # "data": {},
            # "contextOut": [],
           "source": "lotto-bot-test",

               }

    elif game == 'Big 4':
        selectstatement = '''SELECT * FROM public.BigFour where "date" = %s'''
        cursor.execute(selectstatement,(date,))
        records = cursor.fetchone()

        speech = "The result for Big 4 is " + str(records[1:3])



        return {
           "speech": speech,
           "displayText": speech,
            # "data": {},
            # "contextOut": [],
           "source": "lotto-bot-test",

               }

    # elif result == 'Super Six':
    #     return {
    #        "speech": 'speech',
    #        "displayText": 'speech',
    #         # "data": {},
    #         # "contextOut": [],
    #        "source": "lotto-bot-test",
    #
    #            }
    #
    #
    # elif result == 'Double Daily Grand':
    #     return {
    #        "speech": 'speech',
    #        "displayText": 'speech',
    #         # "data": {},
    #         # "contextOut": [],
    #        "source": "lotto-bot-test",
    #
    #            }
    #
    #
    # elif result == '1 Off':
    #     return {
    #        "speech": 'speech',
    #        "displayText": 'speech',
    #         # "data": {},
    #         # "contextOut": [],
    #        "source": "lotto-bot-test",
    #
    #            }
    #
    #
    # elif result == 'Tic Tac Toe':
    #     return {
    #        "speech": 'speech',
    #        "displayText": 'speech',
    #         # "data": {},
    #         # "contextOut": [],
    #        "source": "lotto-bot-test",
    #
    #            }




    return {
       "speech": 'speech',
       "displayText": 'speech',
        # "data": {},
        # "contextOut": [],
       "source": "lotto-bot-test",

           }




def makeWebhookResult(req):

    # delineate between actions to select function
    # if action is lottery-intent use gameResults function

    # action_dict = {"lottery-intent" : gameResults(req),
    #               "drawdate-intent": drawdateResults(req)}

    action = req.get('result').get('action')

    if action == "lottery-intent":
        response = gameResults(req)
        return response
    elif action == "drawdate-intent":
        response = drawdateResults(req)
        return response


if __name__ == '__main__':
   # app.run()
   port = int(os.getenv('PORT', 5000))

   print("Starting app on port %d" % port)

   app.run(debug=True, port=port, host='0.0.0.0')
