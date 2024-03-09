from flask import Flask, session, render_template, request
import swimclub,  os

app = Flask(__name__)
app.secret_key = "this_is_a_very_secret_key"

@app.get("/")
def index():
    return render_template("index.html",
                           title = "Welcome to the Swimclub",)

def populate_data():
    if "swimmers" not in session:
        path = os.getcwd()+"\\ch5\\swimdata"
        filenames = sorted(os.listdir(path))
        filenames.remove(".DS_Store")
        session["swimmers"] = {}
        for file in filenames:
            name , *_ = swimclub.get_swim_data(file)
            if name not in session["swimmers"]:
                session["swimmers"][name] = []
            session["swimmers"][name].append(file)

@app.get("/swimmers")
def display_swimmers():
    populate_data()
    return render_template("select.html",
                           title="Select a swimer",
                           url="/showfiles",
                           data=sorted(session["swimmers"]),
                           select_id="swimmer")


@app.post("/showfiles")
def display_swimers_files():
    populate_data()
    name = request.form["swimmer"]
    return render_template("select.html",
                           title="Select an event",
                           url="/showbarchart",
                           select_id="file",
                           data=session["swimmers"][name],
                           )

@app.post("/showbarchart")
def show_bar_chart():
    file_name = request.form["file"]
    path = swimclub.produce_bar_chart(file_name,location="ch5/templates/")
    return render_template(path.split("\\")[-1])

if __name__ == "__main__":
    app.run(debug=True)