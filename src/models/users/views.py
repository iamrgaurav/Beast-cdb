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
    return jsonify({'data':
        [{
            'sr_no':str(i+1),
            'sim_no':user.sim_cards[i].sim_no,
            'tsp':user.sim_cards[i].tsp,
            'lsa':user.sim_cards[i].lsa,
            'issue_date':"{}".format(user.sim_cards[i].issue_date.strftime('%d/%m/%Y'))
             }
            for i in range(len(user.sim_cards))]
    })
