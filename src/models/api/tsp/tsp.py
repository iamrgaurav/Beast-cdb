from src.models.sim.sim import Sim


class TSPApi:
    @staticmethod
    def get_sims_by_aadhaar(aadhaar):
        sims = Sim.get_by_aadhaar(aadhaar)
        return {'aadhaar_no':aadhaar,
                'sim':[{'lsa':sim.lsa,
                        'tsp':sim.tsp,
                        'mobile':sim.sim_no
                        } for sim in sims]} if sims is not None else None

