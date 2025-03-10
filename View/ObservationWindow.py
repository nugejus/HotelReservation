import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

from Model.RoomType import RoomType
from View.GUI import GUI
from typing import *

class ObservationWindow(tk.Toplevel, GUI):
    def __init__(self, parent, controller) -> None:
        """
        Creates a separate observation window for monitoring the running experiment.
        Inherits from tk.Toplevel to create a new top-level window and GUI for shared functionalities.
        
        :param parent: The parent window (e.g., an instance of InitWindow).
        :param controller: The ExperimentController instance managing the simulation.
        """
        # Initialize the Toplevel window with the parent
        super().__init__(parent)
        
        # Store references to the parent window and the experiment controller
        self.parent = parent
        self.controller = controller

        # Set the window title and size
        self.title("Experiment Observation(Hotel booking and check-in support system)")
        self.geometry("1200x400")

        # ========= Top Label (Displays initial experiment settings) =========
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Retrieve initial experiment parameters (total days and hours per step)
        days, step = self.controller.get_init_info()
        self.lbl_experiment_info = tk.Label(
            top_frame,
            text=f"Total days = {days} day, hour per step = {step} hours",
            font=("Arial", 11, "bold")
        )
        self.lbl_experiment_info.pack(side=tk.LEFT)

        # ========= Left-side Information Area =========
        left_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ---- Time Information ----
        tk.Label(left_frame, text="Time Info", font=("Arial", 10, "underline")).grid(row=0, column=0, pady=5)
        tk.Label(left_frame, text="Date:").grid(row=1, column=0, pady=2)
        tk.Label(left_frame, text="Time:").grid(row=2, column=0, pady=2)

        # Text widgets to display the current simulation day and hour
        self.time_today = tk.Text(left_frame, height=1, width=5)
        self.time_now = tk.Text(left_frame, height=1, width=5)
        self.time_today.grid(row=1, column=1, pady=2)
        self.time_now.grid(row=2, column=1, pady=2)

        # ---- Statistics Information ----
        tk.Label(left_frame, text="Statistics", font=("Arial", 10, "underline")).grid(row=3, pady=5)
        tk.Label(left_frame, text="Average occupancy:").grid(row=4, column=0, pady=2)
        tk.Label(left_frame, text="Profit:").grid(row=5, column=0, pady=2)
        tk.Label(left_frame, text="Successful request %:").grid(row=6, column=0, pady=2)

        # Text widgets to display average occupancy, profit, and success rate
        self.avg_occupancy = tk.Text(left_frame, height=1, width=5)
        self.profit = tk.Text(left_frame, height=1, width=5)
        self.success_rate = tk.Text(left_frame, height=1, width=5)
        self.avg_occupancy.grid(row=4, column=1, pady=2)
        self.profit.grid(row=5, column=1, pady=2)
        self.success_rate.grid(row=6, column=1, pady=2)

        # ========= Right-side Information Area =========
        right_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ---- Request Flow Section ----
        flow_frame = tk.Frame(right_frame)
        flow_frame.pack(side=tk.TOP, fill=tk.BOTH)
        tk.Label(flow_frame, text="Request Flow", font=("Arial", 10, "underline")).grid(row=0, pady=5)
        # Text widget to display the flow of reservation requests and their outcomes
        self.flow_info = scrolledtext.ScrolledText(flow_frame, height=10, width=100)
        self.flow_info.grid(row=1)

        # ---- Room Occupancy Information Section ----
        occupancy_frame = tk.Frame(right_frame)
        occupancy_frame.pack(side=tk.TOP, fill=tk.BOTH)
        tk.Label(occupancy_frame, text="Occupancy of each room", font=("Arial", 10, "underline")).grid(row=2, columnspan=4, sticky=tk.N)
        
        # Labels for different room types
        tk.Label(occupancy_frame, text="Single").grid(row=3, column=0, sticky="w")
        tk.Label(occupancy_frame, text="Double").grid(row=3, column=2, sticky="e")
        tk.Label(occupancy_frame, text="Double(Sofa)").grid(row=4, column=0, sticky="w")
        tk.Label(occupancy_frame, text="Half Lux").grid(row=4, column=2, sticky="e")
        tk.Label(occupancy_frame, text="Lux").grid(row=5, column=0, sticky="w")
        
        # Text widgets to display the occupancy status for each room type
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

        # ========= Bottom Buttons =========
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        # Button to execute the next simulation step
        self.btn_step = tk.Button(bottom_frame, text="Next step", command=self.next_stage, width=7)
        self.btn_step.pack(padx=5)
        # Button to exit the observation window (and parent window)
        self.btn_exit = tk.Button(bottom_frame, text="Exit", command=self.terminate, width=7)
        self.btn_exit.pack(padx=5)
        # Button to jump to the final state of the simulation
        self.btn_goto_end = tk.Button(bottom_frame, text="Goto End", command=self.goto_end, width=7)
        self.btn_goto_end.pack(padx=5)

        self.mode_change_text_box("disabled")

    def goto_end(self) -> None:
        """
        Advances the experiment to its end state by processing all remaining simulation steps,
        and then updates the GUI with the final results.
        """
        self.controller.goto_end()
        self.update_screen()

    def terminate(self) -> None:
        """
        Terminates the observation window and its parent window, effectively ending the experiment.
        A message box is displayed before closing.
        """
        messagebox.showinfo("Termination", "The Experiment has been terminated.")
        self.destroy()
        self.parent.destroy()

    def delete(self) -> None:
        """
        Clears all text fields in the GUI to remove old data before updating them with new simulation results.
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

    def end_experiment(self) -> None:
        """
        Called when the experiment finishes all its simulation steps.
        Displays the final statistics via a message box and terminates the program.
        """
        # Retrieve the final statistics from the controller (currently using displayStatistics as final stats)
        final_stats = self.controller.display_statistics()
        messagebox.showinfo("Experiment Completed", f"Experiment has ended.\n\n{final_stats}")
        # Terminate both this window and the parent window
        self.terminate()

    def mode_change_text_box(self, mode):
        self.flow_info.config(state = mode)
        self.time_today.config(state = mode)
        self.time_now.config(state = mode)
        self.avg_occupancy.config(state = mode)
        self.profit.config(state = mode)
        self.success_rate.config(state = mode)
        self.occupancy_single.config(state = mode)
        self.occupancy_double.config(state = mode)
        self.occupancy_double_sofa.config(state = mode)
        self.occupancy_half_lux.config(state = mode)
        self.occupancy_lux.config(state = mode)

    def update_screen(self) -> None:
        """
        Updates the entire observation window with the latest simulation data:
          - Reservation flow information.
          - Current simulation time.
          - Statistics (average occupancy, profit, success rate).
          - Occupancy details per room type.
        """
        # Clear all existing data in the text widgets
        self.mode_change_text_box("normal")
        self.delete()

        # Retrieve current simulation time (day and hour) and statistics from the controller
        day, hour = self.controller.get_time_info()
        statistics = self.controller.display_statistics()
        
        # Update the request flow information
        self.flow_info.insert(tk.END, self.controller.display_reservation_info())
        
        # Update time-related fields
        self.time_today.insert(tk.END, day)
        self.time_now.insert(tk.END, hour)

        # Update statistics fields
        self.avg_occupancy.insert(tk.END, statistics["avg_occupancy"])
        self.profit.insert(tk.END, statistics["profit"])
        self.success_rate.insert(tk.END, statistics["success_rate"])

        # Update room occupancy information using data from the controller
        room_occupancy = self.controller.display_today_occupancy()
        self.occupancy_single.insert(tk.END, room_occupancy[RoomType.SINGLE])
        self.occupancy_double.insert(tk.END, room_occupancy[RoomType.SIMPLE_DOUBLE])
        self.occupancy_double_sofa.insert(tk.END, room_occupancy[RoomType.DOUBLE_WITH_SOFA])
        self.occupancy_half_lux.insert(tk.END, room_occupancy[RoomType.HALF_LUX])
        self.occupancy_lux.insert(tk.END, room_occupancy[RoomType.LUX])

        self.mode_change_text_box("disabled")

    def next_stage(self) -> None:
        """
        Executes the next step in the simulation:
          - Clears the current display.
          - Runs one simulation step via the controller.
          - If the experiment has ended, displays final statistics and terminates.
          - Otherwise, updates the GUI with new data.
        """
        # Clear previous data from the screen
        self.delete()
        
        # Run one simulation step; step() returns False if the simulation has ended.
        is_running = self.controller.step()

        # If the simulation has ended, finish the experiment
        if not is_running:
            self.end_experiment()
            return

        # Otherwise, update the screen with the latest simulation data
        self.update_screen()
