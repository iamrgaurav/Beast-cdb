from flask_restplus import Resource, Namespace
from flask import jsonify,g
from flask import request
from flask_httpauth import HTTPTokenAuth
import src.models.api.guser as guser
from src.models.api.tsp.tsp import TSPApi

TSP_namespace = Namespace('TSP','There are Various Operations regarding TSP')


auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    if token in guser.tokens:
        g.current_user = guser.tokens[token]

        return True
    return False



@TSP_namespace.route('/sim')
class User_Info(Resource):
    @TSP_namespace.doc(params={
        'aadhaar_no': {'in': 'formData', 'description': 'User Aadhaar Number', 'required': 'True'},
        'tsp': {'in': 'formData', 'description': 'TSP Name', 'required': 'True'}})
    def post(self):
        aadhaar_no = request.form['aadhaar_no']
        tsp = request.form['tsp']
        sims = TSPApi.get_sims_by_aadhaar(aadhaar_no,tsp)
        return jsonify({"data": sims})
@TSP_namespace.route('/')
class User_Info_add(Resource):
    @TSP_namespace.doc(params={
        'auth': {'in': 'header', 'description': 'User Aadhaar Number', 'required': 'True'},
        'aadhaar_no': {'in': 'formData', 'description': 'User Aadhaar Number', 'required': 'True'},
        'mobile_no':{'in': 'formData', 'description': 'User Phone Number in Format +91xxxxxxxxxxx', 'required': 'True'},
        'tsp':{'in': 'formData', 'description': 'Name of TSP', 'required': 'True'},
        'issue_date':{'in': 'formData', 'description': 'Issue Date Time', 'required': 'True'},
        'lsa':{'in': 'formData', 'description': 'LSA', 'required': 'True'},
    })
    def post(self):
        mobile = request.form['mobile_no']
        tsp = request.form['tsp']
        issue_date = request.form['issue_date']
        lsa = request.form['lsa']
        aadhaar_no = request.form['aadhaar_no']
        return 200 if TSPApi.save_sim(mobile,tsp,issue_date,lsa,aadhaar_no) else 400





