from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, jsonify
from app import db, requires_auth
from flask_cors import CORS
from .models import Paste
import uuid
from datetime import datetime
from app.user.models import User
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from functools import wraps
from datetime import datetime
from dateutil import parser


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

mod_paste = Blueprint('paste', __name__)
CORS(mod_paste)


def is_active(paste):
    return parser.parse(paste.expire_time) > datetime.now()


@mod_paste.route('/create_paste', methods=['GET'])
@requires_auth
def create_form():
    curr_id = session['user_id']
    user = User.query.filter(User.id == curr_id).first()
    return render_template('user.html', username=user.username)


@mod_paste.route('/create_paste', methods=['POST'])
def create_paste():
    title = request.form['title']
    text = request.form['text']
    paste_type = request.form['type']
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        user = User.query.filter(User.username == 'Guest').first()
        user_id = user.id
    lang = request.form['lang']
    time_form = request.form['time']
    expire_time = str(time_form)
    add_time = str(datetime.now())
    url = str(uuid.uuid4())
    report_count = 0
    try:
        paste = Paste(title, text, lang, add_time,
                      expire_time, user_id, url, report_count, paste_type)
        user = User.query.filter(User.id == user_id).first()
        x = user.paste_count
        user.paste_count = x + 1
        db.session.add(paste)
        db.session.commit()
        # jsonify(success=True, paste=paste.to_dict())
        return jsonify({'url': url}), 200
    except:
        return jsonify({'error': 'Error while creating Paste, Please check if all fields are filled'}), 400


@mod_paste.route('/paste', methods=['GET'])
@requires_auth
def get_all_pastes():
    # user_id = session['user_id']
    # pastes = paste.query.filter(paste.user_id == user_id).all()
    if 'user_id' in session:
        curr_id = session['user_id']
        user = User.query.filter(curr_id == User.id).first()
        if user.user_type == 2:
            return render_template('admin_mypaste.html')
        return render_template("mypaste.html")
    else:
        return jsonify({'error': 'Please Login to Continue'}), 400
    # return jsonify(success=True, pastes=[paste.to_dict() for paste in
    # pastes])


@mod_paste.route('/api/paste', methods=['POST'])
@requires_auth
def get_all_pastes_object():
    user_id = session['user_id']
    user = User.query.filter(user_id == User.id).first()
    pastes = Paste.query.filter(Paste.user_id == user_id).all()

    active = []
    for paste in pastes:
        if is_active(paste):
            active.append(paste.to_dict())
        else:
            userid_to_red = paste.user_id
            user_to_red = User.query.filter(userid_to_red == User.id)
            user_to_red.paste_count = user_to_red.paste_count - 1
            db.session.delete(paste)
            db.session.commit()

    return jsonify({'paste_list': active, 'username': user.username}), 200


@mod_paste.route('/<url>/embed', methods=['GET'])
def embed_code_form(url):
    paste = Paste.query.filter(Paste.url == url).first()
    if is_active(paste):
        return render_template('embed.html', paste_text=paste.text, paste_link="http://127.0.0.1:8080/" + url)
    else:
        userid_to_red = paste.user_id
        user_to_red = User.query.filter(User.id == userid_to_red).first()
        user_to_red.paste_count = user_to_red.paste_count - 1
        db.session.delete(paste)
        db.session.commit()
        return render_template("index.html"), 404


# @mod_paste.route('/<url>/embed', methods=['POST'])
# def embed_code(url):
# 	paste = Paste.query.filter(Paste.url == url).first()
# 	return jsonify(paste_text = paste.text,paste_link = url)

@mod_paste.route('/<url>/embed/output', methods=['GET'])
def embed_code_disp(url):
    paste = Paste.query.filter(Paste.url == url).first()
    if is_active(paste):
        return render_template('embed_output.html')
    else:
        userid_to_red = paste.user_id
        user_to_red = User.query.filter(User.id == userid_to_red).first()
        user_to_red.paste_count = user_to_red.paste_count - 1
        db.session.delete(paste)
        db.session.commit()
        return render_template("index.html"), 404

