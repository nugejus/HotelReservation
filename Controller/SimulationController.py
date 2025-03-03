from Model import Experiment

class SimulationController:
    def __init__(self):
        self.experiment = None

    def initialize_experiment(self, days, step, rooms_info):
        self.experiment = Experiment(days, step, rooms_info)

    def step(self):
        if not self.experiment:
            return False
        return self.experiment.step()

    def get_statistics(self):
        if not self.experiment:
            return {}
        return self.experiment.displayStatistics()

    def get_time_info(self):
        if not self.experiment:
            return (0, 0)
        return self.experiment.getTimeInfo()

    def get_reservation_info(self):
        if not self.experiment:
            return ""
        return self.experiment.displayReservationInfo()

    def get_today_occupancy(self):
        if not self.experiment:
            return {}
        return self.experiment.displayTodayOccupancy()
    
    def get_init_info(self):
        return self.experiment.get_init_info()

    def terminate_experiment(self):
        self.experiment = None
