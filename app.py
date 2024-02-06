from flask import (
    Flask,
    url_for,
    send_from_directory,
    render_template,
    redirect,
    request,
)

from adult_census.pipeline.stage_05_prediction import PredictionPipeline

app = Flask(__name__)


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)


@app.route("/")
def index():
    return redirect("/home")


@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    elif request.method == "POST":
        user_input = request.form.to_dict()
        user_input = {col: [user_input[col]] for col in user_input.keys()}
        # print(user_input) # for testing and output purpose
        user_prediction = PredictionPipeline().main(user_input=user_input)
        if user_prediction[0] == 0:
            user_prediction = "User's Income less than 50K"
            return render_template(
                "home.html", user_prediction=user_prediction
            )  # user_prediction=user_prediction
        else:
            user_prediction = "User's Income more than 50K"
            return render_template(
                "home.html", user_prediction=user_prediction
            )  # user_prediction=user_prediction


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