# @mod_paste.route('/paste', methods=['GET'])
# @requires_auth
# def get_all_pastes():
#     # user_id = session['user_id']
#     # pastes = paste.query.filter(paste.user_id == user_id).all()
#     curr_id = session['user_id']
#     user = User.query.filter(User.id == curr_id).first()
#     paste_list = Paste.query.filter(curr_id == Paste.user_id).all()
#     url_pre = "/"
#     for paste in paste_list:
#         paste.url = url_pre + paste.url
#     if user.user_type == 1:
#         return render_template('mypaste.html', paste_list=paste_list)
#     return render_template('admin_mypaste.html',paste_list = paste_list)
#     # return jsonify(success=True, pastes=[paste.to_dict() for paste in
#     # pastes])
#
#
# @mod_paste.route('/api/paste', methods=['POST'])
# @requires_auth
# def get_all_pastes_object():
#     user_id = session['user_id']
#     user = User.query.filter(user_id == User.id).first()
#     pastes = Paste.query.filter(Paste.user_id == user_id).all()
#     active = []
#     for paste in pastes:
#         temp_paste = {}
#         if paste.is_active():
#             temp_paste['title'] = paste.title
#             temp_paste['add_time']=paste.add_time
#             temp_paste['expire_time']=paste.expire_time
#             temp_paste['lang']=paste.lang
#             temp_paste['url']=paste.url
#             active.append(temp_paste)
#
#     return jsonify({'paste_list':active,'username':user.username}),200


# @mod_paste.route('/paste/<id>', methods=['GET'])
# @requires_auth
# def get_paste(id):
#     user_id = session['user_id']
#     paste = paste.query.filter(
#         Paste.id == id, Paste.user_id == user_id).first()
#     if paste is None:
#         return render_template("index.html"),4044
#     else:
#         return jsonify(success=True, paste=paste.to_dict())


# @mod_paste.route('/paste/<id>', methods=['POST'])
# @requires_auth
# def edit_paste(id):
#     user_id = session['user_id']
#     paste = Paste.query.filter(
#         Paste.id == id, Paste.user_id == user_id).first()
#     if paste is None:
#         return render_template("index.html"),4044
#     else:
#         paste.title = request.form['title']
#         paste.text = request.form['text']
#         paste.color = request.form['color']
#         paste.lang = request.form['lang']
#         db.session.commit()
#         return jsonify(success=True)


@mod_paste.route('/<url>/delete', methods=['POST'])
@requires_auth
def delete_paste(url):
    user_id = session['user_id']
    # print(user_id)
    paste = Paste.query.filter(Paste.url == url).first()
    user = User.query.filter(User.id == user_id).first()
    if paste is None:
        return render_template("index.html"), 404
    if is_active(paste):
        if paste.user_id == user_id or user.user_type == 2:
            userid_to_red = paste.user_id
            user_to_red = User.query.filter(User.id == userid_to_red).first()
            user_to_red.paste_count = user_to_red.paste_count - 1
            db.session.delete(paste)
            db.session.commit()
            return jsonify(success=True, user_type=user.user_type), 200
        else:
            return jsonify(success=False), 400
    else:
        userid_to_red = paste.user_id
        user_to_red = User.query.filter(User.id == userid_to_red).first()
        user_to_red.paste_count = user_to_red.paste_count - 1
        db.session.delete(paste)
        db.session.commit()
        return render_template("index.html"), 404


# @mod_paste.route('/<url>', methods=['GET'])
# def display_paste(url):
#     paste = Paste.query.filter(Paste.url == url).first()
#     style = HtmlFormatter().get_style_defs('.highlight')
#     lexer = get_lexer_by_name(paste.lang)
#     formatter = HtmlFormatter(linenos=True, cssclass="highlight")
#     result = highlight(paste.text, lexer, formatter)
# return render_template("view_paste.html", paste_title=paste.title,
# paste_lang=paste.lang, highlight_style=style,
@mod_paste.route('/<url>', methods=['GET'])
# paste_text=result,paste_rawdata = paste.text)
def display_paste(url):
    paste = Paste.query.filter(Paste.url == url).first()
    if Paste.query.filter(Paste.url == url).first() != None:
        if is_active(paste):
            if(paste.paste_type == "1" and session['user_id'] != paste.user_id):
                return render_template("index.html"), 200
            if 'user_id' in session:
                user_id = session['user_id']
                user = User.query.filter(User.id == user_id).first()
                if user.user_type == 1:
                    return render_template('view_paste.html')
                if user.user_type == 2:
                    return render_template('view_paste_admin.html')
            return render_template("view_paste_guest.html")
        else:
            userid_to_red = paste.user_id
            user_to_red = User.query.filter(User.id == userid_to_red).first()
            user_to_red.paste_count = user_to_red.paste_count - 1
            db.session.delete(paste)
            db.session.commit()
            return render_template("index.html"), 404
    else:
        return render_template("index.html"), 404


