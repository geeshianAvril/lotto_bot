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

    winning_numbers0 = {"2017-12-30": "12-15-23-29,  Multi: 2,  Letter: M",
                                      "2017-12-27": "8-12-19-25, Multi: 3, Letter: B, Jackpot:37,000",
                                      "2017-12-23": "6-13-27-29, Multi: 3, Letter: G, Jackpot:35,500",
                                      "2017-12-20": "2-5-10-17, Multi: 3, Letter: E, Jackpot:33,500",
                                      "2017-12-16": "1-7-14-16, Multi: 3, Letter: A, Jackpot:31,500",
                                      "2017-12-14": "6-14-15-26, Multi: 3, Letter: C, Jackpot:31,000",
                                      "2017-12-09": "1-3-14-27, Multi: 3, Letter: G, Jackpot:29,000",
                                      "2017-12-06": "2-19-25-29, Multi: 1, Letter: B, Jackpot:27,500",
                                      "2017-12-02": "8-14-17-30, Multi: 4, Letter: H, Jackpot:26,000"}


    winning_numbers1 = {"2017-12-29":  "9-10-13-20-25-27, Multi: E, Jackpot:245,000",
                                     "2017-12-27":  "7-10-15-18-27-28, Multi: L, Jackpot:240,000",
                                     "2017-12-22":  "5-9-13-17-21-28,  Multi: L, Jackpot:235,000",
                                     "2017-12-19":  "1-2-5-7-12-14,  Multi: G,  Jackpot:230,000",
                                     "2017-12-15":  "1-2-12-14-25-28, Multi: G, Jackpot:225,000",
                                     "2017-12-12":  "1-5-6-9-10-19, Multi: F, Jackpot:220,000",
                                     "2017-12-08":  "3-12-19-20-22-23, Multi: N, Jackpot:215,000",
                                     "2017-12-05":  "2-15-21-24-25-27, Multi: H, Jackpot:210,000",
                                     "2017-12-01":  "7-10-15-18-21-27, Multi: J, Jackpot:205,000"}

    winning_numbers = winning_numbers0
    if game != "Super six":
        winning_numbers = winning_numbers1

    win_num = str(winning_numbers[date])
    #win_letter = str(winning_numbers[game][date][2])
    speech = " The Winning Numbers for " + " " + date + " are " + win_num

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
