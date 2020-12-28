import tkinter as tk
from alarm_controller import Medicine, Alarm, datetime, timedelta
from datetime import time, date

class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.master = master
        self.information = []
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.make_static_parts()
    
    def make_static_parts(self):
        title = tk.Label(self, text='Alarm Controller')
        title.pack(side='top')
        self.content = tk.Frame(self, border=2, relief='ridge', padx=5, pady=5)
        self.content.pack(side='top')
        self.create_content()
        self.medicine_count = tk.IntVar(value=0)
        self.medicine_register = tk.Label(self, textvariable=self.medicine_count)
        self.medicine_register.pack(side='top')
        button = tk.Button(self, text="Generate Alarm", command=self.generate_alarm)
        button.pack(side='bottom')


    def create_content(self):
        # Name
        title = tk.Label(self.content, text='Medicine Name:')
        title.grid(row=1, column=0)
        self.med_input_ = tk.Entry(self.content)
        self.med_input_.grid(row=1, column=1)

        # Frecuency
        title = tk.Label(self.content, text='Frequency (hh:mm):')
        title.grid(row=2, column=0)
        self.frec_input_ = tk.Frame(self.content)
        self.frec_input_.grid(row=2, column=1)
        # Hour and time for frec
        self.hourstr_frec = tk.StringVar(value='10')
        self.hour_frec_input_ = tk.Spinbox(self.frec_input_, from_=0,to=23,wrap=True,
                                textvariable=self.hourstr_frec,width=2,state="readonly")
        self.minstr_frec = tk.StringVar(value='30')
        self.minstr_frec.trace(mode='w', callback=self.trace_var_frec)
        self.last_value_frec = ''
        self.min_frec_input_ = tk.Spinbox(self.frec_input_, from_=0,to=59,wrap=True,
                                textvariable=self.minstr_frec,width=2,state="readonly")
        self.hour_frec_input_.grid(row=0, column=0)
        self.min_frec_input_.grid(row=0, column=1)
        format_label = tk.Label(self.frec_input_, text=' - 24h format')
        format_label.grid(row=0, column=2)

        # Hour and time for dosis time
        title = tk.Label(self.content, text='Next Dosis Time (hh:mm):')
        title.grid(row=3, column=0)
        self.time_input_ = tk.Frame(self.content)
        self.time_input_.grid(row=3, column=1)
        # Time and hour for next dosis time
        self.hourstr_time = tk.StringVar(value='10')
        self.hour_time_input_ = tk.Spinbox(self.time_input_, from_=0,to=23,wrap=True,
                                textvariable=self.hourstr_time,width=2,state="readonly")
        self.minstr_time = tk.StringVar(value='30')
        self.minstr_time.trace(mode='w', callback=self.trace_var_time)
        self.last_value_time = ''
        self.min_time_input_ = tk.Spinbox(self.time_input_, from_=0,to=59,wrap=True,
                                textvariable=self.minstr_time,width=2,state="readonly")
        self.hour_time_input_.grid(row=0, column=0)
        self.min_time_input_.grid(row=0, column=1)
        format_label = tk.Label(self.time_input_, text=' - 24h format')
        format_label.grid(row=0, column=2)

        # Quantity
        title = tk.Label(self.content, text='Existing Quantity:')
        title.grid(row=4, column=0)
        self.quantity_input_ = tk.Entry(self.content)
        self.quantity_input_.grid(row=4, column=1)

        # Medicine Type
        title = tk.Label(self.content, text='Medicine Type:')
        title.grid(row=5, column=0)
        options = ['pill', 'syrup'] # TRY TO MODIFY THIS FROM OUTSIDE
        self.type_selected = tk.StringVar()
        self.type_selected.set(options[0])
        self.type_input_ = tk.OptionMenu(self.content, self.type_selected, *options)
        self.type_input_.grid(row=5, column=1)

        # Dosis information
        title = tk.Label(self.content, text='Dosis Information:')
        title.grid(row=6, column=0)
        self.dosis_input_ = tk.Entry(self.content)
        self.dosis_input_.grid(row=6, column=1)

        # Buttons
        button = tk.Button(self.content, text="Add Information", command=self.add_information)
        button.grid(row=7, column=0)
        button = tk.Button(self.content, text="Reset Values", command=self.reset_values)
        button.grid(row=7, column=1)


    def trace_var_frec(self, *args):
        if self.last_value_frec == 59 and self.minstr_frec == '0':
            self.hourstr_frec.set(int(self.hourstr_frec.get())+1
                                 if self.hourstr_frec.get() !="23" else 0)
        self.last_value_frec = self.minstr_frec.get()
    
    def trace_var_time(self, *args):
        if self.last_value_time == 59 and self.minstr_time == '0':
            self.hourstr_time.set(int(self.hourstr_time.get())+1
                                 if self.hourstr_time.get() !="23" else 0)
        self.last_value_time = self.minstr_time.get()

    def add_information(self):
        med = self.create_medicine()
        self.information.append(med)

    def create_medicine(self):
        try:
            name = self.med_input_.get()
            frec = timedelta(hours=int(self.hourstr_frec.get()), minutes=int(self.minstr_frec.get()))
            next_alarm = datetime.combine(date.today(), 
                        time(hour=int(self.hourstr_time.get()), minute=int(self.minstr_time.get())))
            quantity = int(self.quantity_input_.get())
            type_ = self.type_selected.get()
            dosis = self.dosis_input_.get()
            self.medicine_count.set(self.medicine_count.get()+1)
            return Medicine(name=name, freq=frec, quantity=quantity, dosis=dosis,
                             med_type=type_, next_dosis=next_alarm)
        except Exception as e:
            print('[ERROR READING INFORMATION FROM INPUTS]:', e)


    def reset_values(self):
        self.medicine_count.set(value=0)
        del self.information[:]
        # =========== Change this to reset visually the values ================
        # self.med_input_.set = ''
        # self.frec_input_.set = ''
        # self.time_input_.set = ''
        # self.quantity_input_.set = ''
        # self.type_selected.set = ''
        # self.dosis_input_.set = ''

    def generate_alarm(self):
        if len(self.information) > 0 and self.medicine_count.get()>0:
            self.alarm = Alarm(*self.information)
            self.master.destroy()
        else:
            raise NotImplementedError("You dont give the medicines.")

if __name__ == "__main__":
    master = tk.Tk()
    app = MainWindow(master)
    app.mainloop()
    if hasattr(app, 'alarm'):
        app.alarm.run_system()