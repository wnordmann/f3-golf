from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://f3_golf_user:E7IVG1eQgUgMMl0RgzGkWVFuhePDuNum@dpg-cp3annnsc6pc73fls8u0-a/f3_golf'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    team_name = db.Column(db.String(100), nullable=True)


def init_db():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        team_name = request.form['team_name']

        new_participant = Participant(
            name=name, email=email, phone=phone, team_name=team_name)
        db.session.add(new_participant)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('signup.html')


@app.route('/admin')
def admin():
    participants = Participant.query.all()
    return render_template('admin.html', participants=participants)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
