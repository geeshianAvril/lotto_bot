import urllib
import logging
import json
import os
from flask import Flask
from flask import make_response
from flask import request

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
    result = req.get('result')
    parameters = result.get('parameters')
    date = parameters.get('date')
    game = parameters.get('game')

    # dictionary design
    #winning_numbers = {"Power Play":{"Date": ["numbers", "power_pick", "letter", "Jackpot"]},
    #                   "Super Six": {"Date": ["numbers", "letter", "Jackpot"]}}

    winning_numbers = {"Power Play": {"2017-12-30": ["12-15-23-29" "2", "M", "37,500"],
                                      "2017-12-27": ["8-12-19-25", "3", "B", "37,000"],
                                      "2017-12-23": ["6-13-27-29", "3", "G", "35,500"],
                                      "2017-12-20": ["2-5-10-17", "3", "E", "33,500"],
                                      "2017-12-16": ["1-7-14-16", "3", "A", "31,500"],
                                      "2017-12-14": ["6-14-15-26", "3", "C", "31,000"],
                                      "2017-12-09": ["1-3-14-27", "3", "G", "29,000"],
                                      "2017-12-06": ["2-19-25-29", "1", "B", "27,500"],
                                      "2017-12-02": ["8-14-17-30", "4", "H", "26,000"]},
                       "Super six": {"2017-12-29": ["9-10-13-20-25-27", "E", "245,000"],
                                     "2017-12-27": ["7-10-15-18-27-28", "L", "240,000"],
                                     "2017-12-22": ["5-9-13-17-21-28", "L", "235,000"],
                                     "2017-12-19": ["1-2-5-7-12-14", "G", "230,000"],
                                     "2017-12-15": ["1-2-12-14-25-28", "G", "225,000"],
                                     "2017-12-12": ["1-5-6-9-10-19", "F", "220,000"],
                                     "2017-12-08": ["3-12-19-20-22-23", "N", "215,000"],
                                     "2017-12-05": ["2-15-21-24-25-27", "H", "210,000"],
                                     "2017-12-01": ["7-10-15-18-21-27", "J", "205,000"]}}
    win_num = str(winning_numbers[game][date][0])
    win_letter = str(winning_numbers[game][date][2])
    #win_mul = str(winning_numbers[game][date][])
    speech = " The Winning Numbers for " + game + " on " + date + " are " + win_num + " and Letter " + win_letter

    #speech = " The Winning Numbers for " + " " + date + " are " + str(winning_numbers[date])


    print("Response:")
    print(speech)

    return {
       "speech": speech,
       "displayText": speech,
        # "data": {},
        # "contextOut": [],
      "source": "lotto-bot-test"
    }


if __name__ == '__main__':
   # app.run()
   port = int(os.getenv('PORT', 5000))

   print("Starting app on port %d" % port)

   app.run(debug=True, port=port, host='0.0.0.0')
