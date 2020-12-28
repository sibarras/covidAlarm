from datetime import datetime, timedelta
from typing import Dict, List, Literal, Union


class Medicine:
    declarations:Dict[str, object] = globals()
    medicine_objects:List[object] = []

    def __init__(self,  name:str, 
                        freq:timedelta,
                        quantity:int=1, 
                        med_type:Union[Literal['pill'], Literal['syrup']]='pill',
                        dosis:str='1 each time',
                        next_dosis:datetime=datetime.now().replace(microsecond=0)) -> None:

        self.name = name
        self.freq = freq
        self.quantity = quantity
        self.med_type = med_type
        self.dosis = dosis
        self.next_dosis = next_dosis

        assert self.quantity > 0
        valid_types:List[str] = ['pill', 'syrup']
        if self.med_type not in valid_types:
            raise Exception("[ERROR]: Medicine Type is not valid.")

        self.with_dosis:bool = True
        self.last_dosis:datetime = self.next_dosis - self.freq
        self.__class__.medicine_objects.append(self)

    def change_next_dosis_date(self) -> None:
        self.last_dosis = datetime.now().replace(microsecond=0)
        self.last_dosis, self.next_dosis = self.next_dosis, self.next_dosis + self.freq

        if self.med_type == 'pill':
            self.quantity -= 1

        if self.quantity == 0:
            print("Se te acabo la medicina. Pide rapido antes de {}".format(self.next_dosis))
        elif self.quantity == -1:
            self.quantity = 0
            self.with_dosis = False
            print("Necesitas tomar ya y no tienes nada que tomar.")
    
    def __repr__(self) -> str:
        return "(Name:{}, Type:{}, Quantity:{}, Frequency:{})"\
                .format(self.name, self.med_type, self.quantity, self.freq)


if __name__ == "__main__":
    ibuprofeno = Medicine(name='Ibuprofeno', freq=timedelta(hours=8), quantity=6)
    inmuneComplex = Medicine(name='Inmune Complex', freq=timedelta(days=1), quantity=12)
    
