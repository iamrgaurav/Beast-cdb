from flask_restplus import Resource, Namespace,fields
from flask import jsonify
from flask import request

from src.models.api.dot.Admin import AdminAPI

TSP_namespace = Namespace('TSP','There are Various Operations regarding TSP')


@admin_namespace.route('/')
class User_Info(Resource):
    @user_namespace.doc(params={
        'aadhaar_no': {'in': 'formData', 'description': 'User Aadhaar Number', 'required': 'True'}})
    def get(self):
        aadhaar = request.form['aadhaar_no']
        sims = TSPApi.get_sims_by_aadhaar(aadhaar)
        return jsonify({"data": sims})