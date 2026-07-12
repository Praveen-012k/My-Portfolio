from flask import Flask ,render_template , request , redirect ,url_for,flash
from dotenv import load_dotenv
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

load_dotenv()

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.environ.get("API_KEY")

password = os.environ.get("PASSWORD")
my_email = os.environ.get("MY_EMAIL")
sender_email = os.environ.get("SENDING_EMAIL")

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

@app.route("/")
def home():

    return render_template("index.html")



@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            sender={"name": "Portfolio Contact Form", "email": my_email},
            to=[{"email": sender_email}],
            subject="New message from portfolio contact form",
            html_content=f"<p><strong>Name:</strong> {name}</p>"
                         f"<p><strong>Email:</strong> {email}</p>"
                         f"<p><strong>Message:</strong> {message}</p>"
        )

        try:
            api_instance.send_transac_email(send_smtp_email)
            flash("Message sent successfully!")
        except ApiException as e:
            print(e)
            flash("Something went wrong. Please email me directly instead.")

        return redirect(url_for("home"))

    return render_template("index.html")
if __name__ == "__main__":

    app.run(debug=True)