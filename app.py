from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///courses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    telegram_link = db.Column(db.String(200), default="https://t.me/V_Y_I_2")

@app.route('/')
def home():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@app.route('/register/<int:course_id>')
def register_course(course_id):
    course = Course.query.get_or_404(course_id)
    return redirect(course.telegram_link)

@app.route('/telegram')
def telegram_redirect():
    return redirect("https://t.me/V_Y_I_2")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Add initial courses if database is empty
        if not Course.query.first():
            initial_courses = [
                Course(name="🐍 تعلم بايثون من الصفر", description="دورة شاملة في لغة البايثون"),
                Course(name="☕ تعلم جافا خطوة بخطوة", description="دورة تعليمية في لغة جافا"),
                Course(name="💻 تعلم ++C وأساسيات البرمجة", description="دورة في لغة سي بلس بلس"),
                Course(name="🎨 تعلم CSS لتصميم المواقع", description="دورة في تصميم المواقع")
            ]
            for course in initial_courses:
                db.session.add(course)
            db.session.commit()

    app.run(host='0.0.0.0', port=5000, debug=True)