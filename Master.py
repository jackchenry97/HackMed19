from flask import Flask, render_template, request
import nexmo

app = Flask(__name__)
print("loading")
app.debug = True

@app.route('/',methods=["GET"])
def main():  
    return render_template('main.html')

#Variables
client = nexmo.Client(key="5827c039", secret="t6ixFVYXNDfwjNd8")
no_questions = 11
Q = [0]*no_questions
A1 = [0]*no_questions
A2 = [0]*no_questions
A3 = [0]*no_questions
callers_names = {}
caller_status = {}
callers_score = {}
callers_history = []
wrong_answer = "Please try again"
score = 0

#opening questions
def read_QA(filename = "questions.csv"):
  import csv
  with open(filename) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    i = 0
    for row in spamreader:
      Q[i] = row[0]
      A1[i] = row[1]
      A2[i] = row[2]
      A3[i] = row[3]
      i = i + 1
  return(Q, A1, A2, A3)
QA_matrix = read_QA(filename="questions.csv")
print(QA_matrix)

#recieve message
@app.route('/webhooks/inbound-sms', methods=['GET', 'POST'])
def inbound_sms():
    data = request.args
    # print(data)
    inbound = str(data.get("msisdn"))
    text = data.get("text")
    # print(inbound)
    play(inbound, text)
    return ('', 204)

#idk put in recieve message?
def play(number, message):
  if number not in callers_history:
    callers_history.append(number)
    caller_status[number] = -2
  move_in_game(number, message)
 

#main game logic
def move_in_game(number, message):
  index = caller_status[number]
  name = str(callers_names.get(number))
  progress = False
  print("Incomming message from:" + name + "; playing question: " + str(index) + " replying " + message)
  if index == -2:
    first_msg = "Hi please reply with your name"
    send_message(number, first_msg)
    callers_score[number] = 0
    progress = True
  elif index == -1:
    callers_names[number] = message
    second_message = "Hello " + callers_names[number] + ", let's get started!"
    send_message(number, second_message)
    send_message(number, QA_matrix[0][0])
    progress = True
  elif index > -1 and index < 4:
    progress = eval_A(QA_matrix, index, message)
  elif index > 3:
    if message == "1" or "a": 
      callers_score[number] += int(QA_matrix[1][index])
      progress = True
    elif message == "1" or "b": 
      callers_score[number] += int(QA_matrix[2][index])
      progress = True
    elif message == "1" or "c": 
      callers_score[number] += int(QA_matrix[3][index])
      progress = True
  
  if progress == True:
      caller_status[number] = caller_status[number] +1
      if index > -1 and index < no_questions:
        send_message(number, QA_matrix[0][index+1])
      elif (no_questions) == index:
        end_game(number)
  else:
    send_message(number, wrong_answer)

def end_game(number):
  win_score = 17
  lose_score = 10
  win_answer = "Congratulations! You stopped the crazy anti-vaxxers and saved the world! Well if not the world then at least this newborns life then. You convinced the mother to get all of the vaccines. If you want to play again, just send a new message to this number."
  medium_answer = "Congratulations! Well sort of? You almost convinced the mother to get the vaccines but avoided some of them. Luckily the child was able to survive without her immunisations through heard immunity."
  lose_answer = "Oh dear. You have lost to the crazy anti-vaxxers. You were not persuasive enough to the mother and she decided not to get any vaccines. The daughter was not one of the lucky ones to survive through heard immunity and died of the measles and this is on you. If you want to try again, just send a new message to this number."

  if score >= win_score:
    send_message(number, win_answer)
  elif score < win_score and score >= lose_score:
    send_message(number, medium_answer)
  else:
    send_message(number, lose_answer) 
  caller_status[number] = -2

#check if answer is correct
def eval_A(QA_matrix, index, message):
  if message == QA_matrix[1][index] or message == QA_matrix[2][index] or message == QA_matrix[3][index]:
    print("Answer correct")
    result = True
  else:
    result = False
    print("Answer false")
  return(result)

def send_message(number, text):
    print("sending " + text + " to " + number)
    responseData = client.send_message(
    {
        "from": "447937946988",
        "to": number,
        "text": text,
    })
    # print(responseData)
    return ("Sent")
  

if __name__ == '__main__':

    app.run(port=5000)
