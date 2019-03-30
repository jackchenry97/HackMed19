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


@app.route('/webhooks/inbound-sms', methods=['GET', 'POST'])
def inbound_sms():
    if request.is_json:
        pprint(request.get_json())
        print("json")
    else:
        data = dict(request.form) or dict(request.args)
        pprint(data)
        print(data)
    
    return ('', 204)

@app.route('/webhooks/outbound-sms',methods=["GET", "POST"])
def sendMessage():
    responseData = client.send_message(
    {
        "from": "HackMed19",
        "to": "447591608879",
        "text": "What",
    })
    return ("okay")





if __name__ == '__main__':
    app.run(port=5000)
