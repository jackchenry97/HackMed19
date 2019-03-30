from flask import Flask, render_template, request
import nexmo

client = nexmo.Client(key="5827c039", secret="t6ixFVYXNDfwjNd8")

app = Flask(__name__)

app.debug = True

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



if __name__ == '__main__':
    app.run()