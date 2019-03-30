from flask import Flask, render_template, request
import nexmo


client = nexmo.Client(key="5827c039", secret="t6ixFVYXNDfwjNd8")

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
QA_matrix = read_QA(filename="questions.csv")

def eval_A(QAs,index,Response):
  # QAs is the Q and A matrix from read_QA()
  # index is the position of the player in the game
  # Reponse is the player's message
  
  print("Response",Response)
  print("QAs[1][index]",QAs[1][index])
  # print("QAs[2][index]",QAs[2][index])
  if Response == QAs[1][index] or Response == QAs[2][index]:
    print("correct")
    res = True
  else:
    res = False
    print("False")
  return(res)
# eval_A(QAs = QA_matrix, index = 0, Response="This is a wrong answer")

app = Flask(__name__)
print("loading")
app.debug = True


@app.route('/',methods=["GET"])
def main():  
    return render_template('main.html')

@app.route('/test',methods=["GET"])
def test():
    print('test')
    return 'test'

callHistory = {}

@app.route('/webhooks/inbound-sms', methods=['GET', 'POST'])
def inbound_sms():
    print('Recieved a message')
    data = request.args
    print(data)

    inbound = str(data.get("msisdn"))
    text = data.get("text")
    print(inbound)

    if  inbound not in callHistory:
        callHistory[inbound] = 1
    else:
        callHistory[inbound] += 1
    identify_sender(inbound, text) 
    return ('', 204)

correct_answer = "Well done thats correct!"
wrong_answer = "Please try again!"

people = {}
first_message = "Please reply with your name"
second_message = "Lets begin the game!"
third_message = "First Question: Blah Blah Blah."
third_answers = "Reply with the letter for the correct answer: A: Apples, B:Monty C:Fall over"

end_message = "You have finished the game"

def identify_sender(inbound, text):
    print(callHistory[inbound])
    if callHistory[inbound] == 1:
        message(inbound, first_message)
    elif callHistory[inbound] == 2:
        people[inbound] = text
        message(inbound, second_message)
        message(inbound, third_message)
        message(inbound, third_answers)
    elif callHistory[inbound] == 3:
        if text == "A" or "B":
            message(wrong_answer)
        else:
            message(correct_answer)





    elif callHistory[inbound] >= 5:
        messgae(inbound, end_message)
        

def message(number, message):
    print("sending " + message + " to " + number)
    responseData = client.send_message(
    {
        "from": "HackMed19",
        "to": number,
        "text": message,
    })
    print(responseData)
    return ("Sent")
  

if __name__ == '__main__':

    app.run(port=5000)
