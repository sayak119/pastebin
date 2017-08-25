from flask import Blueprint, request, session, jsonify, render_template, redirect
from sqlalchemy.exc import IntegrityError
from app import db
from .models import User
from app.paste.models import Paste
from functools import wraps


def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify(message="Unauthorized", success=False), 401
        user_id = session['user_id']
        user = User.query.filter(User.id == user_id).first()
        if(user.user_type != 2):
            return jsonify(message="Unauthorized", success=False), 401
        return f(*args, **kwargs)
    return decorated

mod_user = Blueprint('user', __name__)


@mod_user.route('/', methods=['GET'])
def main_form():
    return render_template('pastebin.html')


@mod_user.route('/', methods=['POST'])
def check_type():
    if 'user_id' not in session:
        return jsonify(type=0)
    user = User.query.filter(User.id == session['user_id']).first()
    # top_5 = Paste.query.all()
    # if(top_)
    return jsonify(type=user.user_type)


@mod_user.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')


@mod_user.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # except KeyError as e:
    # return render_template('register.html',error = "%s not sent in the
    # request" % e.args)

    if '@' not in email:
        return jsonify({'error': '@ not added in email'}), 400

    u = User(username, email, password, 0, 1)
    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify({'error': 'Invalid Credentials'}), 400

    return jsonify({'success': 'User Registeration successful'}), 200


@mod_user.route('/login', methods=['POST'])
def login_user():
    try:
        username = request.form['username']
        password = request.form['password']
    except KeyError as e:
        return jsonify({'error': 'All Credentials not filled'}), 400

    user = User.query.filter(User.username == username).first()
    if(user is None or not user.check_password(password)):
        return jsonify({'error': 'Invalid Username or Password is Incorrect'}), 400

    session['user_id'] = user.id

    return jsonify(success='Login successful', type=user.user_type), 200


@mod_user.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')


@mod_user.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id')
    return redirect('/')


@mod_user.route('/admin/register', methods=['GET'])
@requires_admin
def admin_form():
    return render_template('admin_reg.html')


# @mod_user.route('/admin/register', methods=['POST'])
# @requires_admin
# def register_admin():
#     username = request.form['username']
#     email = request.form['email']
#     password = request.form['password']

#     # except KeyError as e:
#     # return render_template('register.html',error = "%s not sent in the
#     # request" % e.args)

#     if '@' not in email:
#         return jsonify({'error': '@ not added in email'}), 400

#     u = User(username, email, password, 0, 2)
#     db.session.add(u)
#     try:
#         db.session.commit()
#     except IntegrityError as e:
#         return jsonify({'error': 'Invalid Credentials'}), 400

#     return redirect('/admin/all_paste')

@mod_user.route('/admin', methods=['GET'])
@requires_admin
def admin_home():
    return render_template('admin.html')


@mod_user.route('/admin/register_deregister', methods=['POST'])
@requires_admin
def reg_dereg_admin():
    user_name = request.form['username']
    user = User.query.filter(User.username == user_name).first()
    if user.user_type == 2:
        user.user_type = 1
        db.session.commit()
        return jsonify(success=True, reply="Admin Deregistered", type=1)
    else:
        user.user_type = 2
        db.session.commit()
        return jsonify(success=True, reply="Registered as Admin", type=2)


@mod_user.route('/api/allusers', methods=['POST'])
@requires_admin
def get_all_users():
    user_id = session['user_id']
    user = User.query.filter(user_id == User.id).first()
    all_users = User.query.all()
    users = []
    for curr_user in all_users:
        users.append(curr_user.to_dict())
    return jsonify({'users': users, 'username': user.username}), 200


@mod_user.route('/allusers', methods=['GET'])
@requires_admin
def all_users():
    return render_template('allusers.html')

# @mod_user.route('/create_paste', methods=['POST'])
# def increase_paste_count():
#     user_id = session['user_id']
#     user = User.query.filter_by(user_id=user_id).first()
#     user.paste_count = user.paste_count + 1
#     db.session.commit()
#     return jsonify({'url': url}), 200
