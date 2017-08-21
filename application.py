from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    
    # get users current porfolio
    rows = db.execute("SELECT stock, SUM(amount) as amount FROM history WHERE userid = :userid GROUP BY stock HAVING SUM(amount) <> 0", userid = session["user_id"])
    
    # map 
    for row in rows:
        
        # get current stock info
        result = lookup(row["stock"])
        
        # handle errors
        if result == None:
            return apology("could not get stock info")
        
        # map results to rows
        row["name"] = result["name"]
        row["price"] = usd(result["price"])
        row["total"] = usd(result["price"] * row["amount"])
        
        # saves unformatted one to be used in sum
        row["total_unf"] = result["price"] * row["amount"]
    
    # figure out how much cash user has
    cash = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])
    
    # sum value of portfolio
    val = float(cash[0]["cash"])
    for row in rows:
        val += row["total_unf"]

    # render index
    return render_template("index.html", stocks=rows, cash = usd(cash[0]["cash"]), total = usd(val))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # get stock info
        result = lookup(request.form.get("symbol"))
        
        # handle invalid inputs
        if result == None:
            return apology("invalid symbol")
        
        # render apology if number to buy is not a positive int
        try:
            if int(request.form.get("shares")) < 1:
                return apology("number less than 1")
                
        except ValueError:
            return apology("not an integer")

        # select current amt of user money money
        money = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])
        
        # if not enough money to complete transaction, render apology
        if money[0]["cash"] < result["price"] * int(request.form.get("shares")):
            return apology("not enough cash")
        
        # else enough money to buy 
        else:
            
            # update cash in users
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = money[0]["cash"] - (result["price"] * int(request.form.get("shares"))), id = session["user_id"])
            
            # add stock, price, quantity to portfolio
            db.execute("INSERT INTO 'history' (userid, stock, amount, price) VALUES (:userid, :stock, :amount, :price)", userid = session["user_id"], stock = result["symbol"], amount = int(request.form.get("shares")), price = result["price"])
        
            # redirect user to homepage
            flash("Bought!")
            return redirect(url_for("index"))
        
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")
        
        
@app.route("/history")
@login_required
def history():
    """Show history of transactions."""

    # get users transaction history
    rows = db.execute("SELECT stock, amount, price, timestamp FROM history WHERE userid = :userid ORDER BY timestamp desc", userid = session["user_id"])
    
    # format price
    for row in rows:
        row["price"] = usd(row["price"])
    
    # render history
    return render_template("history.html", stocks = rows)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # store stock info
        result = lookup(request.form.get("symbol"))
        
        # handle invalid inputs
        if result == None:
            return apology("invalid symbol")
        
        # render quoted page
        else:    
            return render_template("quoted.html", name = result["name"], symbol = result["symbol"], price = usd(result["price"]))
    
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    
    # if user reached route via POST (as by submitting a form via post)
    if request.method == "POST":
        
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")
            
        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
            
        # ensure passwords match
        elif request.form.get("password") != request.form.get("passwordCheck"):
            return apology("passwords must match")
            
        else:
            
            # hash password
            hashword = pwd_context.hash(request.form.get("password"))
                
            # insert username and hashword into db
            result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username = request.form.get("username"), hash = hashword)
            if not result:
                return apology("Name already exists")
            
            else:
                # remember which user has registered/logged in
                session["user_id"] = result

                # redirect user to home page
                return redirect(url_for("index"))
   
   # else if user reached route via GET (as by clicking a link or via redirect)             
    else:    
        return render_template("register.html")
    
    
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # render apology if number to sell is not a positive int
        try:
            if int(request.form.get("shares")) < 1:
                return apology("number less than 1")
                
        except ValueError:
            return apology("not an integer")
            
        # get stock info
        result = lookup(request.form.get("symbol"))        
        
        # handle invalid inputs
        if result == None:
            return apology("invalid symbol")        

        
        # query current number of shares owned
        rows = db.execute("SELECT stock, SUM(amount) as amount FROM history WHERE userid = :userid and stock = :stock GROUP BY stock", userid = session["user_id"], stock = request.form.get("symbol"))
        
        # apologize if no shares owned
        if not rows:
            return apology("no shares owned")
        
        # if current shares owned is less than submitted quantity
        if int(request.form.get("shares")) > rows[0]["amount"]:
            
            # error
            return apology("don't own enough shares")
        
        # otherwise modify db and redirect
        else:
            
            # add transaction to history
            db.execute("INSERT INTO 'history' (userid, stock, amount, price) VALUES (:userid, :stock, :amount, :price)", userid = session["user_id"], stock = result["symbol"], amount = -int(request.form.get("shares")), price = result["price"])
            
            # select current amt of user money money
            money = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])            
            
            # update cash
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = money[0]["cash"] + (result["price"] * int(request.form.get("shares"))), id = session["user_id"])            
            
            # redirect to index
            flash("Sold!")
            return redirect(url_for("index"))

   # else if user reached route via GET (as by clicking a link or via redirect)             
    else:
        
        return render_template("sell.html")
        
        

@app.route("/cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add cash to account."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # try converting to float
        try:
            
            # don't let people remove money
            if float(request.form.get("money")) < 0:
                return apology("can't subtract money", "bad choice to invest with us")
        
        # error if not a float
        except ValueError:
            return apology("not a float")

        # select current amt of user money money
        money = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])

        # update cash
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = money[0]["cash"] + float(request.form.get("money")), id = session["user_id"])
        
        # redirect to index
        flash("Added!")
        return redirect(url_for("index"))        
        
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("cash.html")