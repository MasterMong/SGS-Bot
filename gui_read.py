#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import clipboard
from time import sleep
import pyautogui


class GuiApp:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=200, width=300)
        self.frame_main = ttk.Frame(toplevel1, name="frame_main")
        self.btn_check = ttk.Button(self.frame_main, name="btn_check")
        self.btn_check.configure(text='Check')
        self.btn_check.grid(column=0, row=0)
        self.btn_check.configure(command=self.fn_check)
        self.label_column = ttk.Label(self.frame_main, name="label_column")
        self.label_column.configure(text='Column: 0')
        self.label_column.grid(column=1, padx=10, row=0)
        self.label_row = ttk.Label(self.frame_main, name="label_row")
        self.label_row.configure(text='Row : 0')
        self.label_row.grid(column=2, padx=10, row=0)
        label6 = ttk.Label(self.frame_main)
        label6.configure(text='Delay (s)')
        label6.grid(column=0, row=1)
        self.delay = ttk.Entry(self.frame_main, name="delay")
        _text_ = '5'
        self.delay.configure()
        self.delay.delete("0", "end")
        self.delay.insert("0", _text_)
        self.delay.grid(column=1, columnspan=2, row=1)
        self.btn_start = ttk.Button(self.frame_main, name="btn_start")
        self.btn_start.configure(text='Start')
        self.btn_start.grid(column=0, columnspan=3, pady=10, row=2)
        self.btn_start.configure(command=self.fn_calc)
        self.label_cooldown = ttk.Label(self.frame_main)
        self.label_cooldown.configure(
            font="{Ubuntu} 12 {}",
            state="normal",
            text='tile left')
        self.label_cooldown.grid(column=0, columnspan=3, pady=20, row=4)
        # frame3 = ttk.Frame(self.frame_main)
        # frame3.configure(height=20, width=200)
        # progressbar1 = ttk.Progressbar(frame3)
        # self.progress = tk.DoubleVar(value=50)
        # progressbar1.configure(
        #     maximum=100,
        #     orient="horizontal",
        #     value=50,
        #     variable=self.progress)
        # progressbar1.place(anchor="nw", relwidth=1.0, x=0, y=0)
        # frame3.grid(column=0, columnspan=3, row=6)
        self.frame_main.pack(side="top")

        # window
        # self.mainwindow.attributes('-topmost', True)
        # Main widget
        self.mainwindow = toplevel1

    def center(self, event):
        wm_min = self.mainwindow.wm_minsize()
        wm_max = self.mainwindow.wm_maxsize()
        screen_w = self.mainwindow.winfo_screenwidth()
        screen_h = self.mainwindow.winfo_screenheight()
        """ `winfo_width` / `winfo_height` at this point return `geometry` size if set. """
        x_min = min(screen_w, wm_max[0],
                    max(self.main_w, wm_min[0],
                        self.mainwindow.winfo_width(),
                        self.mainwindow.winfo_reqwidth()))
        y_min = min(screen_h, wm_max[1],
                    max(self.main_h, wm_min[1],
                        self.mainwindow.winfo_height(),
                        self.mainwindow.winfo_reqheight()))
        x = screen_w - x_min
        y = screen_h - y_min
        self.mainwindow.geometry(f"{x_min}x{y_min}+{x // 2}+{y // 2}")
        self.mainwindow.unbind("<Map>", self.center_map)

    def run(self, center=False):
        if center:
            """ If `width` and `height` are set for the main widget,
            this is the only time TK returns them. """
            self.main_w = self.mainwindow.winfo_reqwidth()
            self.main_h = self.mainwindow.winfo_reqheight()
            self.center_map = self.mainwindow.bind("<Map>", self.center)
        self.mainwindow.mainloop()

    def fn_clipboard(self, paste=False):
        data = clipboard.paste()
        lines = data.splitlines()
        line_header = lines.pop(0)
        line_columns = line_header.split('\t')

        self.label_column.config(text=f'Column: {len(line_columns)}')
        self.label_row.config(text=f'Row: {len(lines)}')

        sec = 0
        left = int(self.delay.get())

        while left > sec:
            left = left - 1
            self.label_cooldown.config(text=f'{left} seconds')
            sleep(1)

        if (paste and len(lines) > 0):
            for line in lines:
                if (line != ''):
                    cells = line.split('\t')
                    for cell in cells:
                        print(f'filling {cell}')
                        pyautogui.hotkey('ctrl', 'a')
                        pyautogui.hotkey('backspace')
                        pyautogui.write(cell)
                        pyautogui.press('tab')
                        sleep(0.01)
                    print('done')

    def fn_check(self):
        print('check')
        self.fn_clipboard()
        pass

    def fn_calc(self):
        print('calc')
        self.fn_clipboard(paste=True)
        pass


if __name__ == "__main__":
    app = GuiApp()
    app.run()
