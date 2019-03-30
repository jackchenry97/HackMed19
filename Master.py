from flask import Flask, render_template, request
import nexmo
from pprint import pprint


client = nexmo.Client(key="5827c039", secret="t6ixFVYXNDfwjNd8")

app = Flask(__name__)

app.debug = True

print("OK")

@app.route('/',methods=["GET"])
def main():
    print("loading")
    
    return render_template('main.html')
    

@app.route('/sendMessage',methods=["POST"])
def sendMessage():
    print("Running")
    responseData = client.send_message(
    {
        "from": "HackMed19",
        "to": 447591608879,
        "text": "A text message sent using the Nexmo SMS API",
    })
    return "okay"



@app.route('/webhooks/inbound-sms', methods=['GET', 'POST'])
def inbound_sms():
    if request.is_json:
        pprint(request.get_json())
    else:
        data = dict(request.form) or dict(request.args)
        pprint(data)

    return ('', 204)

if __name__ == '__main__':
    app.run()
