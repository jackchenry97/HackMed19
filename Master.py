from flask import Flask, render_template, request
import nexmo

@app.route('/main',methods=["GET"])
def main():
    return render_template('main.html')