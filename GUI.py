import tkinter as tk
from tkinter import messagebox
from Experiment import Experiment
from RoomType import RoomType
from abc import abstractmethod

class GUI(tk.Tk):
    @abstractmethod
    def terminate(self):
        pass

# (1) 실험 초기화 창: days, step 입력
class InitWindow(GUI):
    def __init__(self):
        super().__init__()
        self.title("Initialize Experiment")
        self.geometry("430x250")
        
        tk.Label(self, text="Days for experiments:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_days = tk.Entry(self)
        self.entry_days.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Steps for each day:").grid(row=1, column=0, padx=10, pady=10, sticky="w")    
        self.entry_step = tk.Entry(self)
        self.entry_step.grid(row=1, column=1, padx=10, pady=10)

        # 방 갯수 입력 부분
        tk.Label(self, text = "Room numbers").grid(row = 2, padx=10, pady=10, sticky="e")
        tk.Label(self, text = "Single").grid(row = 3, column = 0, sticky="w", padx = 1)
        tk.Label(self, text = "Double").grid(row = 3, column = 2, sticky="w")
        tk.Label(self, text = "Double(Sofa)").grid(row = 4, column = 0, sticky="w")
        tk.Label(self, text = "Half Lux").grid(row = 4, column = 2, sticky="w")
        tk.Label(self, text = "Lux").grid(row = 5, column = 0, sticky="w")

        self.single = tk.Entry(self, width=5)
        self.double = tk.Entry(self, width=5)
        self.double_sofa = tk.Entry(self, width=5)
        self.half_lux = tk.Entry(self, width=5)
        self.lux = tk.Entry(self, width=5)

        self.single.grid(row = 3, column = 1, sticky="w")
        self.double.grid(row = 3, column = 3, sticky="w")
        self.double_sofa.grid(row=4,column=1, sticky="w")
        self.half_lux.grid(row = 4, column=3, sticky="w")
        self.lux.grid(row = 5, column = 1, sticky="w")
        
        self.start_button = tk.Button(self, text="Start", command=self.start_experiment)
        self.start_button.grid(row=5, column=2, columnspan=2, pady=10, sticky="w")

        self.exit_button = tk.Button(self, text = "Exit", command = self.terminate)
        self.exit_button.grid(row = 5, column=3, columnspan=2, pady=10)
        
    def start_experiment(self):
        rooms = {RoomType.SINGLE : self.single.get(), 
                 RoomType.SIMPLE_DOUBLE : self.double.get(), 
                 RoomType.DOUBLE_WITH_SOFA : self.double_sofa.get(), 
                 RoomType.HALF_LUX : self.half_lux.get(), 
                 RoomType.LUX : self.lux.get()}
        
        days = self.entry_days.get()
        step = self.entry_step.get()
        
        if not days.isdigit() or not step.isdigit():
            messagebox.showerror("Error", "Required INTEGER value.")
            return

        for key,value in rooms.items():
            if not value.isdigit():
                messagebox.showerror("Error", "Required INTEGER value.")
                return
            else:
                rooms[key] = int(value)

        days = int(days)
        step = int(step)
        self.withdraw()  # 초기화 창 숨김
        obs_win = ObservationWindow(self, days, step, rooms)
        obs_win.mainloop()
    
    def terminate(self):
        self.destroy()

# (2) 실험 관찰 창: 실험 상태 및 통계 표시, 실험 종료 및 다음 단계 버튼 제공
class ObservationWindow(tk.Toplevel, GUI):
    def __init__(self, parent, days, step, rooms):
        super().__init__(parent)
        self.parent = parent
        self.days = days
        self.step = step
        self.title("Experiment Observation")
        self.geometry("1200x400")

        try:
            # ========== 상단 레이블(총 기간/단계 표시) ==========
            top_frame = tk.Frame(self)
            top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

            self.lbl_experiment_info = tk.Label(
                top_frame,
                text=f"Total day = {days} days, hour per step = {step} hour",
                font=("Arial", 11, "bold")
            )
            self.lbl_experiment_info.pack(side=tk.LEFT)

            # ========== 좌측 정보 영역 ==========
            left_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
            left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

            # ---- Time Info ----
            tk.Label(left_frame, text="Time Info", font=("Arial", 10, "underline")).grid(row = 0, column = 0, pady=5)
            tk.Label(left_frame, text=f"Today:").grid(row = 1, column = 0, pady=2)
            tk.Label(left_frame, text=f"Now:").grid(row = 2, column = 0, pady=2)

            self.time_today = tk.Text(left_frame, height=1, width=5)
            self.time_now = tk.Text(left_frame, height=1, width=5)

            self.time_today.grid(row = 1, column = 1, pady = 2)
            self.time_now.grid(row = 2, column = 1, pady = 2)

            # ---- Statistics ----
            tk.Label(left_frame, text="Statistics", font=("Arial", 10, "underline")).grid(row = 3, pady=5)

            tk.Label(left_frame, text="Mean occupancy today:").grid(row=4, column=0, pady = 2)
            tk.Label(left_frame, text="Profit:").grid(row=5, column=0, pady = 2)
            tk.Label(left_frame, text="Successful request percentage:").grid(row=6, column=0, pady = 2)

            self.avg_occupancy = tk.Text(left_frame, height=1, width=5)
            self.profit = tk.Text(left_frame, height=1, width=5)
            self.success_rate = tk.Text(left_frame, height=1, width=5)

            self.avg_occupancy.grid(row=4, column=1, pady = 2)
            self.profit.grid(row=5, column=1, pady = 2)
            self.success_rate.grid(row=6, column=1, pady = 2)

            # ========== 우측 정보 영역 ==========
            right_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
            right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

            # ---- Request Flow ----
            flow_frame = tk.Frame(right_frame)
            flow_frame.pack(side = tk.TOP, fill = tk.BOTH)

            tk.Label(flow_frame, text="Request Flow", font=("Arial", 10, "underline")).grid(row = 0, pady=5)

            self.flow_info = tk.Text(flow_frame, height=10, width=100)
            self.flow_info.grid(row=1)

            # ---- Occupancy information of each room ----
            occupancy_frame = tk.Frame(right_frame)
            occupancy_frame.pack(side = tk.TOP, fill = tk.BOTH)

            tk.Label(occupancy_frame, text= "Occupancy of each room", font=("Arial", 10, "underline")).grid(row=2,columnspan=4, sticky=tk.N)

            tk.Label(occupancy_frame, text = "Single").grid(row = 3, column=0,sticky="w")
            tk.Label(occupancy_frame, text = "Double").grid(row = 3, column=2,sticky="e")
            tk.Label(occupancy_frame, text = "Double(Sofa)").grid(row = 4, column=0,sticky="w")
            tk.Label(occupancy_frame, text = "Half Lux").grid(row = 4, column=2,sticky="e")
            tk.Label(occupancy_frame, text = "Lux").grid(row=5, column=0,sticky="w")

            self.occupancy_single = tk.Text(occupancy_frame, height=1, width=5)
            self.occupancy_double = tk.Text(occupancy_frame, height=1, width=5)
            self.occupancy_double_sofa = tk.Text(occupancy_frame, height=1, width=5)
            self.occupancy_half_lux = tk.Text(occupancy_frame, height=1, width=5)
            self.occupancy_lux = tk.Text(occupancy_frame, height=1, width=5)

            self.occupancy_single.grid(row=3, column=1, pady = 2,sticky="w")           
            self.occupancy_double.grid(row=3, column=3, pady = 2,sticky="e")
            self.occupancy_double_sofa.grid(row=4, column=1, pady = 2,sticky="w")
            self.occupancy_half_lux.grid(row=4, column=3, pady = 2,sticky="e") 
            self.occupancy_lux.grid(row=5, column=1, pady = 2,sticky="w")

            # ========== 하단 버튼 ==========
            bottom_frame = tk.Frame(self)
            bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

            self.btn_step = tk.Button(bottom_frame, text="Next step", command=self.next_stage)
            self.btn_step.pack(side=tk.LEFT, padx=5)

            self.btn_exit = tk.Button(bottom_frame, text="Exit", command=self.terminate)
            self.btn_exit.pack(side=tk.RIGHT, padx=5)

            self.experiment = Experiment(days, step, rooms)

        except:
            self.terminate()
    
    def terminate(self):
        messagebox.showinfo("Termination", "The Experiment has been terminated.")
        self.destroy()
        self.parent.destroy()

    def delete(self):
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

    def endExperiment(self):
        messagebox.showinfo("End of Experiment","The experiment ended")
        self.destroy()
        self.parent.destroy()

    def next_stage(self):
        # 다음 단계 버튼 클릭 시 시뮬레이션 실행 후 통계 업데이트
        # request, request_result, day, time = self.experiment.step()
        self.delete()
        is_running = self.experiment.step()

        if not is_running:
            self.endExperiment()

        day, hour = self.experiment.getTimeInfo()
        statistics = self.experiment.displayStatistics()
        
        self.flow_info.insert(tk.END, self.experiment.displayReservationInfo())
        self.time_today.insert(tk.END, day)
        self.time_now.insert(tk.END, hour)

        self.avg_occupancy.insert(tk.END, statistics["avg_occupancy"])
        self.profit.insert(tk.END, statistics["profit"])
        self.success_rate.insert(tk.END, statistics["success_rate"])

        room_occupancy = self.experiment.displayTodayOccupancy()

        self.occupancy_single.insert(tk.END, room_occupancy[RoomType.SINGLE])
        self.occupancy_double.insert(tk.END, room_occupancy[RoomType.SIMPLE_DOUBLE])
        self.occupancy_double_sofa.insert(tk.END, room_occupancy[RoomType.DOUBLE_WITH_SOFA])
        self.occupancy_half_lux.insert(tk.END, room_occupancy[RoomType.HALF_LUX])
        self.occupancy_lux.insert(tk.END, room_occupancy[RoomType.LUX])