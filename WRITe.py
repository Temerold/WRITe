import tkinter
import threading


ENTRIES = {}  # Entry box dictionary, containing all the entry boxes
ROWS = 5
COLUMNS = 3


class SimpleTableInput(threading.Thread, tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)

        # Validation command; command to validate entry box input (only
        # numbers are allowed)
        global validationCommand
        validationCommand = (self.register(self.validate), "%P")

        # Create integer-only entry boxes
        for row in range(ROWS):
            for column in range(COLUMNS):
                self.addEntry(row, column, validationCommand)

        # Create column headers
        headers = ["Date", "Word Count", "Word Increase"]
        for column in range(COLUMNS):
            index = (0, column)
            entry = ENTRIES[index]
            header = tkinter.StringVar(parent, value=headers[column])
            entry.config(textvariable=header)
            entry.config(state="readonly")

    def addEntry(
        self,
        row: int,
        column: int,
        # Default validation command: True if int.
        validationCommand=(lambda x: True if x is int else False),
    ):
        entryBox = tkinter.Entry(
            self, validate="key", validatecommand=validationCommand
        )
        entryBox.grid(row=row, column=column, stick="nsew")

        index = (row, column)
        ENTRIES[index] = entryBox

    def validate(self, P):
        """
        Perform input validation.

        Allow only an empty value, or a value that can be converted to
        an int.
        """

        try:
            int(P)
        except ValueError:
            return False
        return True


class App(tkinter.Frame):
    def __init__(self, parent):
        super().__init__()
        tkinter.Frame.__init__(self, parent)
        self.table = SimpleTableInput(self)
        self.table.grid(row=1, column=1, sticky="nsew")


root = tkinter.Tk()
root.title("WRITe")
root.resizable(width=False, height=False)
App(root).pack(side="top", fill="both", expand=True)


root.mainloop()
