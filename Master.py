from flask import Flask, render_template, request
import nexmo


client = nexmo.Client(key="5827c039", secret="t6ixFVYXNDfwjNd8")

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
        if text = "A" or "B":
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
