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
    name = db.StringField(required=True)  # Kotityön nimi
    added = db.StringField(required=True)  # Lisäyspäivä, joka näkyy HTML:ssä
    final = db.StringField(required=True)  # Viimeinen tekopäivä, näkyy HTML:ssä
    tehty = db.BooleanField(required=True)  # Merkkaa kotityön tehdyksi
    deldate = db.DateTimeField()  # Päivämäärä, jonka mukaan työ poistuu automaattisesti
    date = db.DateField()  # Päiväämäärä, mikä päättää kotitöiden järjestyksen HTML:ssä


@app.route("/")
#Etusivu
def home():
    job = Todo.objects
    for t in job:
        #Kotityöt poistuvat listalta automaattisesti 14 päivän päästä
        if (datetime.utcnow() - t['deldate']) >= timedelta(days=0):
            job.delete()
        else:
            pass
    #Kotityöt näkyvät listassa Päivämäärän mukaan
    jobs = Todo.objects(tehty=False).order_by('date')
    return render_template("tekemattomat.html", jobs=jobs)


@app.route("/tehdyt/")
#Tehtyjen kotitöiden sivu
def done():
    jobs = Todo.objects(tehty=True).order_by('date')
    return render_template("done.html", jobs=jobs)


@app.route("/kotityö/<name>")
#Valitsee kotityön, listalta
def hae_kotityo(name):
    for s in Todo.objects:
        if s['name'] == name:
            return render_template("work.html", job=s)


@app.route("/update", methods=["POST"])
#Lomake, jolla voi päivittää tekemättömän kotityön tietoja
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
#Avaa lomakkeen, jolla voidaan lisätä kotityö
def add():
    jobs = Todo.objects(tehty=False).order_by('date')
    return render_template("add.html", jobs=jobs)

@app.route("/add/", methods=["POST"])
#Lomake jolla lisätään kotityö tekemättömien listaan
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
#Päivittää kotityön tehdyksi, lisää sen tehtyjen listaan
def doing(name):
    job = Todo.objects(name=name)
    job.update(tehty=True, added=today.strftime('%A %d.%m'))
    jobs = Todo.objects(tehty=False).order_by('date')
    return render_template("tekemattomat.html", jobs=jobs)


@app.route("/Kotityöt/<name>")
#Poistaa kotityön tekemättömien kotitöiden listasta, päivittää listan
def delete(name):
    job = Todo.objects(name=name, tehty=False)
    job.delete()
    jobs = Todo.objects(tehty=False).order_by('date')
    return render_template("tekemattomat.html", jobs=jobs)


@app.route("/tehdyt/<name>")
#poistaa kotityön tehtyjen listasta, sekä päivittää listan
def deldone(name):
    job = Todo.objects(name=name, tehty=True)
    job.delete()
    jobs = Todo.objects(tehty=True).order_by('date')
    return render_template("done.html", jobs=jobs)


if __name__ == '__main__':
    app.run(debug=True)
