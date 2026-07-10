from flask import Flask ,render_template , request , redirect ,url_for,flash
from dotenv import load_dotenv
import os
from smtplib import SMTP


from pyexpat.errors import messages

load_dotenv()

password = os.environ.get("PASSWORD")
my_email = os.environ.get("MY_EMAIL")
sender_email = os.environ.get("SENDING_EMAIL")

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

@app.route("/")
def home():

    return render_template("index.html")


@app.route("/submit",methods=["GET","POST"])
def submit():

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        try:
            with SMTP("smtp.gmail.com", 587, timeout=10) as connection:
                connection.ehlo()
                connection.starttls()
                connection.ehlo()
                connection.login(sender_email, password)
                connection.sendmail(
                    sender_email,
                    my_email,
                    f"Subject:From portfolio contacts\n\n"
                    f"Name: {name}\n"
                    f"Email: {email}\n"
                    f"Message: {message}"
                )

                flash("Mail sent Successfully")

                return redirect(url_for("home"))

        except Exception as e:
            return str(e)

    return render_template("index.html")


if __name__ == "__main__":

    app.run(debug=True)