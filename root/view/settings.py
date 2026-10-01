from tkinter import Toplevel, Label, Entry, Scrollbar, Frame, Button, Checkbutton, Tk, LabelFrame
from tkinter.ttk import Treeview
from idlelib.tooltip import Hovertip

class Settings(Toplevel):
    '''
    Settings
    --------

    Settings window
    '''
    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.master = master
        self.title('Settings')
        self.minsize(600, 420)

        row_num = 0

        Label(self, text='Sleep Interval', justify='right').grid(column=0, row=row_num, sticky='nesw', padx=5, pady=5)
        self.entry_sleep_interval = Entry(self, width=20, justify='center')
        self.entry_sleep_interval.grid(column=1, row=row_num, sticky='nesw', padx=5, pady=5)

        Label(self, text='Sleep Time', justify='right').grid(column=2, row=row_num, sticky='nesw', padx=5, pady=5)
        self.entry_sleep_time = Entry(self, width=20, justify='center')
        self.entry_sleep_time.grid(column=3, row=row_num, sticky='nesw', padx=5, pady=5)
        
        row_num += 1
        Label(self, text='Start Delay', justify='right').grid(column=0, row=row_num, sticky='nesw', padx=5, pady=5)
        self.entry_start_delay = Entry(self, width=20, justify='center')
        self.entry_start_delay.grid(column=1, row=row_num, sticky='nesw', padx=5, pady=5)

        Label(self, text='Start Minimized', justify='right').grid(column=2, row=row_num, sticky='nesw', padx=5, pady=5)
        self.check_start_min = Checkbutton(self, justify='center')
        self.check_start_min.grid(column=3, row=row_num, sticky='nesw', padx=5, pady=5)

        row_num += 1
        Label(self, text='Pause Time', justify='right').grid(column=0, row=row_num, sticky='nesw', padx=5, pady=5)
        self.entry_pause_time = Entry(self, width=20, justify='center')
        self.entry_pause_time.grid(column=1, row=row_num, sticky='nesw', padx=5, pady=5)

        row_num += 1

        operation_time_frame = LabelFrame(self, text='Opetarion Time')
        operation_time_frame.grid(column=0, row=row_num, columnspan=4, rowspan=1, sticky='nesw', padx=3, pady=3)
        operation_time_frame.grid_rowconfigure(0, weight=1, minsize=40)
        operation_time_frame.grid_columnconfigure((1, 3), weight=1)

        Label(operation_time_frame, text='From', justify='right').grid(column=0, row=0, sticky='nesw', padx=5, pady=5)
        self.entry_operation_start_time = Entry(operation_time_frame, width=8, justify='center')
        self.entry_operation_start_time.grid(column=1, row=0, sticky='nesw', padx=5, pady=5)

        Label(operation_time_frame, text='Until', justify='right').grid(column=2, row=0, sticky='nesw', padx=5, pady=5)
        self.entry_operation_end_time = Entry(operation_time_frame, width=8, justify='center')
        self.entry_operation_end_time.grid(column=3, row=0, sticky='nesw', padx=5, pady=5)

        row_num += 1

        treeview_frame = LabelFrame(self, text='Process List')
        treeview_frame.grid(column=0, row=row_num, columnspan=4, rowspan=2, sticky='nesw', padx=3, pady=3)
        row_num += 1
        treeview_frame.grid_columnconfigure([1, 2, 3], weight=1)

        self.columns = ('process', 'process_path', 'cmd_line_detail')
        columns_description = ('Process', 'Process Path', 'CMD Line Detail')
        columns_width = (50, 200, 100)
        anchor_value = ('center', 'w', 'w')
        scrollbar = Scrollbar(treeview_frame, orient='vertical', background='white')
        self.treeview = Treeview(treeview_frame, columns=self.columns, height=5, show='headings', yscrollcommand=scrollbar.set)
        self.treeview.grid(column=1, row=0, columnspan=3, sticky='nesw', padx=(5, 0), pady=(0, 5))
        Hovertip(self.treeview, 'Process List.')
        scrollbar.grid(column=4, row=0, sticky='nesw', padx=(0, 3), pady=(0, 5))
        scrollbar.config(command=self.treeview.yview)
        self.treeview.tag_configure('evenrow', background='white')
        self.treeview.tag_configure('oddrow', background='#E0E0E0')

        self.button_add = Button(treeview_frame, text='Add')
        self.button_add.grid(column=1, row=1, sticky='nesw', padx=(5, 0), pady=(0, 5))
        Hovertip(self.button_add, 'Add new process')
        self.button_edit = Button(treeview_frame, text='Edit')
        self.button_edit.grid(column=2, row=1, sticky='nesw', padx=0, pady=(0, 5))
        Hovertip(self.button_add, 'Edit selected process')
        self.button_remove = Button(treeview_frame, text='Remove', width=5)
        self.button_remove.grid(column=3, row=1, columnspan=2, sticky='nesw', padx=(0, 5), pady=(0, 5))
        Hovertip(self.button_remove, 'Remove selected process')

        for i, column in enumerate(self.columns):
            self.treeview.heading(column, text=columns_description[i])
            self.treeview.column(column, width=columns_width[i], anchor=anchor_value[i])                         

        row_num += 1
        button_frame = Frame(self)
        button_frame.grid(column=0, row=row_num, columnspan=5, sticky='nesw')
        button_frame.grid_rowconfigure(0, minsize=40)
        button_frame.grid_columnconfigure(0, weight=1)

        for i in range(row_num + 1):
            self.grid_rowconfigure(i, weight=1, minsize=40)
        self.grid_columnconfigure([1, 3], weight=1)

        self.button_cancel = Button(button_frame, text='Cancel', width=15)
        self.button_ok = Button(button_frame, text='Ok', width=15)
        self.button_cancel.grid(column=1, row=0, sticky='nesw', padx=(5, 0), pady=5)
        self.button_ok.grid(column=2, row=0, sticky='nesw', padx=5, pady=5)


if __name__ == '__main__':
    root = Tk()
    main_frame = Frame(root)
    main_frame.grid(column=0, row=0, sticky='nesw')
    settings = Settings(main_frame)
    root.mainloop()
