from flask import Flask, request, jsonify, make_response, render_template, abort
from flask_mongoengine import MongoEngine
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['MONGODB_SETTING'] = {
    'db': 'Todolist',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

today = datetime.utcnow()

class Todo(db.Document):
    name = db.StringField(required=True) #Kotityön nimi
    added = db.StringField(required=True) #Lisäyspäivä, joka näkyy HTML:ssä
    final = db.StringField(required=True) #Viimeinen tekopäivä, näkyy HTML:ssä
    tehty = db.BooleanField(required=True) #Merkkaa kotityön tehdyksi
    deldate = db.DateTimeField() #Päivämäärä, jonka mukaan työ poistuu automaattisesti
    date = db.DateField() #Päiväämäärä, mikä päättää kotitöiden järjestyksen HTML:ssä

@app.route("/")
def home():
    job = Todo.objects
    for t in job:
        if (datetime.utcnow() - t['deldate']) >= timedelta(days=0): #Kotityöt poistuvat listalta automaattisesti
            job.delete()                                            #14 päivän päästä
        else:
            pass
    jobs = Todo.objects(tehty=False).order_by('date')
    return render_template("tekemattomat.html", jobs=jobs)

@app.route("/tehdyt/")
def done():
        jobs = Todo.objects(tehty=True).order_by('date')
        return render_template("done.html", jobs=jobs)

@app.route("/kotityö/<name>")
def hae_kotityo(name):
    for s in Todo.objects:
        if s['name'] == name:
            return render_template("work.html", job=s)

@app.route("/update", methods=["POST"])
def update():
    name = request.form["name"]
    deldate = today + timedelta(days=14)
    added = request.form["added"]
    get_date = request.form["final"]
    date = datetime.strptime(get_date, '%Y-%m-%d')
    final = date.strftime('%A %d.%m')

    jobs = Todo.objects(name=name, added=added, tehty=False)
    jobs.update(date=date, final=final, deldate=deldate)
    jobs = Todo.objects(tehty=False).order_by('date')
    return render_template("tekemattomat.html", jobs=jobs)

@app.route("/add/")
def add():
    jobs = Todo.objects(tehty=False).order_by('date')
    return render_template("add.html", jobs=jobs)

@app.route("/add/", methods=["POST"])
def added():
    name = request.form['name']
    deldate = today + timedelta(days=14)
    added = today.strftime('%A %d.%m')
    get_date = request.form["final"]
    date = datetime.strptime(get_date, '%Y-%m-%d')
    final = date.strftime('%A %d.%m')

    job = Todo(
                name=name,
                added=added,
                final=final,
                tehty=False,
                deldate=deldate,
                date=date
                )

    job.save()
    jobs = Todo.objects(tehty=False).order_by('date')

    return render_template("tekemattomat.html", jobs=jobs)

@app.route("/tehty/<name>")
def doing(name):
    job = Todo.objects(name=name)
    job.update(tehty=True, added=today.strftime('%A %d.%m'))
    jobs = Todo.objects(tehty=False).order_by('date')
    return render_template("tekemattomat.html", jobs=jobs)

@app.route("/Kotityöt/<name>")
def delete(name):
    job = Todo.objects(name=name, tehty=False)
    job.delete()
    jobs = Todo.objects(tehty=False).order_by('date')
    return render_template("tekemattomat.html", jobs=jobs)

@app.route("/tehdyt/<name>")
def deldone(name):
    job = Todo.objects(name=name, tehty=True)
    job.delete()
    jobs = Todo.objects(tehty=True).order_by('date')
    return render_template("done.html", jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)


