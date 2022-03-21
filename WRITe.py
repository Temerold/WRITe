import tkinter
import threading


ENTRIES = {}  # Entry box dictionary, containing all the entry boxes
ROWS = 5
COLUMNS = 3


class SimpleTableInput(threading.Thread, tkinter.Frame):
    def __init__(self, parent):
        global ROWS
        tkinter.Frame.__init__(self, parent)

        # Load save file (data.csv)
        try:
            with open("data.csv", "r") as file:
                fileContents = file.readlines()
                rowCount = len(fileContents)
                if rowCount > 0:
                    ROWS = rowCount + 1
        except FileNotFoundError:
            fileContents = []

        # Validation command; command to validate entry box input (only
        # numbers are allowed)
        global validationCommand
        validationCommand = (self.register(self.validate), "%P")

        # Create integer-only entry boxes
        for row in range(ROWS):
            for column in range(COLUMNS):
                self.addEntry(row, column, validationCommand)

        # Re-create data from save file (data.csv)
        currentRow = 0
        for row in fileContents:
            currentRow += 1
            row = row.split(";")
            for column in range(COLUMNS):
                ENTRIES[(currentRow, column)].insert(0, row[column])

        # Create column headers
        headers = ["Date", "Word Count", "Word Increase"]
        for column in range(COLUMNS):
            index = (0, column)
            entry = ENTRIES[index]
            header = tkinter.StringVar(parent, value=headers[column])
            entry.config(textvariable=header)
            entry.config(state="readonly")

    def addEntry(self, row: int, column: int, validationCommand):
        entryBox = tkinter.Entry(
            self, validate="key", validatecommand=validationCommand
        )
        entryBox.grid(row=row, column=column, stick="nsew")

        index = (row, column)
        ENTRIES[index] = entryBox

    def addRow(self):
        global ROWS

        for column in range(COLUMNS):
            self.addEntry(ROWS, column, validationCommand)

        ROWS += 1

    def deleteRow(self):
        global ROWS

        if ROWS > 1:  # Don't delete the headers
            for column in range(COLUMNS):
                index = (ROWS - 1, column)
                ENTRIES[index].destroy()
            ROWS -= 1

    def save(self):
        string = ""
        data = []
        for row in range(ROWS):
            currentRow = []
            for column in range(COLUMNS):
                currentRow.append(ENTRIES[(row, column)].get())
            data.append(currentRow)

        del data[0]  # Remove headers from data
        for row in data:
            string += ";".join(row) + "\n"
        with open("data.csv", "w+") as file:
            file.write(string)

    def validate(self, P):
        """
        Perform input validation.

        Allow only an empty value, or a value that can be converted to
        an int.
        """

        if P == "":
            return True
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
        self.table.grid(row=2, column=1, sticky="nsew")

        buttonFrame = tkinter.Frame(root)
        buttonFrame.pack()

        buttonWidth = 9
        saveButton = tkinter.Button(
            buttonFrame,
            text="Save Data",
            command=self.table.save,
            width=buttonWidth,
        )
        saveButton.grid(row=0, column=0)
        addRowButton = tkinter.Button(
            buttonFrame,
            text="Add Row",
            command=self.table.addRow,
            # Green
            bg="#2fba54",
            width=buttonWidth,
        )
        addRowButton.grid(row=0, column=1)
        deleteRowButton = tkinter.Button(
            buttonFrame,
            text="Delete Row",
            command=self.table.deleteRow,
            # Red
            bg="#ff5242",
            width=buttonWidth,
        )
        deleteRowButton.grid(row=0, column=2)


root = tkinter.Tk()
root.title("WRITe")
root.resizable(width=False, height=False)
App(root).pack(side="top", fill="both", expand=True)

root.mainloop()
