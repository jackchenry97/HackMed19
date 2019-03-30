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
    

@app.route('/webhooks/outbound-sms',methods=["GET", "POST"])
def sendMessage():
    responseData = client.send_message(
    {
        "from": "HackMed19",
        "to": 447591608879,
        "text": "What",
    })
    return ("okay")



@app.route('/webhook/inbound-sms', methods=['GET', 'POST'])
def inbound_sms():
    print("Method is working")
    if request.is_json:
        print("Its a json")
        print(request.get_json())
    else:
        data = dict(request.form) or dict(request.args)
        
        print("Sender Number:")
        print(data.get("msisdn"))
        
        
        print("Text message:")
        print(data.get("text"))
        # print("Its not a json")
        # pprint(data)
    
    return ('', 204)

if __name__ == '__main__':

    app.run(port=3000)
