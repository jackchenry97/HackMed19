from flask import Flask, render_template, request
import nexmo


client = nexmo.Client(key="5827c039", secret="t6ixFVYXNDfwjNd8")
Q = {}
A = {}

def read_QA(filename = "questions.csv"):
  # reads 1st col as questions
  # and second col as answer
  # return array with matrix[0][0...n] with questions
  # and matrix[1][0...n] with respective answers

  import csv
  with open(filename) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    index = 0
    for row in spamreader:
      Q[index] = row[0]
      A[index] = row[1]
      index = index + 1
      #count how many rows in csv
  return(Q,A)
QA_matrix = read_QA(filename="questions.csv")

app = Flask(__name__)
print("loading")
app.debug = True
read_QA()


@app.route('/',methods=["GET"])
def main():  
    return render_template('main.html')

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

end_message = "You have finished the game"


def identify_sender(inbound, text):
    print(callHistory[inbound])
    if callHistory[inbound] == 1:
        message(inbound, first_message)
    elif callHistory[inbound] == 2:
        people[inbound] = text
        message(inbound, second_message)
        message(inbound, Q[0])
    elif callHistory[inbound] >= 3:
        question_index = callHistory[inbound] -3
        if text == A[question_index]:
            message(inbound, correct_answer)
        else:
            message(inbound, wrong_answer)





    elif callHistory[inbound] >= 5:
        messgae(inbound, end_message)
        

def message(number, message):
    print("sending " + message + " to " + number)
    responseData = client.send_message(
    {
        "from": "447937946988",
        "to": number,
        "text": message,
    })
    print(responseData)
    return ("Sent")
  

if __name__ == '__main__':

    app.run(port=5000)
