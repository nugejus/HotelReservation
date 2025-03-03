import tkinter as tk
from tkinter import messagebox

from Model.RoomType import RoomType

from View.GUI import GUI
from View.ObservationWindow import ObservationWindow

from Controller import SimulationController

class InitWindow(GUI):
    def __init__(self) -> None:
        # Call the constructor of the parent GUI class
        super().__init__()

        self.controller = SimulationController()
        
        # Set the title of the window
        self.title("Initialize Experiment")
        
        # Set the size of the window (width x height)
        self.geometry("430x250")
        
        # Label and Entry for "Days for experiments"
        tk.Label(self, text="Days for experiments:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_days = tk.Entry(self)
        self.entry_days.grid(row=0, column=1, padx=10, pady=10)
        
        # Label and Entry for "Steps for each day"
        tk.Label(self, text="Steps for each day:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_step = tk.Entry(self)
        self.entry_step.grid(row=1, column=1, padx=10, pady=10)

        # Labels for entering the number of rooms
        tk.Label(self, text="Room numbers").grid(row=2, padx=10, pady=10, sticky="e")
        tk.Label(self, text="Single").grid(row=3, column=0, sticky="w", padx=1)
        tk.Label(self, text="Double").grid(row=3, column=2, sticky="w")
        tk.Label(self, text="Double(Sofa)").grid(row=4, column=0, sticky="w")
        tk.Label(self, text="Half Lux").grid(row=4, column=2, sticky="w")
        tk.Label(self, text="Lux").grid(row=5, column=0, sticky="w")

        # Entry fields for each room type
        self.single = tk.Entry(self, width=5)
        self.double = tk.Entry(self, width=5)
        self.double_sofa = tk.Entry(self, width=5)
        self.half_lux = tk.Entry(self, width=5)
        self.lux = tk.Entry(self, width=5)
        
        # Positioning the Entry fields in the grid
        self.single.grid(row=3, column=1, sticky="w")
        self.double.grid(row=3, column=3, sticky="w")
        self.double_sofa.grid(row=4, column=1, sticky="w")
        self.half_lux.grid(row=4, column=3, sticky="w")
        self.lux.grid(row=5, column=1, sticky="w")
        
        # Button to start the experiment
        self.start_button = tk.Button(self, text="Start", command=self.start_experiment)
        self.start_button.grid(row=5, column=2, columnspan=2, pady=10, sticky="w")

        # Button to exit the program
        self.exit_button = tk.Button(self, text="Exit", command=self.terminate)
        self.exit_button.grid(row=5, column=3, columnspan=2, pady=10)
        
    def start_experiment(self) -> None:
        """
        Validates user input, converts them to integers if valid,
        and then opens the ObservationWindow to start the experiment.
        """
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
        
        # Validate that days and step are integers         
        if not days.isdigit() or not step.isdigit():
            messagebox.showerror("Error", "Required INTEGER value.")
            return

        # Validate that each room count is also an integer
        for key, value in rooms.items():
            if not value.isdigit():
                messagebox.showerror("Error", "Required INTEGER value.")
                return
            else:
                # Convert the valid strings to integers
                rooms[key] = int(value)

        # Convert days and step to integers
        days = int(days)
        step = int(step)

        self.controller.initialize_experiment(days, step, rooms)

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
