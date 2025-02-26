import tkinter as tk
from tkinter import messagebox
from Experiment import Experiment
from RoomType import RoomType

# (1) 실험 초기화 창: days, step 입력
class InitWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("실험 초기화")
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
        
        self.start_button = tk.Button(self, text="실험 시작", command=self.start_experiment)
        self.start_button.grid(row=5, column=2, columnspan=2, pady=10)
        
    def start_experiment(self):
        rooms = {RoomType.SINGLE : self.single.get(), 
                 RoomType.SIMPLE_DOUBLE : self.double.get(), 
                 RoomType.DOUBLE_WITH_SOFA : self.double_sofa.get(), 
                 RoomType.HALF_LUX : self.half_lux.get(), 
                 RoomType.LUX : self.lux.get()}
        
        days = self.entry_days.get()
        step = self.entry_step.get()
        
        if not days.isdigit() or not step.isdigit():
            messagebox.showerror("오류", "정수 값을 입력해 주세요.")
            return

        for key,value in rooms.items():
            if not value.isdigit():
                messagebox.showerror("오류", "정수 값을 입력해 주세요.")
                return
            else:
                rooms[key] = int(value)

        days = int(days)
        step = int(step)
        self.withdraw()  # 초기화 창 숨김
        obs_win = ObservationWindow(self, days, step, rooms)
        obs_win.mainloop()

# (2) 실험 관찰 창: 실험 상태 및 통계 표시, 실험 종료 및 다음 단계 버튼 제공
class ObservationWindow(tk.Toplevel):
    def __init__(self, parent, days, step, rooms):
        super().__init__(parent)
        self.parent = parent
        self.days = days
        self.step = step
        self.title("실험 관찰")
        self.geometry("724x500")

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
            self.time_today.grid(row = 1, column = 1, pady = 2)

            self.time_now = tk.Text(left_frame, height=1, width=5)
            self.time_now.grid(row = 2, column = 1, pady = 2)

            # ---- Statistics ----
            tk.Label(left_frame, text="Statistics", font=("Arial", 10, "underline")).grid(row = 3, pady=5)

            tk.Label(left_frame, text="Средний загруз:").grid(row=4, column=0, pady = 2)
            tk.Label(left_frame, text="Доход:").grid(row=5, column=0, pady = 2)
            tk.Label(left_frame, text="Процент успешных заявок:").grid(row=6, column=0, pady = 2)

            self.avg_occupancy = tk.Text(left_frame, height=1, width=5)
            self.avg_occupancy.grid(row=4, column=1, pady = 2)

            self.profit = tk.Text(left_frame, height=1, width=5)
            self.profit.grid(row=5, column=1, pady = 2)
            
            self.success_rate = tk.Text(left_frame, height=1, width=5)
            self.success_rate.grid(row=6, column=1, pady = 2)

            # ========== 우측 정보 영역 ==========
            right_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
            right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

            # ---- Поток заявок ----
            tk.Label(right_frame, text="Поток заявок", font=("Arial", 10, "underline")).pack(pady=5)

            self.flow_info = tk.Text(right_frame, height=10, width=40)
            self.flow_info.pack(pady=5)

            # ---- Результат обработки заявок ----
            result_label = tk.Label(right_frame, text="Результат обработки заявок", font=("Arial", 10, "underline"))
            result_label.pack(pady=5)

            self.request_result = tk.Text(right_frame, height=10, width=40)
            self.request_result.pack(pady=5)

            # ========== 하단 버튼 ==========
            bottom_frame = tk.Frame(self)
            bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

            self.btn_start = tk.Button(bottom_frame, text="Next step", command=self.next_stage)
            self.btn_start.pack(side=tk.LEFT, padx=5)

            self.btn_exit = tk.Button(bottom_frame, text="Выход", command=self.terminate_experiment)
            self.btn_exit.pack(side=tk.RIGHT, padx=5)

            self.experiment = Experiment(days, step, rooms)

        except:
            self.terminate_experiment()
    
    def terminate_experiment(self):
        messagebox.showinfo("실험 종료", "실험이 종료되었습니다.")
        self.destroy()
        self.parent.destroy()
    
    def next_stage(self):
        # 다음 단계 버튼 클릭 시 시뮬레이션 실행 후 통계 업데이트
        request, request_result, day, time = self.experiment.step()
        
        self.flow_info.delete(1.0, tk.END)
        if request:    
            self.flow_info.insert(tk.END, request.display_request_info())
        else:
            self.flow_info.insert(tk.END, "Nobody wants to stay in Our Hotel....")

        self.request_result.delete(1.0, tk.END)
        if request_result:
            self.request_result.insert(tk.END, request_result.displayRoomInfo())
        else:
            self.request_result.insert(tk.END, "Could not check in")
        self.time_today.delete(1.0, tk.END)
        self.time_today.insert(tk.END, day)

        self.time_now.delete(1.0, tk.END)
        self.time_now.insert(tk.END, time)

        statistics = self.experiment.getStatistics()

        self.avg_occupancy.delete(1.0, tk.END)
        self.profit.delete(1.0, tk.END)
        self.success_rate.delete(1.0, tk.END)

        self.avg_occupancy.insert(tk.END, statistics["avg_occupancy"])
        self.profit.insert(tk.END, statistics["profit"])
        self.success_rate.insert(tk.END, statistics["success_rate"])