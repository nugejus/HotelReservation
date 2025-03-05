import tkinter as tk
from tkinter import messagebox
from typing import Tuple, Dict, Optional

from Model.RoomType import RoomType

from View.GUI import GUI
from View.ObservationWindow import ObservationWindow

from Controller import ExperimentController

class InitWindow(GUI):
    def __init__(self) -> None:
        """
        Initializes the experiment initialization window.
        Sets up the ExperimentController, window properties, and all input widgets.
        """
        # Call the constructor of the parent GUI class
        super().__init__()

        # Initialize the ExperimentController instance
        self.controller = ExperimentController()
        
        # Set the title of the window
        self.title("Initialize Experiment")
        
        # Set the size of the window (width x height)
        self.geometry("250x250")

        # Create labels for the top row: Time Info and Request Num
        tk.Label(self, text="Time Info").grid(row=0, columnspan=2)
        tk.Label(self, text="Request Num").grid(row=0, column=2, columnspan=2)
        
        # Label and Entry for "Days" (total days for experiments)
        tk.Label(self, text="Days:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_days = tk.Entry(self, width=5)
        self.entry_days.grid(row=1, column=1, padx=10, pady=5)
        
        # Label and Entry for "Steps" (steps per day)
        tk.Label(self, text="Steps:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_step = tk.Entry(self, width=5)
        self.entry_step.grid(row=2, column=1, padx=10, pady=5)

        # Labels and entries for minimum and maximum number of requests per step
        tk.Label(self, text="Min").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        tk.Label(self, text="Max").grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.min_request_num = tk.Entry(self, width=5)
        self.max_request_num = tk.Entry(self, width=5)
        self.min_request_num.grid(row=1, column=3)
        self.max_request_num.grid(row=2, column=3)

        # Label for "Room numbers" and labels for each room type
        tk.Label(self, text="Room numbers").grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="e")
        tk.Label(self, text="Single").grid(row=4, column=0, sticky="w", padx=1)
        tk.Label(self, text="Double").grid(row=4, column=2, sticky="w")
        tk.Label(self, text="Double(Sofa)").grid(row=5, column=0, sticky="w")
        tk.Label(self, text="Half Lux").grid(row=5, column=2, sticky="w")
        tk.Label(self, text="Lux").grid(row=6, column=0, sticky="w")

        # Create Entry widgets for each room type count
        self.single = tk.Entry(self, width=5)
        self.double = tk.Entry(self, width=5)
        self.double_sofa = tk.Entry(self, width=5)
        self.half_lux = tk.Entry(self, width=5)
        self.lux = tk.Entry(self, width=5)
        
        # Position the room count Entry fields in the grid
        self.single.grid(row=4, column=1, pady=5, sticky="w")
        self.double.grid(row=4, column=3, pady=5, sticky="w")
        self.double_sofa.grid(row=5, column=1, pady=5, sticky="w")
        self.half_lux.grid(row=5, column=3, pady=5, sticky="w")
        self.lux.grid(row=6, column=1, pady=5, sticky="w")

        # Button to start the experiment after validating parameters
        self.start_button = tk.Button(self, text="Start", command=self.start_experiment)
        self.start_button.grid(row=6, column=2, columnspan=2, pady=5, sticky="w")

        # Button to exit the program
        self.exit_button = tk.Button(self, text="Exit", command=self.terminate)
        self.exit_button.grid(row=6, column=3, columnspan=2, pady=5)

    def parameter_input(self) -> Optional[Tuple[int, int, Dict[RoomType, int], Tuple[int, int]]]:
        """
        Retrieves and validates user input from the Entry widgets.
        Provides default values if inputs are empty.
        
        :return: A tuple containing:
                 - days (int): Total days for the experiment.
                 - step (int): Steps per day.
                 - rooms (Dict[RoomType, int]): Dictionary mapping each room type to its count.
                 - request number range (Tuple[int, int]): A tuple (min_request, max_request).
                 Returns None if any validation fails.
        """
        # Collect room numbers from Entry widgets into a dictionary.
        rooms = {
            RoomType.SINGLE: self.single.get(),
            RoomType.SIMPLE_DOUBLE: self.double.get(),
            RoomType.DOUBLE_WITH_SOFA: self.double_sofa.get(),
            RoomType.HALF_LUX: self.half_lux.get(),
            RoomType.LUX: self.lux.get()
        }
        # Retrieve time and request parameters from Entry widgets.
        days = self.entry_days.get()
        step = self.entry_step.get()
        min_req = self.min_request_num.get()
        max_req = self.max_request_num.get()

        # Use default values if entries are empty.
        days = days if days else "20"  # default number of days
        step = step if step else "10"  # default step size
        min_req = min_req if min_req else "1"  # default minimum number of requests
        max_req = max_req if max_req else "5"  # default maximum number of requests

        # Validate that 'days' and 'step' are integers.
        if not days.isdigit() or not step.isdigit():
            messagebox.showerror("Error", "Required INTEGER value for Days and Steps.")
            return None

        # Validate each room count entry is an integer; use a default of "5" if empty.
        for key, value in rooms.items():
            value = value if value else "5"  # default room count
            if not value.isdigit():
                messagebox.showerror("Error", "Required INTEGER value for room numbers.")
                return None
            else:
                # Convert the valid string to an integer.
                rooms[key] = int(value)

        # Return the parsed parameters as a tuple.
        return int(days), int(step), rooms, (int(min_req), int(max_req))
    
    def start_experiment(self) -> None:
        """
        Validates the user input and, if valid, initializes the experiment.
        Opens the ObservationWindow for further experiment visualization.
        """
        params = self.parameter_input()
        # If input validation failed, do not proceed.
        if params is None:
            return
        
        days, step, rooms, request_num = params

        # Initialize the experiment using the controller.
        self.controller.initialize_experiment(days, step, rooms, request_num)

        # Hide the initialization window.
        self.withdraw()
        
        # Create and display the ObservationWindow with the initialized controller.
        obs_win = ObservationWindow(self, controller=self.controller)
        obs_win.mainloop()
    
    def terminate(self) -> None:
        """
        Terminates the application by closing the window.
        """
        self.destroy()
