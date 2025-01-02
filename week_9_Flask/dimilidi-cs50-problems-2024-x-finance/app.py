import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Get users stocks and shares
    stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
                        user_id=session["user_id"])

    # Get users cash balance
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
                      user_id=session["user_id"])[0]["cash"]

    # Variables for total values
    total_value = cash
    grand_total = cash

    # Iterate over stocks and add price and total value
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["value"] = stock["price"] * stock["total_shares"]
        total_value += stock["value"]
        grand_total += stock["value"]

    return render_template("index.html", stocks=stocks, cash=cash, total_value=total_value, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        if not symbol:
            return apology("please provide symbol")
        elif not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("please provide positive number for shares")

        quote = lookup(symbol)
        if quote is None:
            return ("symbol not found", 400)

        price = quote["price"]
        total_cost = int(shares) * price
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=session["user_id"])[0]["cash"]

        if cash < total_cost:
            return ("not enough cash", 400)

        # Update users table
        db.execute("UPDATE users SET cash = cash - :total_cost WHERE id = :user_id",
                   total_cost=total_cost, user_id=session["user_id"])

        # Add purchase to history table
        db.execute("INSERT INTO transactions(user_id, symbol, shares, price) VALUES(:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"], symbol=symbol, shares=shares, price=price)

        flash(f"Bought {shares} shares of {symbol} for {usd(total_cost)}!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Find users transactions order starting from most recent
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id= :user_id ORDER BY timestamp DESC", user_id=session["user_id"])

    # Parse the timestamp into a datetime object
    for transaction in transactions:
        transaction["timestamp"] = datetime.strptime(transaction["timestamp"], "%Y-%m-%d %H:%M:%S")

    # Render history page with transactions
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("please provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("please provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if not quote:
            return apology("Invalid symbol", 400)
        return render_template("quote.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget user id
    session.clear()

    # If register via POST method (form)
    if request.method == "POST":
        # Validate user input
        if not request.form.get("username"):
            return apology("please provide username", 400)
        elif not request.form.get("password"):
            return apology("please provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("please confirm password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Find username in db
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Check if user already exists
        if len(rows) != 0:
            return apology("user already exists", 400)
        # Insert user into db
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                   request.form.get("username"), generate_password_hash(request.form.get("password")))
        # Find the new user in db
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Store user id in the session
        session["user_id"] = rows[0]["id"]

        # Redirect to homepage
        return redirect("/")

    # If register via GET (via redirect, link)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Get users stocks and shares
    stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
                        user_id=session["user_id"])

    # If the user submits the form
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        if not symbol:
            return apology("please provide symbol")
        elif not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("please provide positive number for shares")
        else:
            shares = int(shares)

        for stock in stocks:
            if stock["symbol"] == symbol:
                if stock["total_shares"] < shares:
                    return apology("not enough shares")
                else:
                    # Get quote
                    quote = lookup(symbol)
                    if quote is None:
                        return apology("symbol not found")
                    price = quote["price"]
                    total_sale = shares * price

                    # Update users table
                    db.execute("UPDATE users SET cash = cash + :total_sale WHERE id = :user_id",
                               total_sale=total_sale, user_id=session["user_id"])

                    # Add sale to history table
                    db.execute("INSERT INTO transactions(user_id, symbol, shares, price) VALUES(:user_id, :symbol, :shares, :price)",
                               user_id=session["user_id"], symbol=symbol, shares=-shares, price=price)

                    flash(f"Sold {shares} shares of {symbol} for {usd(total_sale)}!")
                    return redirect("/")

        return apology("symbol not found")

    # If the user visits the page
    else:
        return render_template("sell.html", stocks=stocks)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow users to change their password"""
    if request.method == "POST":
        # Get form inputs
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Validate inputs
        if not old_password or not new_password or not confirmation:
            return apology("all fields are required", 400)
        if new_password != confirmation:
            return apology("passwords do not match", 400)

        # Get the user's current password hash from the database
        user = db.execute("SELECT hash FROM users WHERE id = :user_id",
                          user_id=session["user_id"])[0]

        # Verify the old password
        if not check_password_hash(user["hash"], old_password):
            return apology("incorrect old password", 400)

        # Update the password with a new hash
        new_password_hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = :new_hash WHERE id = :user_id",
                   new_hash=new_password_hash, user_id=session["user_id"])

        # Flash a success message and redirect to the home page
        flash("Password changed successfully!")
        return redirect("/")

    # Render the change password form
    else:
        return render_template("change_password.html")
