import tkinter as tk
from tkinter import messagebox
from Experiment import Experiment
from RoomType import RoomType
from GUI import GUI

from typing import *

class ObservationWindow(tk.Toplevel, GUI):
    def __init__(self, parent, days: int, step: int, rooms: Dict[RoomType, int]) -> None:
        """
        This class creates a separate observation window for the running experiment.
        It inherits from tk.Toplevel (for creating a new top-level window) and GUI (for shared GUI-related functionalities).
        
        :param parent: The parent window (InitWindow) instance
        :param days: Total days for the experiment
        :param step: The time interval (hours) per step
        :param rooms: A dictionary containing the number of rooms per RoomType
        """
        super().__init__(parent)
        
        # Store references to parent and experiment parameters
        self.parent = parent
        self.days = days
        self.step = step

        # Set window title and size
        self.title("Experiment Observation")
        self.geometry("1200x400")

        # ========== Top label (displays total days / steps) ==========
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.lbl_experiment_info = tk.Label(
            top_frame,
            text=f"Total day = {days} days, hour per step = {step} hour",
            font=("Arial", 11, "bold")
        )
        self.lbl_experiment_info.pack(side=tk.LEFT)

        # ========== Left-side information area ==========
        left_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ---- Time Info ----
        tk.Label(left_frame, text="Time Info", font=("Arial", 10, "underline")).grid(row=0, column=0, pady=5)
        tk.Label(left_frame, text="Today:").grid(row=1, column=0, pady=2)
        tk.Label(left_frame, text="Now:").grid(row=2, column=0, pady=2)

        self.time_today = tk.Text(left_frame, height=1, width=5)
        self.time_now = tk.Text(left_frame, height=1, width=5)

        self.time_today.grid(row=1, column=1, pady=2)
        self.time_now.grid(row=2, column=1, pady=2)

        # ---- Statistics ----
        tk.Label(left_frame, text="Statistics", font=("Arial", 10, "underline")).grid(row=3, pady=5)

        tk.Label(left_frame, text="Mean occupancy today:").grid(row=4, column=0, pady=2)
        tk.Label(left_frame, text="Profit:").grid(row=5, column=0, pady=2)
        tk.Label(left_frame, text="Successful request percentage:").grid(row=6, column=0, pady=2)

        self.avg_occupancy = tk.Text(left_frame, height=1, width=5)
        self.profit = tk.Text(left_frame, height=1, width=5)
        self.success_rate = tk.Text(left_frame, height=1, width=5)

        self.avg_occupancy.grid(row=4, column=1, pady=2)
        self.profit.grid(row=5, column=1, pady=2)
        self.success_rate.grid(row=6, column=1, pady=2)

        # ========== Right-side information area ==========
        right_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ---- Request Flow ----
        flow_frame = tk.Frame(right_frame)
        flow_frame.pack(side=tk.TOP, fill=tk.BOTH)

        tk.Label(flow_frame, text="Request Flow", font=("Arial", 10, "underline")).grid(row=0, pady=5)

        self.flow_info = tk.Text(flow_frame, height=10, width=100)
        self.flow_info.grid(row=1)

        # ---- Occupancy information of each room ----
        occupancy_frame = tk.Frame(right_frame)
        occupancy_frame.pack(side=tk.TOP, fill=tk.BOTH)

        tk.Label(occupancy_frame, text="Occupancy of each room", font=("Arial", 10, "underline")).grid(row=2, columnspan=4, sticky=tk.N)

        tk.Label(occupancy_frame, text="Single").grid(row=3, column=0, sticky="w")
        tk.Label(occupancy_frame, text="Double").grid(row=3, column=2, sticky="e")
        tk.Label(occupancy_frame, text="Double(Sofa)").grid(row=4, column=0, sticky="w")
        tk.Label(occupancy_frame, text="Half Lux").grid(row=4, column=2, sticky="e")
        tk.Label(occupancy_frame, text="Lux").grid(row=5, column=0, sticky="w")

        self.occupancy_single = tk.Text(occupancy_frame, height=1, width=5)
        self.occupancy_double = tk.Text(occupancy_frame, height=1, width=5)
        self.occupancy_double_sofa = tk.Text(occupancy_frame, height=1, width=5)
        self.occupancy_half_lux = tk.Text(occupancy_frame, height=1, width=5)
        self.occupancy_lux = tk.Text(occupancy_frame, height=1, width=5)

        self.occupancy_single.grid(row=3, column=1, pady=2, sticky="w")
        self.occupancy_double.grid(row=3, column=3, pady=2, sticky="e")
        self.occupancy_double_sofa.grid(row=4, column=1, pady=2, sticky="w")
        self.occupancy_half_lux.grid(row=4, column=3, pady=2, sticky="e")
        self.occupancy_lux.grid(row=5, column=1, pady=2, sticky="w")

        # ========== Bottom buttons ==========
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        self.btn_step = tk.Button(bottom_frame, text="Next step", command=self.next_stage)
        self.btn_step.pack(side=tk.LEFT, padx=5)

        self.btn_exit = tk.Button(bottom_frame, text="Exit", command=self.terminate)
        self.btn_exit.pack(side=tk.RIGHT, padx=5)

        # Initialize the Experiment instance
        self.experiment = Experiment(days, step, rooms)
    
    def terminate(self) -> None:
        """
        Terminates the current observation window and also destroys the parent window.
        This effectively ends the entire program flow.
        """
        messagebox.showinfo("Termination", "The Experiment has been terminated.")
        self.destroy()
        self.parent.destroy()

    def delete(self) -> None:
        """
        A helper method to clear out all the text fields before updating them.
        This prevents old data from persisting between steps.
        """
        self.flow_info.delete(1.0, tk.END)
        self.time_today.delete(1.0, tk.END)
        self.time_now.delete(1.0, tk.END)
        self.avg_occupancy.delete(1.0, tk.END)
        self.profit.delete(1.0, tk.END)
        self.success_rate.delete(1.0, tk.END)
        self.occupancy_single.delete(1.0, tk.END)
        self.occupancy_double.delete(1.0, tk.END)
        self.occupancy_double_sofa.delete(1.0, tk.END)
        self.occupancy_half_lux.delete(1.0, tk.END)
        self.occupancy_lux.delete(1.0, tk.END)

    def endExperiment(self) -> None:
        """
        Called when the experiment (simulation) finishes all its steps.
        Displays final statistics (if desired) and terminates the program.
        """
        # If you want to display overall statistics across all days, 
        # you could implement something like experiment.displayFinalStatistics() in Experiment.
        # For now, we'll just reuse the current statistics as an example.
        
        final_stats = self.experiment.displayStatistics()  # Using current stats as final result
        messagebox.showinfo("Experiment Completed", f"Experiment has ended.\n\n{final_stats}")
        
        # Close this window and end the program
        self.terminate()

    def next_stage(self) -> None:
        """
        Called when the 'Next step' button is clicked.
        Runs one step of the experiment, updates the GUI fields, and checks if the experiment has ended.
        """
        # Clear existing text to avoid overlapping old data
        self.delete()
        
        # Perform one step in the simulation
        is_running = self.experiment.step()

        # If the experiment is no longer running, display final stats and terminate
        if not is_running:
            self.endExperiment()
            return

        # Otherwise, update the UI with the latest data
        day, hour = self.experiment.getTimeInfo()
        statistics = self.experiment.displayStatistics()
        
        # Insert reservation (request) info into the flow_info text box
        self.flow_info.insert(tk.END, self.experiment.displayReservationInfo())
        
        # Time-related info
        self.time_today.insert(tk.END, day)
        self.time_now.insert(tk.END, hour)

        # Statistics info
        self.avg_occupancy.insert(tk.END, statistics["avg_occupancy"])
        self.profit.insert(tk.END, statistics["profit"])
        self.success_rate.insert(tk.END, statistics["success_rate"])

        # Room occupancy info
        room_occupancy = self.experiment.displayTodayOccupancy()
        self.occupancy_single.insert(tk.END, room_occupancy[RoomType.SINGLE])
        self.occupancy_double.insert(tk.END, room_occupancy[RoomType.SIMPLE_DOUBLE])
        self.occupancy_double_sofa.insert(tk.END, room_occupancy[RoomType.DOUBLE_WITH_SOFA])
        self.occupancy_half_lux.insert(tk.END, room_occupancy[RoomType.HALF_LUX])
        self.occupancy_lux.insert(tk.END, room_occupancy[RoomType.LUX])
