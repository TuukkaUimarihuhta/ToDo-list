from flask import Flask, request, render_template
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
    name = db.StringField(required=True)  # Name of the housework
    added = db.StringField(required=True)  # The date housework was added
    final = db.StringField(required=True)  # Last date to do the housework
    tehty = db.BooleanField(required=True)  # Mark the housework as done
    deldate = db.DateTimeField()  # The date on which the housework is automatically removed
    date = db.DateField()  # Date that decides the order housework are listed


@app.route("/")
# Unfinished housework
def unfinished():
    job = Todo.objects
    for t in job:
        # Housework is removed from list automatically after 14 days pass
        if (datetime.utcnow() - t['deldate']) >= timedelta(days=0):
            job.delete()
        else:
            pass
    # Housework are listed based on dates
    jobs = Todo.objects(tehty=False).order_by('date')
    return render_template("unfinished.html", jobs=jobs)


@app.route("/finished")
# Finished housework
def done():
    jobs = Todo.objects(tehty=True).order_by('date')
    return render_template("finished.html", jobs=jobs)


@app.route("/housework/<name>")
# Choose housework from list
def hae_kotityo(name):
    for s in Todo.objects:
        if s['name'] == name:
            return render_template("work.html", job=s)


@app.route("/update", methods=["POST"])
# Form that you can use to update the information of a housework
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
    return render_template("unfinished.html", jobs=jobs)

@app.route("/add/")
# Opens a form that can be used to add a housework
def add():
    jobs = Todo.objects(tehty=False).order_by('date')
    return render_template("add.html", jobs=jobs)

@app.route("/add/", methods=["POST"])
# Form that is used to add a housework
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

    return render_template("unfinished.html", jobs=jobs)


@app.route("/finished/<name>")
# Updates a housework as finished
def doing(name):
    job = Todo.objects(name=name)
    job.update(tehty=True, added=today.strftime('%A %d.%m'))
    jobs = Todo.objects(tehty=False).order_by('date')
    return render_template("unfinished.html", jobs=jobs)


@app.route("/unfinished/<name>")
# Deletes a housework from the list of unfinished housework
def delete(name):
    job = Todo.objects(name=name, tehty=False)
    job.delete()
    jobs = Todo.objects(tehty=False).order_by('date')
    return render_template("unfinished.html", jobs=jobs)


@app.route("/finish/<name>")
# Deletes housework from the finished housework list
def deldone(name):
    job = Todo.objects(name=name, tehty=True)
    job.delete()
    jobs = Todo.objects(tehty=True).order_by('date')
    return render_template("finished.html", jobs=jobs)


if __name__ == '__main__':
    app.run(debug=True)
