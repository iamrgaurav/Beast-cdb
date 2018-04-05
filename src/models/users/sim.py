import uuid
import datetime


from src.common.Utility.Utility import CommonUtility as SimUtility

class Sim:
    def __init__(self, sim_no, tsp, lsa, issue_date, status=1, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.sim_no = SimUtility.formating_phone(sim_no)
        self.tsp = SimUtility.formating_name(tsp)
        self.lsa = SimUtility.formating_name(lsa)
        self.status = status
        self.issue_date = datetime.datetime.strptime(issue_date, "%Y-%m-%d") if isinstance(issue_date,
                                                                                           str) else issue_date

    def json(self):
        return {
            '_id': self._id,
            'sim_no': self.sim_no,
            'tsp': self.tsp,
            'lsa': self.lsa,
            'status':self.status,
            'issue_date': self.issue_date.strftime("%Y-%m-%d")
        }