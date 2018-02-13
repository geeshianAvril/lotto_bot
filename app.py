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


def drawdateResults(req):

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

    result = req.get('result')
    parameters = result.get('parameters')
    date = parameters.get('date')
    game = parameters.get('game-options')

    speech = drawdate_dict[game][0]

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

    winning_numbers = {"Power Play": {"2017-12-30": ["12-15-23-29" "2", "M", "37,500"],
                                      "2017-12-27": ["8-12-19-25", "3", "B", "37,000"],
                                      "2017-12-23": ["6-13-27-29", "3", "G", "35,500"],
                                      "2017-12-20": ["2-5-10-17", "3", "E", "33,500"],
                                      "2017-12-16": ["1-7-14-16", "3", "A", "31,500"],
                                      "2017-12-14": ["6-14-15-26", "3", "C", "31,000"],
                                      "2017-12-09": ["1-3-14-27", "3", "G", "29,000"],
                                      "2017-12-06": ["2-19-25-29", "1", "B", "27,500"],
                                      "2017-12-02": ["8-14-17-30", "4", "H", "26,000"]
                                      },
                       "Super Six": {"2017-12-29": ["9-10-13-20-25-27", "E", "245,000"],
                                     "2017-12-27": ["7-10-15-18-27-28", "L", "240,000"],
                                     "2017-12-22": ["5-9-13-17-21-28", "L", "235,000"],
                                     "2017-12-19": ["1-2-5-7-12-14", "G", "230,000"],
                                     "2017-12-15": ["1-2-12-14-25-28", "G", "225,000"],
                                     "2017-12-12": ["1-5-6-9-10-19", "F", "220,000"],
                                     "2017-12-08": ["3-12-19-20-22-23", "N", "215,000"],
                                     "2017-12-05": ["2-15-21-24-25-27", "H", "210,000"],
                                     "2017-12-01": ["7-10-15-18-21-27", "J", "205,000"]
                                     },
                       "Big 4": {"2018-01-31": ["9-6-5-3", "5-4-5-2", " "],
                                 "2018-01-30": ["1-7-6-4", "1-3-0-0", " "],
                                 "2018-01-29": ["4-8-7-9", "2-6-2-5", " "],
                                 "2018-01-27": ["9-6-5-3", "5-4-5-2", " "],
                                 "2018-01-26": ["1-7-6-4", "1-3-0-0", " "],
                                 "2018-01-25": ["4-8-7-9", "2-6-2-5", " "],
                                 "2018-01-24": ["9-6-5-3", "5-4-5-2", " "],
                                 "2018-01-23": ["1-7-6-4", "1-3-0-0", " "],
                                 "2018-01-22": ["4-8-7-9", "2-6-2-5", " "],
                                 "2018-01-21": ["9-6-5-3", "5-4-5-2", " "],
                                 "2018-01-20": ["1-7-6-4", "1-3-0-0", " "],
                                 "2018-01-19": ["4-8-7-9", "2-6-2-5", " "],
                                 "2017-12-30": ["5-7-9-0", "1-4-9-5", " "],
                                 "2017-12-29": ["4-1-3-3", "3-9-5-4", " "],
                                 "2017-12-28": ["1-5-5-4", "8-6-3-1", " "],
                                 "2017-12-27": ["4-9-4-7", "1-5-6-9", " "],
                                 "2017-12-23": ["5-0-6-3", "2-3-7-1", " "],
                                 "2017-12-22": ["8-2-3-5", "9-4-6-4", " "],
                                 "2017-12-21": ["2-5-8-2", "8-1-6-7", " "],
                                 "2017-12-20": ["3-7-3-6", "6-1-7-8", " "],
                                 "2017-12-19": ["3-6-0-5", "1-5-9-0", " "],
                                 "2018-01-18": ["9-6-5-3", "5-4-5-2", " "],
                                 "2018-01-17": ["1-7-6-4", "1-3-0-0", " "],
                                 "2018-01-16": ["4-8-7-9", "2-6-2-5", " "],
                                 "2018-01-15": ["9-6-5-3", "5-4-5-2", " "],
                                 "2018-01-14": ["1-7-6-4", "1-3-0-0", " "],
                                 "2018-01-13": ["4-8-7-9", "2-6-2-5", " "],
                                 "2018-01-12": ["9-6-5-3", "5-4-5-2", " "],
                                 "2018-01-11": ["1-7-6-4", "1-3-0-0", " "],
                                 "2018-01-10": ["4-8-7-9", "2-6-2-5", " "],
                                 "2018-01-09": ["9-6-5-3", "5-4-5-2", " "],
                                 "2018-01-08": ["1-7-6-4", "1-3-0-0", " "],
                                 "2018-01-07": ["4-8-7-9", "2-6-2-5", " "],
                                 "2017-12-06": ["5-7-9-0", "1-4-9-5", " "],
                                 "2017-12-05": ["4-1-3-3", "3-9-5-4", " "],
                                 "2017-12-04": ["1-5-5-4", "8-6-3-1", " "],
                                 "2017-12-03": ["4-9-4-7", "1-5-6-9", " "],
                                 "2017-12-02": ["5-0-6-3", "2-3-7-1", " "],
                                 "2017-12-01": ["8-2-3-5", "9-4-6-4", " "],

                                 },

                       "Lucky 3": {"2018-01-31": ["9-1-9", "7-4-2", " "],
                                   "2018-01-30": ["2-4-5", "0-0-4", " "],
                                   "2018-01-29": ["8-5-9", "9-7-7", " "],
                                   "2018-01-27": ["6-3-3", "7-8-9", " "],
                                   "2018-01-26": ["3-2-7", "8-6-6", " "],
                                   "2018-01-25": ["3-4-2", "5-3-3", " "],
                                   "2018-01-24": ["4-7-7", "0-3-1", " "],
                                   "2018-01-23": ["2-4-7", "7-5-7", " "],
                                   "2018-01-22": ["3-4-9", "9-0-4", " "],
                                   "2018-01-21": ["1-1-6", "9-6-1", " "],
                                   "2018-01-20": ["5-7-3", "6-3-1", " "],
                                   "2018-01-19": ["8-8-1", "3-9-3", " "],
                                   "2018-01-18": ["9-1-9", "7-4-2", " "],
                                   "2018-01-17": ["2-4-5", "0-0-4", " "],
                                   "2018-01-16": ["8-5-9", "9-7-7", " "],
                                   "2018-01-15": ["6-3-3", "7-8-9", " "],
                                   "2018-01-14": ["3-2-7", "8-6-6", " "],
                                   "2018-01-13": ["3-4-2", "5-3-3", " "],
                                   "2018-01-12": ["4-7-7", "0-3-1", " "],
                                   "2018-01-11": ["1-1-6", "9-6-1", " "],
                                   "2018-01-10": ["5-7-3", "6-3-1", " "],
                                   "2018-01-09": ["8-8-1", "3-9-3", " "],
                                   "2018-01-08": ["9-1-9", "7-4-2", " "],
                                   "2018-01-07": ["2-4-5", "0-0-4", " "],
                                   "2018-01-06": ["8-5-9", "9-7-7", " "],
                                   "2018-01-05": ["6-3-3", "7-8-9", " "],
                                   "2018-01-04": ["3-2-7", "8-6-6", " "],
                                   "2018-01-03": ["3-4-2", "5-3-3", " "],
                                   "2018-01-02": ["4-7-7", "0-3-1", " "],
                                   "2018-01-01": ["4-7-3", "0-2-1", " "],

                                   },
                       "Double Daily Grand": {"2018-01-31": ["2-5-15-21", " ", "A"],
                                              "2018-01-30": ["2-3-14-21", " ", "A"],
                                              "2018-01-29": ["1-4-12-15", " ", "A"],
                                              "2018-01-27": ["8-10-15-16", " ", "A"],
                                              "2018-01-26": ["5-8-09-13", " ", "A"],
                                              "2018-01-25": ["3-12-14-19", " ", "A"],
                                              "2018-01-24": ["3-15-19-21", " ", "A"],
                                              "2018-01-23": ["8-14-15-18", " ", "A"],
                                              "2018-01-22": ["1-2-4-12", " ", "A"],
                                              "2018-01-20": ["4-6-14-17", " ", "A"],
                                              "2018-01-19": ["5-13-20-22", " ", "A"],
                                              "2018-01-18": ["11-16-17-21", "A", "A"],
                                              "2018-01-17": ["2-5-7-10", " ", "A"],
                                              "2018-01-16": ["11-15-19-21", " ", "A"],
                                              "2018-01-15": ["5-8-09-13", " ", "A"],
                                              "2018-01-14": ["3-12-14-19", " ", "A"],
                                              "2018-01-13": ["3-15-19-21", " ", "A"],
                                              "2018-01-12": ["8-14-15-18", " ", "A"],
                                              "2018-01-11": ["1-2-4-12", " ", "A"],
                                              "2018-01-10": ["4-6-14-17", " ", "A"],
                                              "2018-01-09": ["5-13-20-22", " ", "A"],
                                              "2018-01-08": ["11-16-17-21", " ", "A"],
                                              "2018-01-07": ["2-5-7-10", " ", "A"],
                                              "2018-01-06": ["11-15-19-21", " ", "A"],
                                              "2018-01-05": ["5-8-09-13", " ", "A"],
                                              "2018-01-04": ["3-12-14-19", " ", "A"],
                                              "2018-01-03": ["3-15-19-21", " ", "A"],
                                              "2018-01-02": ["8-14-15-18", " ", "A"],
                                              "2018-01-01": ["1-2-4-12", " ", "A"],

                                              },
                       "1 Off": {"2018-01-31": ["9-1-9", "7-4-2", " "],
                                 "2018-01-30": ["2-4-5", "0-0-4", " "],
                                 "2018-01-29": ["8-5-9", "9-7-7", " "],
                                 "2018-01-27": ["6-3-3", "7-8-9", " "],
                                 "2018-01-26": ["3-2-7", "8-6-6", " "],
                                 "2018-01-25": ["3-4-2", "5-3-3", " "],
                                 "2018-01-24": ["4-7-7", "0-3-1", " "],
                                 "2018-01-23": ["2-4-7", "7-5-7", " "],
                                 "2018-01-22": ["3-4-9", "9-0-4", " "],
                                 "2018-01-21": ["1-1-6", "9-6-1", " "],
                                 "2018-01-20": ["5-7-3", "6-3-1", " "],
                                 "2018-01-19": ["8-8-1", "3-9-3", " "],
                                 "2018-01-18": ["9-1-9", "7-4-2", " "],
                                 "2018-01-17": ["2-4-5", "0-0-4", " "],
                                 "2018-01-16": ["8-5-9", "9-7-7", " "],
                                 "2018-01-15": ["6-3-3", "7-8-9", " "],
                                 "2018-01-14": ["3-2-7", "8-6-6", " "],
                                 "2018-01-13": ["3-4-2", "5-3-3", " "],
                                 "2018-01-12": ["4-7-7", "0-3-1", " "],
                                 "2018-01-11": ["1-1-6", "9-6-1", " "],
                                 "2018-01-10": ["5-7-3", "6-3-1", " "],
                                 "2018-01-09": ["8-8-1", "3-9-3", " "],
                                 "2018-01-08": ["9-1-9", "7-4-2", " "],
                                 "2018-01-07": ["2-4-5", "0-0-4", " "],
                                 "2018-01-06": ["8-5-9", "9-7-7", " "],
                                 "2018-01-05": ["6-3-3", "7-8-9", " "],
                                 "2018-01-04": ["3-2-7", "8-6-6", " "],
                                 "2018-01-03": ["3-4-2", "5-3-3", " "],
                                 "2018-01-02": ["4-7-7", "0-3-1", " "],
                                 "2018-01-01": ["4-7-3", "0-2-1", " "],

                                 },

                       "Tic Tac Toe": {"2018-01-31": ["3-9-11-15-17-18-20", " ", "A"],
                                       "2018-01-30": ["1-2-4-5-6-10-11", " ", " ", "A"],
                                       "2018-01-29": ["4-6-7-11-15-16-19", " ", "A"],
                                       "2018-01-27": ["2-8-12-13-15-17-21", " ", "A"],
                                       "2018-01-26": ["1-4-5-10-15-17-19", " ", "A"],
                                       "2018-01-25": ["2-8-10-12-13-14-18", " ", "A"],
                                       "2018-01-24": ["2-4-5-15-18-19-21", " ", "A"],
                                       "2018-01-23": ["3-6-7-12-13-17-21", " ", "A"],
                                       "2018-01-22": ["7-9-11-15-16-17-20", " ", "A"],
                                       "2018-01-20": ["2-4-6-7-11-14-18", " ", "A"],
                                       "2018-01-19": ["3-9-11-15-17-18-20", " ", "A"],
                                       "2018-01-18": ["1-2-4-5-6-10-11", " ", "A"],
                                       "2018-01-17": ["4-6-7-11-15-16-19", " ", "A"],
                                       "2018-01-16": ["2-8-12-13-15-17-21", " ", "A"],
                                       "2018-01-15": ["1-4-5-10-15-17-19", " ", "A"],
                                       "2018-01-14": ["2-8-10-12-13-14-18", " ", "A"],
                                       "2018-01-13": ["2-4-5-15-18-19-21", " ", "A"],
                                       "2018-01-12": ["3-6-7-12-13-17-21", " ", "A"],
                                       "2018-01-11": ["7-9-11-15-16-17-20", " ", "A"],
                                       "2018-01-10": ["2-4-6-7-11-14-18", " ", "A"],
                                       "2018-01-09": ["3-9-11-15-17-18-20", " ", "A"],
                                       "2018-01-08": ["1-2-4-5-6-10-11", " ", "A"],
                                       "2018-01-07": ["4-6-7-11-15-16-19", " ", "A"],
                                       "2018-01-06": ["2-8-12-13-15-17-21", " ", "A"],
                                       "2018-01-05": ["1-4-5-10-15-17-19", " ", "A"],
                                       "2018-01-04": ["2-8-10-12-13-14-18", " ", "A"],
                                       "2018-01-03": ["2-4-5-15-18-19-21", " ", "A"],
                                       "2018-01-02": ["3-6-7-12-13-17-21", " ", "A"],
                                       "2018-01-01": ["7-9-11-15-16-17-20", " ", "A"],
                                       }

                       }

    # if req.get('result').get('action') != 'lottery-intent':
    #   return{}

    win_num = str(winning_numbers[game][date][0])
    #win_num1 = str(winning_numbers[game][date])
    win_letter = str(winning_numbers[game][date][2])
    e_win_num = str(winning_numbers[game][date][0])
    m_win_num = str(winning_numbers[game][date][1])
    multi_num = str(winning_numbers[game][date][1])
    win_letter2 = str(winning_numbers[game][date][1])

    game_dict = { "Double Daily Grand": "The Winning Numbers for " + game + " on " + date + " are: " + "\n" + "🎫" +
                                        win_num,

                  "Tic Tac Toe": "The Winning Numbers for " + game + " on " + date + " are: " + "\n" + "🎫" + win_num,

                  "1 Off": "The Winning Numbers for " + game + " on " + date + " are: " + "\n Evening: " + "🎫" +
                           e_win_num + " \n Midday: " + "🎫" + m_win_num,

                  "Lucky 3": "The Winning Numbers for " + game + " on " + date + " are: " + "\n Evening: " + "🎫" +
                             e_win_num + "\n Midday: " + "🎫" + m_win_num,

                  "Big 4": "The Winning Numbers for " + game + " on " + date + " are: " + "\n Evening: " + "🎫" +
                           e_win_num + "\n Midday: " + "🎫" + m_win_num,

                  "Power Play": " The Winning Numbers for " + game + " on " + date + " are: " + "\n" + "🎫" + win_num +
                                 " the multiplier: " + multi_num + " and Letter " + win_letter,

                  "Super Six": " The Winning Numbers for " + game + " on " + date + " are: " + "\n" + "🎫" + win_num +
                               " and Letter " + win_letter2
                  }

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




def makeWebhookResult(req):

    # delineate between actions to select function
    # if action is lottery-intent use gameResults function

    action_dict = {"lottery-intent" : gameResults(req),
                   "drawdate-intent": drawdateResults(req)}
    action = req.get('result').get('action')
    if action not in action_dict.keys():
        return{}
    response = action_dict[action]

    return response



if __name__ == '__main__':
   # app.run()
   port = int(os.getenv('PORT', 5000))

   print("Starting app on port %d" % port)

   app.run(debug=True, port=port, host='0.0.0.0')
