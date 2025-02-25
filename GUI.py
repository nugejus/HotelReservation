import tkinter as tk
from tkinter import messagebox
from Experiment import Experiment

# (1) 실험 초기화 창: days, step 입력
class InitWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("실험 초기화")
        self.geometry("350x150")
        
        tk.Label(self, text="일수 (days):").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_days = tk.Entry(self)
        self.entry_days.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(self, text="시간 단위 (step):").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_step = tk.Entry(self)
        self.entry_step.grid(row=1, column=1, padx=10, pady=10)
        
        self.start_button = tk.Button(self, text="실험 시작", command=self.start_experiment)
        self.start_button.grid(row=2, column=0, columnspan=2, pady=10)
        
    def start_experiment(self):
        days = self.entry_days.get()
        step = self.entry_step.get()
        if not days.isdigit() or not step.isdigit():
            messagebox.showerror("오류", "정수 값을 입력해 주세요.")
            return
        days = int(days)
        step = int(step)
        self.withdraw()  # 초기화 창 숨김
        obs_win = ObservationWindow(self, days, step)
        obs_win.mainloop()

# (2) 실험 관찰 창: 실험 상태 및 통계 표시, 실험 종료 및 다음 단계 버튼 제공
class ObservationWindow(tk.Toplevel):
    def __init__(self, parent, days, step):
        super().__init__(parent)
        self.parent = parent
        self.days = days
        self.step = step
        self.title("실험 관찰")
        self.geometry("400x600")

        try: 
            self.initial_lable = tk.Label(self, text=f"실험: {days}일, 단계: {step}시간", font=("Arial", 12))
            self.initial_lable.grid(row = 0, column= 0, pady = 10)

            self.day_info_lable = tk.Label(self, text = "day",font=("Arial", 10), fg="gray")
            self.day_info_lable.grid(row = 1, column= 0, sticky="w", padx=10)
            self.day_info = tk.Text(self, height=1, width=5)
            self.day_info.grid(row = 2, column= 0, padx= 5, pady= 10)
            
            self.time_info_lable = tk.Label(self, text = "time",font=("Arial", 10), fg="gray")
            self.time_info_lable.grid(row = 1, column= 1, sticky="w", padx=10)
            self.time_info = tk.Text(self, height=1, width=5)
            self.time_info.grid(row = 2, column= 1, padx= 5, pady= 10)

            
            self.stats_label = tk.Label(self, text = "Stats",font=("Arial", 10), fg="gray")
            self.stats_label.grid(row = 3, column= 0, sticky="w", padx=10)
            self.stats_text = tk.Text(self, height=5, width=40)
            self.stats_text.grid(row = 4, column= 0, pady=10)

            self.request_flow_label = tk.Label(self, text = "Request Flow",font=("Arial", 10), fg="gray")
            self.request_flow_label.grid(row = 5,sticky="w", padx=10)
            self.request_flow = tk.Text(self, height=5, width=40)
            self.request_flow.grid(row = 6, pady = 10)
            
            self.terminate_button = tk.Button(self, text="실험 종료", command=self.terminate_experiment)
            self.terminate_button.grid(row = 7, pady=5)
            
            self.next_stage_button = tk.Button(self, text="다음 단계", command=self.next_stage)
            self.next_stage_button.grid(row = 8, pady=5)
        
            # Experiment 객체 생성
            self.experiment = Experiment(days, step)
        except:
            self.terminate_experiment()
    
    def terminate_experiment(self):
        messagebox.showinfo("실험 종료", "실험이 종료되었습니다.")
        self.destroy()
        self.parent.destroy()
    
    def next_stage(self):
        # 다음 단계 버튼 클릭 시 시뮬레이션 실행 후 통계 업데이트
        request, day, time = self.experiment.step()
        self.request_flow.delete(1.0, tk.END)
        self.request_flow.insert(tk.END, request.get_request_info())

        self.day_info.delete(1.0, tk.END)
        self.day_info.insert(tk.END, day)
        self.time_info.delete(1.0, tk.END)
        self.time_info.insert(tk.END, time)

        stats = self.experiment.displayStatistics()
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats)