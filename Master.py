from flask import Flask, render_template, request
import nexmo


client = nexmo.Client(key="5827c039", secret="t6ixFVYXNDfwjNd8")

Callers_names = {}
caller_status = {}
wrong_answer = "No, not quite. Try again."

def read_QA(filename = "questions.csv"):
  # reads 1st col as questions
  # and second col as answer
  # return array with matrix[0][0...n] with questions
  # and matrix[1][0...n] with respective answers
  Q = {}
  A1 = {}
  A2 = {}
  
  import csv
  with open(filename) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    index = 0
    for row in spamreader:
      Q[index] = row[0]
      A1[index] = row[1]
      A2[index] = row[2]
      index = index + 1
  return(Q,A1,A2)
def is_first(number,message):
  if number not in Callers_names:
    Callers_names[number] = message
    caller_status[number] = -1
def move_in_game(number,message):
  print("Message from:" + Callers_names[number] + "; Text: "+message)
  # first time caller?
  if caller_status[number] == -1:
    first_msg = "Hi " + Callers_names[number] + ", this is Alice. We need your help!"
    send_message(number=number, text = first_msg)
    answer_correct = True
  else:
    answer_correct = eval_A(QAs=QA_matrix,index=caller_status[number],message=message)
  if answer_correct == True:
      caller_status[number] = caller_status[number] +1
      ask_question(QAs=QA_matrix,number=number,state_in_game=caller_status[number])
      last_question = has_won(QAs=QA_matrix,number=number)
      if last_question == True:
        caller_status[number] = -1

  else:
    send_message(number=number,text=wrong_answer)
def eval_A(QAs,index,message):
  # QAs is the Q and A matrix from read_QA()
  if message == QAs[1][index] or message == QAs[2][index]:
    print("Answer correct")
    res = True
  else:
    res = False
    print("Answer false")
  return(res)
def play(number,message):
  is_first(number=number,message=message)
  move_in_game(number=number,message=message)
def ask_question(QAs,number,state_in_game):
  Question = QAs[0][state_in_game]
  send_message(number=number,text=Question)
def has_won(QAs,number):
  print(len(QAs))
  print(caller_status[number]-1)
  finished = len(QAs) == caller_status[number]
  return finished
  

QA_matrix = read_QA(filename="questions.csv")



app = Flask(__name__)
print("loading")
app.debug = True


@app.route('/',methods=["GET"])
def main():  
    return render_template('main.html')

callHistory = {}

@app.route('/webhooks/inbound-sms', methods=['GET', 'POST'])
def inbound_sms():
    data = request.args
    # print(data)
    inbound = str(data.get("msisdn"))
    text = data.get("text")
    # print(inbound)
    play(number=inbound,message=text)
    return ('', 204)

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

    app.run(port=3000)
