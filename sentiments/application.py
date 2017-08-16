from flask import Flask, redirect, render_template, request, url_for

import os
import sys
import helpers
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name, 100)

    # error if timeline not successfully returned
    if tweets == None:
        return redirect(url_for("index"))
    
    # absolute paths to lists
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")
    
    # create analyzer instance
    analyzer = Analyzer(positives, negatives)
    
    # initialize chart variables
    positive, negative, neutral = 0.0, 0.0, 0.0    
    
    # 
    for t in tweets:
        # compute score
        score = analyzer.analyze(t)
        if score > 0.0:
            positive += 1
        if score < 0.0:
            negative += 1
        if score == 0.0:
            neutral += 1            

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
