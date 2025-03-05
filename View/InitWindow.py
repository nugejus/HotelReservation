import tkinter as tk
from tkinter import messagebox
from typing import *

from Model.RoomType import RoomType

from View.GUI import GUI
from View.ObservationWindow import ObservationWindow

from Controller import ExperimentController

class InitWindow(GUI):
    def __init__(self) -> None:
        # Call the constructor of the parent GUI class
        super().__init__()

        # self.controller = SimulationController()
        self.controller = ExperimentController()
        
        # Set the title of the window
        self.title("Initialize Experiment")
        
        # Set the size of the window (width x height)
        self.geometry("250x250")

        tk.Label(self, text="Time Info").grid(row = 0, columnspan=2)
        tk.Label(self, text="Request Num").grid(row = 0, column=2, columnspan=2)
        
        # Label and Entry for "Days for experiments"
        tk.Label(self, text="Days:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_days = tk.Entry(self, width=5)
        self.entry_days.grid(row=1, column=1, padx=10, pady=5)
        
        # Label and Entry for "Steps for each day"
        tk.Label(self, text="Steps:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_step = tk.Entry(self, width=5)
        self.entry_step.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="Min").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        tk.Label(self, text="Max").grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.min_request_num = tk.Entry(self, width=5)
        self.max_request_num = tk.Entry(self, width=5)

        self.min_request_num.grid(row = 1, column=3)
        self.max_request_num.grid(row = 2, column=3)

        # Labels for entering the number of rooms
        tk.Label(self, text="Room numbers").grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="e")
        tk.Label(self, text="Single").grid(row=4, column=0, sticky="w", padx=1)
        tk.Label(self, text="Double").grid(row=4, column=2, sticky="w")
        tk.Label(self, text="Double(Sofa)").grid(row=5, column=0, sticky="w")
        tk.Label(self, text="Half Lux").grid(row=5, column=2, sticky="w")
        tk.Label(self, text="Lux").grid(row=6, column=0, sticky="w")

        # Entry fields for each room type
        self.single = tk.Entry(self, width=5)
        self.double = tk.Entry(self, width=5)
        self.double_sofa = tk.Entry(self, width=5)
        self.half_lux = tk.Entry(self, width=5)
        self.lux = tk.Entry(self, width=5)
        
        # Positioning the Entry fields in the grid
        self.single.grid(row=4, column=1, pady=5, sticky="w")
        self.double.grid(row=4, column=3, pady=5, sticky="w")
        self.double_sofa.grid(row=5, column=1, pady=5, sticky="w")
        self.half_lux.grid(row=5, column=3, pady=5, sticky="w")
        self.lux.grid(row=6, column=1, pady=5, sticky="w")

        
        # Button to start the experiment
        self.start_button = tk.Button(self, text="Start", command=self.start_experiment)
        self.start_button.grid(row=6, column=2, columnspan=2, pady=5, sticky="w")

        # Button to exit the program
        self.exit_button = tk.Button(self, text="Exit", command=self.terminate)
        self.exit_button.grid(row=6, column=3, columnspan=2, pady=5)

    def parameter_input(self) -> Tuple[int, int, Dict[RoomType, int]]:
        # Gather the entered room numbers into a dictionary
        rooms = {
            RoomType.SINGLE: self.single.get(),
            RoomType.SIMPLE_DOUBLE: self.double.get(),
            RoomType.DOUBLE_WITH_SOFA: self.double_sofa.get(),
            RoomType.HALF_LUX: self.half_lux.get(),
            RoomType.LUX: self.lux.get()
        }
        # Get the number of days and steps from the Entry fields
        days = self.entry_days.get()
        step = self.entry_step.get()
        min_req = self.min_request_num.get()
        max_req = self.max_request_num.get()

        # Validate that days and step are integers
        days = days if days else "20" # default value
        step = step if step else "10" # default value
        min_req = min_req if min_req else "1" # default value
        max_req = max_req if max_req else "5" # default value

        if not days.isdigit() or not step.isdigit():
            messagebox.showerror("Error", "Required INTEGER value.")
            return

        # Validate that each room count is also an integer
        for key, value in rooms.items():
            value = value if value else "5" # default value
            if not value.isdigit():
                messagebox.showerror("Error", "Required INTEGER value.")
                return
            else:
                # Convert the valid strings to integers
                rooms[key] = int(value)

        return int(days), int(step), rooms, (int(min_req), int(max_req))
    
    def start_experiment(self) -> None:
        """
        Validates user input, converts them to integers if valid,
        and then opens the ObservationWindow to start the experiment.
        """
        days, step, rooms, request_num = self.parameter_input()        

        self.controller.initialize_experiment(days, step, rooms, request_num)

        # Hide the current window (InitWindow)
        self.withdraw()
        
        # Create and display the ObservationWindow
        obs_win = ObservationWindow(self, controller = self.controller)
        obs_win.mainloop()
    
    def terminate(self) -> None:
        """
        Closes the current window and ends the program.
        """
        self.destroy()
