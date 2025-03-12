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
        # Call the constructor of the parent GUI class.
        super().__init__()

        # Create an ExperimentController instance to manage the simulation.
        self.controller = ExperimentController()

        # Set the window title.
        self.title("Initialize Experiment (Hotel Reservation)")

        # Set the size of the window (width x height).
        self.geometry("550x250")

        # --- Top Labels ---
        # Create a label for time-related input information.
        tk.Label(self, text="Time Info").grid(row=0, columnspan=2)

        # --- Input Fields for Time Parameters ---
        # Create label and entry for total experiment days with a valid range hint.
        tk.Label(self, text="Experiment duration day(12-30):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_days = tk.Entry(self, width=5)
        self.entry_days.grid(row=1, column=1, padx=10, pady=5)
        self.entry_days.insert(0, "20")  # Default value

        # Create label and entry for steps per day with a valid range hint.
        tk.Label(self, text="Hours per step(1-5):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_step = tk.Entry(self, width=5)
        self.entry_step.grid(row=2, column=1, padx=10, pady=5)
        self.entry_step.insert(0, "3")  # Default value

        # --- Input Fields for Request Number Range ---
        # Create a label for request number input with a hint of the valid range.
        tk.Label(self, text="The number of requests(1-6)").grid(row=0, column=2, columnspan=2)
        # Create labels for the minimum and maximum number of requests per step.
        tk.Label(self, text="Min").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        tk.Label(self, text="Max").grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.min_request_num = tk.Entry(self, width=5)
        self.max_request_num = tk.Entry(self, width=5)
        self.min_request_num.grid(row=1, column=3)
        self.max_request_num.grid(row=2, column=3)
        self.min_request_num.insert(0, "3")  # Default value
        self.max_request_num.insert(0, "5")  # Default value

        # --- Input Fields for Room Numbers ---
        # Create a label indicating room numbers must be provided for each room type.
        tk.Label(self, text="The number of rooms(4-6 for each room)").grid(
            row=3, column=1, columnspan=2, padx=10, pady=10, sticky="e"
        )
        # Create labels for each room type.
        tk.Label(self, text="Single").grid(row=4, column=0, sticky="w", padx=1)
        tk.Label(self, text="Double").grid(row=4, column=2, sticky="w")
        tk.Label(self, text="Double(Sofa)").grid(row=5, column=0, sticky="w")
        tk.Label(self, text="Half Lux").grid(row=5, column=2, sticky="w")
        tk.Label(self, text="Lux").grid(row=6, column=0, sticky="w")

        # Create entry fields for each room type count.
        self.single = tk.Entry(self, width=5)
        self.double = tk.Entry(self, width=5)
        self.double_sofa = tk.Entry(self, width=5)
        self.half_lux = tk.Entry(self, width=5)
        self.lux = tk.Entry(self, width=5)

        # Position the room count entry fields in the grid.
        self.single.grid(row=4, column=1, pady=5, sticky="w")
        self.double.grid(row=4, column=3, pady=5, sticky="w")
        self.double_sofa.grid(row=5, column=1, pady=5, sticky="w")
        self.half_lux.grid(row=5, column=3, pady=5, sticky="w")
        self.lux.grid(row=6, column=1, pady=5, sticky="w")

        # Set default values for room counts.
        self.single.insert(0, "5")
        self.double.insert(0, "5")
        self.double_sofa.insert(0, "5")
        self.half_lux.insert(0, "5")
        self.lux.insert(0, "5")

        # --- Buttons ---
        # Create a "Start" button to validate input and start the experiment.
        self.start_button = tk.Button(self, text="Start", command=self.start_experiment)
        self.start_button.grid(row=6, column=2, columnspan=2, pady=5, sticky="w")

        # Create an "Exit" button to terminate the application.
        self.exit_button = tk.Button(self, text="Exit", command=self.terminate)
        self.exit_button.grid(row=6, column=3, columnspan=2, pady=5)

    def parameter_input(self) -> Optional[Tuple[int, int, Dict[RoomType, int], Tuple[int, int]]]:
        """
        Retrieves and validates user input from the Entry widgets.
        
        :return: A tuple containing:
                 - days (int): Total days for the experiment.
                 - step (int): Steps per day.
                 - rooms (Dict[RoomType, int]): Dictionary mapping each room type to its count.
                 - request number range (Tuple[int, int]): A tuple (min_request, max_request).
                 Returns None if any validation fails.
        """
        # Collect room numbers from entry fields into a dictionary.
        rooms = {
            RoomType.SINGLE: self.single.get(),
            RoomType.SIMPLE_DOUBLE: self.double.get(),
            RoomType.DOUBLE_WITH_SOFA: self.double_sofa.get(),
            RoomType.HALF_LUX: self.half_lux.get(),
            RoomType.LUX: self.lux.get()
        }
        # Retrieve the time and request parameters from entry fields.
        days = self.entry_days.get()
        step = self.entry_step.get()
        min_req = self.min_request_num.get()
        max_req = self.max_request_num.get()
        # Create a parameters dictionary for validation.
        params = {"days": days, "steps": step, "min_req": min_req, "max_req": max_req}

        # Validate input values using the check_valid_input method.
        if not self.check_valid_input(params, list(rooms.values())):
            messagebox.showerror("Error", "Please check input value.")
            return None

        # Convert all string inputs to integers.
        days, step, min_req, max_req = int(days), int(step), int(min_req), int(max_req)
        for key, val in rooms.items():
            rooms[key] = int(val)

        return days, step, rooms, (min_req, max_req)

    def check_valid_input(self, params: Dict[str, str], rooms: list[str]) -> bool:
        """
        Validates the user input values based on specified criteria.
        
        :param params: A dictionary containing the string inputs for days, steps, min_req, and max_req.
        :param rooms: A list of string inputs representing the number of rooms for each room type.
        :return: True if all inputs meet the criteria; otherwise, False.
        """
        try:
            # Validate days: must be a digit and between 12 and 30.
            assert params["days"] and params["days"].isdigit() and 12 <= int(params["days"]) <= 30
            # Validate steps: must be a digit and between 1 and 6.
            assert params["steps"] and params["steps"].isdigit() and 1 <= int(params["steps"]) <= 6
            # Validate request range: both min_req and max_req must be digits and min_req < max_req, within 1 to 6.
            assert (
                params["min_req"] and params["max_req"]
                and params["min_req"].isdigit()
                and params["max_req"].isdigit()
                and 1 <= int(params["min_req"]) < int(params["max_req"]) <= 6
            )

            # Validate each room number: must be a digit and between 4 and 6.
            for val in rooms:
                assert val and val.isdigit() and 4 <= int(val) <= 6, f"room {val}"
        except Exception:
            return False
        return True

    def start_experiment(self) -> None:
        """
        Validates the user input and, if valid, initializes the experiment.
        Opens the ObservationWindow for further experiment visualization.
        """
        # Retrieve and validate user input parameters.
        params = self.parameter_input()
        # If input validation fails, exit without starting the experiment.
        if params is None:
            return

        days, step, rooms, request_num = params

        # Initialize the experiment using the controller with the provided parameters.
        self.controller.initialize_experiment(days, step, rooms, request_num)

        # Hide the initialization window.
        self.withdraw()

        # Create and display the ObservationWindow using the initialized controller.
        obs_win = ObservationWindow(self, controller=self.controller)
        obs_win.mainloop()

    def terminate(self) -> None:
        """
        Terminates the application by closing the window.
        """
        self.destroy()
