from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:53578696Rr$@localhost/agenda'
app.config['SECRET_KEY'] = '555'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Ruta de inicio
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        if 'login' in request.form:
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))
            else:
                flash('Credenciales incorrectas.')
        elif 'register' in request.form:
            email = request.form['email']
            password = request.form['password']
            hashed_password = generate_password_hash(password)
            new_user = User(email=email, password=hashed_password)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Registro exitoso.')
            except Exception as e:
                db.session.rollback()
                flash(f'Error al registrar: {str(e)}')
            return redirect(url_for('index'))

    return render_template('index.html')

# dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user_id = session['user_id']
    contacts = Contact.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', contacts=contacts)

# agregar contacto
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    name = request.form['name']
    phone = request.form['phone']
    user_id = session['user_id']
    new_contact = Contact(name=name, phone=phone, user_id=user_id)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'Error al agregar contacto: {str(e)}')
    return redirect(url_for('dashboard'))

# eliminar contacto
@app.route('/delete_contact/<int:contact_id>')
def delete_contact(contact_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    contact = Contact.query.get(contact_id)
    if contact and contact.user_id == session['user_id']:
        try:
            db.session.delete(contact)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f'Error al eliminar contacto: {str(e)}')
    return redirect(url_for('dashboard'))

# cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)


