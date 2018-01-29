import urllib
import json
import os
from flask import Flask
from flask import make_response
from flask import request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res,indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'

def makeWebhookResult(req):
    if req.get('result').get('action') != 'lottery-intent':
        return{}
    result = req.get('result')
    parameters = result.get('parameters')
    date = parameters.get('date')

    winning_numbers = {"01/27/2018" : ["17-21-26-47-54-07", "2"], "01/24/2018" : ["05-09-11-33-64-21", "3"],
                       "01/20/2018": ["26-28-47-49-58-03", "8"]}

    speech = " The Winning Numbers for " + date + "are" + str(winning_numbers[date][0]) + "and the multiplier is" + \
             str(winning_numbers[date][1])

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
   # app.run()
   port = int(os.getenv('PORT', 5000))

   print("Starting app on port %d" % port)

   app.run(debug=True, port=port, host='0.0.0.0')
