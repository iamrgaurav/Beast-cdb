import uuid
import src.models.sim.constants as SimConstants
from src.common.database import Database
import datetime


class Sim:
    def __init__(self, aadhaar_no, sim_no, tsp, lsa, issue_date,_id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.aadhaar_no = aadhaar_no
        self.sim_no = sim_no
        self.tsp = tsp
        self.lsa = lsa
        self.issue_date = datetime.datetime.strptime(issue_date,"%Y-%m-%d") if isinstance(issue_date, str) else issue_date

    def json(self):
        return {
            '_id': self._id,
            'sim_no': self.sim_no,
            'aadhaar_no': self.aadhaar_no,
            'tsp': self.tsp,
            'lsa': self.lsa,
            'issue_date': self.issue_date
        }

    def save_to_db(self):
        return Database.update(SimConstants.COLLECTIONS, {'_id': self._id}, self.json())

    def remove_from_db(self):
        return True if Database.delete(SimConstants.COLLECTIONS, {'_id': self._id}) else False

    @classmethod
    def get_by_aadhaar(cls, aadhaar_no):
        cluster_data = Database.find(SimConstants.COLLECTIONS, {'aadhaar_no': aadhaar_no})
        return [cls(**data) for data in cluster_data if data is not None] if cluster_data is not None else False
