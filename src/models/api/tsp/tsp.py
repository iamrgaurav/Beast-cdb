from src.models.sim.sim import Sim


class TSPApi:
    @staticmethod
    def get_sims_by_aadhaar(aadhaar, tsp):
        sims = Sim.get_by_aadhaar(aadhaar)
        return {'aadhaar_no': aadhaar,
                'sim': [{'lsa': sim.lsa,
                         'tsp': sim.tsp,
                         'mobile': sim.sim_no,
                         'issue_date':sim.issue_date.strftime("%Y-%m-%d")
                         } for sim in sims if tsp == sim.tsp]if sims is not None else 0,
                'sims_by_other_tsp': Sim.get_sim_count_by_tsp(aadhaar),
                'Total Sim':len(sims)
                }
    @staticmethod
    def save_sim(mobile, tsp, issue_date, lsa, aadhaar_no):
        return Sim(aadhaar_no,mobile,tsp,lsa,issue_date).save_to_db()


