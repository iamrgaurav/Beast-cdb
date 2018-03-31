from flask import Blueprint, render_template, session, jsonify
from src.models.users.user import User
user_blueprint = Blueprint('users', __name__)
@user_blueprint.route('/dashboard/<user_id>')
def view_dashboard(user_id):
    user = User.get_by_id(user_id)
    return render_template('user/dashboard.html', user=user)

@user_blueprint.route('/sim')
def user_sim():
    user = User.get_by_id(session['uid'])
    sims = user.get_sim_details()
    return jsonify({'data':
        [{
            'sr_no':str(i+1),
            'sim_no':sims[i].sim_no,
            'tsp':sims[i].tsp,
            'lsa':sims[i].lsa,
            'issue_date':"{}".format(sims[i].issue_date.strftime('%d/%m/%Y'))
             }
            for i in range(len(sims))]
    })
