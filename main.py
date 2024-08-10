from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash  # type: ignore
from flask_bootstrap import Bootstrap5  # type: ignore
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)  # type: ignore
import os

# import smtplib
from forms import CreatePostForm, AuthForm, ContactForm
from models import Project, db
from scraper_md import scrapy

app = Flask(__name__)

ADMIN_KEY = "619UmOvjSOE1io{k/M$G"
# SECRET_KEY = os.environ.get("SECRET_KEY")
app.config["SECRET_KEY"] = "Y-9D6Bq;QF>?Y0Z4<7Zg"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///C:/Users/Neriukas/Desktop/Code/Portfolio/instance/database.db"
)
# ADMIN_KEY = os.environ.get("ADMIN_KEY")
# # SECRET_KEY = os.environ.get("SECRET_KEY")
# app.config["SECRET_KEY"] = os.environ.get("FLASK_KEY")
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
#     "DB_URI", "sqlite:///database.db"
# )
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(key):
    if key == ADMIN_KEY:
        return User(key)
    return None


db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    result = db.session.execute(db.select(Project))
    projects = result.scalars().all()
    return render_template("index.html", projects=projects)


@app.route("/collaborate")
def collab():
    return render_template("collab.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/project/<int:project_id>", methods=["GET", "POST"])
def show_project(project_id):
    requested_project = db.get_or_404(Project, project_id)
    return render_template("project.html", project=requested_project)


@app.route("/login", methods=["GET", "POST"])
def login():
    auth_form = AuthForm()
    if request.method == "POST" and auth_form.validate_on_submit():
        key = auth_form.key.data
        print(key)
        if key == ADMIN_KEY:
            user = User(key)
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials. Please try again.")
    return render_template("login.html", form=auth_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/upload", methods=["GET", "POST"])
@login_required
def add_new_project():
    form = CreatePostForm()
    if request.method == "POST" and form.validate_on_submit():
        new_project = Project(
            title=form.title.data,
            subtitle=form.subtitle.data,
            img_url=form.img_url.data,
            date=datetime.today().strftime("%B %d, %Y"),
            github_url=form.github_url.data,
            readme=scrapy(form.github_url.data),
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("upload.html", form=form)


@app.route("/edit-project/<int:project_id>", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    project = db.get_or_404(Project, project_id)
    edit_form = CreatePostForm(
        title=project.title,
        subtitle=project.subtitle,
        img_url=project.img_url,
        github_url=project.github_url,
    )
    if edit_form.validate_on_submit():
        project.title = edit_form.title.data
        project.subtitle = edit_form.subtitle.data
        project.img_url = edit_form.img_url.data
        project.github_url = edit_form.github_url.data
        project.readme = scrapy(edit_form.github_url.data)
        db.session.commit()
        return redirect(url_for("show_project", project_id=project.id))
    return render_template("upload.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:project_id>")
@login_required
def delete_project(project_id):
    project_to_delete = db.get_or_404(Project, project_id)
    db.session.delete(project_to_delete)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == "POST" and form.validate_on_submit():
        data = request.form
        send_email(data["name"], data["email"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", form=form, msg_sent=False)


# TODO: Implement email sending feature
def send_email(name, email, message):
    email_message = f"Subject:New Message from Portfolio Website\n\nName: {name}\nEmail: {email}\nMessage:{message}"
    print(email_message)
    # with smtplib.SMTP("smtp.gmail.com") as connection:
    #     connection.starttls()
    #     connection.login(SMTP_EMAIL, APP_PASSWORD)
    #     connection.sendmail(SMTP_EMAIL, SMTP_EMAIL, email_message)


if __name__ == "__main__":
    app.run(debug=True)
