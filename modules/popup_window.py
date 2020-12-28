import tkinter as tk
from typing import Dict
from medicine_model import Medicine

class PopUp(tk.Frame):
    def __init__(self, master:tk.Tk, info:Dict[str, str], title:str='Alarm') -> None:
        super().__init__(master=master)
        self.information = info
        self.master = master
        self.popTitle = title
        self.pack()
        self.create_widgets()
        
    def create_widgets(self):
        # title
        self.titleLabel = tk.Label(justify='center', text=self.popTitle, padx=10, pady=10)
        self.titleLabel.pack(side='top')
        # Medicine Information
        self.create_window_content()
        # Close PopUp Button
        self.close_btn = tk.Button(text="Close", command=self.close_all, pady=10)
        self.close_btn.pack(side='bottom')

    def create_window_content(self):
        # Main Frame
        self.content = tk.Frame(border=2, relief='ridge', padx=5, pady=5)
        self.content.pack(fill='both', side='top')
        self.row_av:int = 0
        # Content inside frame
        for key, val in self.information.items():
            self.add_content(key=key, value=val)

    def add_content(self, key:str, value:str) -> None:
        self.variableValue = tk.StringVar(value=value)
        self.name_label = tk.Label(self.content, text=key+':')
        self.name_label.grid(row=self.row_av, column=0)
        self.name_label = tk.Label(self.content,  textvariable=self.variableValue)
        self.name_label.grid(row=self.row_av, column=1)
        self.row_av += 1

    def close_all(self, event=None):
        self.master.destroy()


if __name__ == "__main__":
    from datetime import timedelta
    Medicine.declarations = globals()

    ibuprofeno = Medicine(name='Ibuprofeno', freq=timedelta(hours=8))
    master = tk.Tk()
    dispAlarm = PopUp(master, {'base': '1', 'Activo':'2'})
    dispAlarm.mainloop()