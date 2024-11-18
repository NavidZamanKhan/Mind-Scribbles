from flask import Flask, render_template, request
import requests, datetime
from dotenv import load_dotenv
import os, smtplib

load_dotenv("email.env")

OWN_EMAIL = os.getenv("gmail")
OWN_PASSWORD = os.getenv("password")


app = Flask(__name__)

response = requests.get("https://api.npoint.io/623d7162a61d571db725")
posts = response.json()


@app.route("/")
def index():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/form-entry", methods=["GET", "POST"])
def receive_data():
    if request.method == "POST":
        data = request.form
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New message\n\nName: {name}\nEmail: {email}\nPhone{phone}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
