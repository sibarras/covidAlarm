from datetime import date, datetime, time, timedelta
from time import sleep
from typing import Dict, Tuple
from medicine_model import Medicine
from popup_window import PopUp, tk

class Alarm:
    def __init__(self, *args:Medicine) -> None:
        if type(args[0]) == Tuple[Medicine, ...]:
            self.medicines:Tuple[Medicine, ...] = args[0]
        else:
            self.medicines:Tuple[Medicine, ...] = args

        self.next_medicine:Medicine
        self.medicine_dict:Dict[str, Medicine] = {}
        self.info_created:bool = False
        self.win:PopUp
        self.set_alarm_time()

    def set_alarm_time(self) -> None:
        self.medicine_dict.clear()
        for medicine in self.medicines:
            self.medicine_dict[medicine.name] = medicine
        self.medicine_dict = dict(sorted(self.medicine_dict.items(), key=lambda med:med[1].next_dosis))
        self.next_medicine = list(self.medicine_dict.values())[0]

    @property
    def time_remaining(self) -> timedelta:
        time_remaining:timedelta = (self.next_medicine.next_dosis - datetime.now() if self.next_medicine.next_dosis > datetime.now() else timedelta(seconds=0))
        return time_remaining

    def is_time(self) -> bool:
        now = datetime.now().replace(microsecond=0)
        if now.date() >= self.next_medicine.next_dosis.date() and now.time().replace(second=0) >= self.next_medicine.next_dosis.time().replace(second=0):
            return True
        return False

    def run_system(self) -> None:
        while True:
            info = {
                'Next Medicine': self.next_medicine.name,
                'Alarm': self.next_medicine.next_dosis.time().strftime('%I:%M %p'),
                'Time Remaining': (datetime.min + self.time_remaining).time().strftime('%H:%M')
            }
            master = tk.Tk()
            infowin = PopUp(master, info=info, title="Waiting...")
            infowin.update()
            print('Waiting...')
            while not self.is_time():
                try:
                    infowin.update()
                    sleep(1)
                    infowin.variableValue.set((datetime.min + self.time_remaining).time().strftime('%H:%M:%S'))
                except Exception:
                    print('The Program was closed.')
                    exit()
            print('Closing...')
            infowin.close_all()

            print('alarm On...')
            if self.is_time():
                print('Alarm!')
                self.run_alarm()

    def run_alarm(self) -> None:
        current_info = self.get_info(self.next_medicine)
        self.view(current_info, title='ALARM!!')
        self.next_medicine.change_next_dosis_date()
        self.set_alarm_time()
        next_info = self.get_info(self.next_medicine)
        self.view(next_info, title='Next Medicine')

    @staticmethod
    def get_info(medicine:Medicine) -> Dict[str,str]:
        info:Dict[str, str] = {}
        info['Medicine'] = medicine.name
        info['Alarm Time'] = medicine.next_dosis.time().strftime('%I:%M %p')
        info['Quantity'] = str(medicine.quantity)
        info['Frequency'] = str(medicine.freq.seconds//3600) + ' hours'
        info['dosis'] = medicine.dosis
        return info

    @staticmethod
    def view(info:Dict[str,str], title:str='Alarm', after=None) -> PopUp:
        master = tk.Tk()
        win = PopUp(master, info=info, title=title)
        if after is not None:
            win.after(0, after)
            return win
        win.mainloop()
        return win
    
    def __repr__(self) -> str:
        return "(Medicines:{}, \nNext Medicine:{}, \nNext Alarm:{})"\
                .format(self.medicine_dict.keys(), self.next_medicine.name, self.next_medicine.next_dosis.time())


if __name__ == "__main__":
    from datetime import timedelta
    Medicine.declarations = globals()
    ibuprofeno = Medicine(name='Ibuprofeno', freq=timedelta(hours=8), quantity=15, med_type='pill', dosis="Tomar 1", next_dosis=datetime.combine(date.today(), time(hour=7)))
    inmuneComplex = Medicine(name='Inmune Complex', freq=timedelta(days=1), quantity=12, med_type='pill', dosis="Tomar 1", next_dosis=datetime.combine(date.today(), time(hour=11, minute=30)))
    hidroxicloroquina = Medicine(name='Hidroxicloroquina', freq=timedelta(days=1), quantity=6, med_type='pill', dosis="Tomar 1", next_dosis=datetime.combine(date.today(), time(hour=15)))
    antiflu = Medicine(name='Anti-Flu', freq=timedelta(hours=8), quantity=6, med_type='pill', dosis="Tomar 1", next_dosis=datetime.combine(date.today(), time(hour=10, minute=30)))
    ambroxol = Medicine(name='Ambroxol', freq=timedelta(hours=8), med_type='syrup', dosis="10 ml", next_dosis=datetime.combine(date.today(), time(hour=9, minute=30)))
    bottleMix = Medicine(name='Ada\'s Mix', freq=timedelta(hours=6), med_type='syrup', dosis="4 taps",  next_dosis=datetime.combine(date.today(), time(hour=9, minute=30)))
    samuel_medicines = Alarm(ibuprofeno,inmuneComplex,hidroxicloroquina, antiflu, ambroxol, bottleMix)
    samuel_medicines.run_system()