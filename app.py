import urllib
import logging
import json
import os
from flask import Flask
from flask import make_response
from flask import request
import psycopg2

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


def makeWebhookResult(req):
    if req.get('result').get('action') != 'lottery-intent':
        return{}
    conn_string = "host='ec2-54-235-64-195.compute-1.amazonaws.com' dbname=d2fjg5inmb4pta user='dcudkoeyfioakr' password='0984fa768adc6681ee0955a7848b0a7a714846e73fc9a033bae80a7b48216be2'"

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()


    result = req.get('result')
    parameters = result.get('parameters')
    date = parameters.get('date')
    game = parameters.get('game-options')

    if result == 'Lucky 3':
        selectstatement = ''' SELECT  FROM public.LuckyThree where "date" = %s'''
        cursor.execute(selectstatement,(data,))
        records = cursor.fetchone()


        speech = "The result for Lucky 3 is " + str(records[1:3])



        return {
           "speech": speech,
           "displayText": speech,
            # "data": {},
            # "contextOut": [],
           "source": "lotto-bot-test",

               }




    else if result == 'Power Play':
        selectstatement = '''SELECT * FROM public.PowerPlay where "date" = %s'''
        cursor.execute(selectstatement,(data,))
        records = cursor.fetchone()
        speech = "The result for Power Play is " + str(records[1:3])



        return {
           "speech": speech,
           "displayText": speech,
            # "data": {},
            # "contextOut": [],
           "source": "lotto-bot-test",

               }

    else if result == 'Big 4':
        selectstatement = '''SELECT * FROM public.BigFour where "date" = %s'''
        cursor.execute(selectstatement,(data,))
        records = cursor.fetchone()

        speech = "The result for Big 4 is " + str(records[1:3])



        return {
           "speech": speech,
           "displayText": speech,
            # "data": {},
            # "contextOut": [],
           "source": "lotto-bot-test",

               }

    else if result == 'Super Six':

    else if result == 'Double Daily Grand':


    else if result == '1 Off':


    else if result == 'Tic Tac Toe':


    if game not in game_dict:
        return {}


    speech = game_dict[game]

    print("Response:")
    print(speech)

    return {
       "speech": speech,
       "displayText": speech,
        # "data": {},
        # "contextOut": [],
       "source": "lotto-bot-test",

           }


if __name__ == '__main__':
   # app.run()
   port = int(os.getenv('PORT', 5000))

   print("Starting app on port %d" % port)

   app.run(debug=True, port=port, host='0.0.0.0')
