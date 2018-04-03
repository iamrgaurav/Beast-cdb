import requests
from flask import Blueprint, request, session, redirect, url_for, render_template, jsonify

from src.models.dot.dot import Admin
from src.models.dot.errors import AdminError

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/')
def home():
    if 'uid' not in session.keys() or session['uid']==None:
        return render_template('dot/home.html')
    else:
        return redirect(url_for('redirect_to_dash'))

@admin_blueprint.route('/dashboard/<user_id>')
def view_dashboard(user_id):
    admin = Admin.get_by_id(user_id)
    return render_template('dot/dashboard.html', admin = admin)


@admin_blueprint.route('/login', methods = ["GET", "POST"])
def login_user():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        try:
            admin = Admin.is_login_valid(username, password)
            if admin:
                session['uid'] = admin._id
                return redirect(url_for(".redirect_to_dash"))
        except AdminError as e:
            return e.msg
    return render_template('dot/login.html')

@admin_blueprint.route('/to-dash/redirecting')
def redirect_to_dash():
    if session['uid']==None:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('.view_dashboard', user_id = session['uid']))

@admin_blueprint.route('/list-by-lsa')
def list_by_lsa():
    return render_template('dot/lsa.html')

@admin_blueprint.route('/by-lsa')
def ajax_by_lsa():
    lsa = request.form['lsa']
    req = requests.post("https://beast-cdb.herokuapp.com", data = {"lsa":lsa}).json()
    return jsonify({'data':
        [{
            'sr_no':str(i+1),
            'aadhaar':req['data'][i]['aadhaar'],
            'count': req['data'][i]['count'],
        }
            for i in range(len(req['data']))]
    })

@admin_blueprint.route('/list-by-count')
def list_by_count():
    return render_template('dot/sim_counts.html')

@admin_blueprint.route('/by-count')
def ajax_by_count():
    count = request.form['count']
    req = requests.post("https://beast-cdb.herokuapp.com", data = {"lsa":count}).json()
    return jsonify({'data':
        [{
            'sr_no':str(i+1),
            'aadhaar':req['data'][i]['aadhaar'],
            'count': req['data'][i]['count']
        }
            for i in range(len(req['data']))]
    })