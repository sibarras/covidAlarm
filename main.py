from pathlib import Path
from sys import path

module_relative_path = 'modules'
main_path = Path(__file__).parent
module_path = main_path.joinpath(module_relative_path)
path.append(str(module_path))

import user_interface as ui

if __name__ == "__main__":    
    master = ui.tk.Tk()
    app = ui.MainWindow(master)
    app.mainloop()
    if hasattr(app, 'alarm'):
        app.alarm.run_system()