@mod_paste.route('/api/<url>', methods=['POST'])
@requires_auth
def ret_paste(url):
    paste = Paste.query.filter(Paste.url == url).first()
    user = User.query.filter(paste.user_id == User.id).first()
    if is_active(paste):
        return jsonify({'paste_owner': user.username, 'paste_text': paste.text, 'paste_title': paste.title, 'paste_lang': paste.lang, 'paste_add': paste.add_time, 'paste_expire': paste.expire_time}), 200
    else:
        userid_to_red = paste.user_id
        user_to_red = User.query.filter(User.id == userid_to_red).first()
        user_to_red.paste_count = user_to_red.paste_count - 1
        db.session.delete(paste)
        db.session.commit()
        return render_template("index.html"), 404

# @mod_paste.route('/<url>/add_report', methods=['POST'])
# @requires_auth
# def to_delete(url):
#     paste_to_delete = Paste.query.filter(Paste.url == url).first()
#     if paste_to_delete.report_count > 5:
#         db.session.delete(paste_to_delete)
#     else:
#         paste_to_delete.report_count = paste_to_delete.report_count + 1
#     db.session.commit()
#     curr_id = session['user_id']
#     paste_list = Paste.query.filter(Paste.user_id == curr_id).all()
#     url_pre = "/"
#     for paste in paste_list:
#         paste.url = url_pre + paste.url
#     return render_template('mypaste.html', paste_list=paste_list)


@mod_paste.route('/<url>/edit', methods=['GET'])
@requires_auth
def edit_form(url):
    if 'user_id' in session:
        user_id = session['user_id']
        paste = Paste.query.filter(Paste.url == url).first()
        if is_active(paste):
            if paste.user_id == user_id:
                return render_template('editpaste.html')
            return jsonify(success=False, reply="Not Authorized"), 400
        else:
            userid_to_red = paste.user_id
            user_to_red = User.query.filter(User.id == userid_to_red).first()
            user_to_red.paste_count = user_to_red.paste_count - 1
            db.session.delete(paste)
            db.session.commit()
            return render_template("index.html"), 404
    return jsonify(success=False, reply="Please Login"), 400


@mod_paste.route('/<url>/edit', methods=['POST'])
@requires_auth
def edit_paste(url):
    if 'user_id' in session:
        user_id = session['user_id']
        paste = Paste.query.filter(Paste.url == url).first()
        if not is_active(paste):
            userid_to_red = paste.user_id
            user_to_red = User.query.filter(User.id == userid_to_red).first()
            user_to_red.paste_count = user_to_red.paste_count - 1
            db.session.delete(paste)
            db.session.commit()
            return render_template('index.html'), 404
        if paste.user_id != user_id:
            return jsonify(success=False, reply="Not Authorized"), 400
        title = request.form['title']
        text = request.form['text']
        lang = request.form['lang']
        time_form = request.form['time']
        paste_type = request.form['type']
        expire_time = str(time_form)

        paste.title = title
        paste.text = text
        paste.lang = lang
        paste.expire_time = expire_time
        paste.paste_type = paste_type
        db.session.commit()
        return jsonify(success=True, url=url)
    return jsonify(success=False, reply="Please Login")


@mod_paste.route('/admin/pastes', methods=['GET'])
@requires_admin
def all_pastes():
    paste_list = db.session.all()
    url_pre = "/"
    for paste in paste_list:
        if is_active(paste):
            paste.url = url_pre + paste.url
        else:
            userid_to_red = paste.user_id
            user_to_red = User.query.filter(User.id == userid_to_red).first()
            user_to_red.paste_count = user_to_red.paste_count - 1
            db.session.delete(paste)
            db.session.commit()
    return render_template('allpaste.html', paste_list=paste_list)


@mod_paste.route('/<username>/paste', methods=['GET'])
@requires_admin
def get_user_pastes(username):
    # user_id = session['user_id']
    # pastes = paste.query.filter(paste.user_id == user_id).all()
    if 'user_id' in session:
        return render_template('user_paste.html')
    else:
        return jsonify({'error': 'Please Login to Continue'}), 400
    # return jsonify(success=True, pastes=[paste.to_dict() for paste in
    # pastes])


@mod_paste.route('/<username>/api/paste', methods=['POST'])
#@requires_admin
def get_user_pastes_object(username):
    # admin_id = session['user_id']
    # admin = User.query.filter(admin_id == User.id).first()
    user = User.query.filter(User.username == username).first()
    pastes = Paste.query.filter(Paste.user_id == user.id).all()
    active = []
    for paste in pastes:
        if is_active(paste):
            active.append(paste.to_dict())
        else:
            userid_to_red = paste.user_id
            user_to_red = User.query.filter(User.id == userid_to_red).first()
            user_to_red.paste_count = user_to_red.paste_count - 1
            db.session.delete(paste)
            db.session.commit()
    return jsonify({'paste_list': active, 'username': user.username}), 200
