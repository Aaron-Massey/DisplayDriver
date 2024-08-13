class UI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Image to Bytes")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.file_path = ""
        self.image = None

        # Create a Notebook widget
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill='both')

        # Create frames for each tab
        self.image_frame = ttk.Frame(self.notebook)
        self.console_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.image_frame, text='Image')
        self.notebook.add(self.console_frame, text='Console')

        # Image tab widgets
        self.label = Label(self.image_frame, text="Select an image")
        self.label.pack()

        self.button = Button(self.image_frame, text="Select Image", command=self.select_image)
        self.button.pack()

        self.convert_button = Button(self.image_frame, text="Convert to Bytecode", command=self.convert_to_bytecode, state='disabled')
        self.convert_button.pack()

        self.image_label = Label(self.image_frame)
        self.image_label.pack()

        # Add toggle buttons in a 2x2 grid
        self.printBinary = BooleanVar()
        self.printHex = BooleanVar(value=True)
        self.printDec = BooleanVar()
        self.printFormatted = BooleanVar(value=True)

        self.toggle_frame = Frame(self.image_frame)
        self.toggle_frame.pack()

        self.binary_check = Checkbutton(self.toggle_frame, text="Print Binary", variable=self.printBinary)
        self.binary_check.grid(row=0, column=0)

        self.hex_check = Checkbutton(self.toggle_frame, text="Print Hex", variable=self.printHex)
        self.hex_check.grid(row=0, column=1)

        self.dec_check = Checkbutton(self.toggle_frame, text="Print Dec", variable=self.printDec)
        self.dec_check.grid(row=1, column=0)

        self.formatted_check = Checkbutton(self.toggle_frame, text="Print Formatted", variable=self.printFormatted)
        self.formatted_check.grid(row=1, column=1)

        # Console tab widgets
        self.console_text = Text(self.console_frame)
        self.console_text.pack(expand=1, fill='both')

        # Redirect stdout to the console text widget
        sys.stdout = TextRedirector(self.console_text)

        self.root.mainloop()

    def select_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        self.label.config(text=self.file_path)

        if self.file_path:
            # Use ImageToBytes.reduceImage to resize the image
            ImageToBytes.reduceImage(self.file_path)
            self.image = Image.open("temp/reduced.jpg")

            # Resize the image to 320x320 for display
            display_image = self.image.resize((320, 320), Image.NEAREST)

            # Display the image in the root window
            img = ImageTk.PhotoImage(display_image)
            self.image_label.config(image=img)
            self.image_label.image = img  # Keep a reference to avoid garbage collection

            # Enable the convert button
            self.convert_button.config(state='normal')

            print("Image loaded successfully")
            print(f"Image path: {self.file_path}")

    def convert_to_bytecode(self):
        ImageToBytes.clear_output()
        ImageToBytes.clear_colors()

        bytecode = ImageToBytes.ImageToBytes(
            "temp/reduced.jpg",
            printHex=self.printHex.get(),
            printBin=self.printBinary.get(),
            PrintDec=self.printDec.get(),
            printFormatted=self.printFormatted.get()
        )

        # Create a new Toplevel window for bytecode display
        bytecode_window = Toplevel(self.root)
        bytecode_window.title("Bytecode")
        bytecode_window.geometry("400x300")

        # Add a button to copy bytecode to clipboard at the top
        copy_button = Button(bytecode_window, text="Copy to Clipboard", command=lambda: self.copy_to_clipboard(bytecode))
        copy_button.pack()

        # Create a frame to hold the Text widget and scrollbar
        frame = Frame(bytecode_window)
        frame.pack(expand=1, fill='both')

        # Create a Text widget for displaying the bytecode
        text_widget = Text(frame)
        text_widget.insert('1.0', bytecode)
        text_widget.pack(side='left', expand=1, fill='both')

        # Create a Scrollbar and link it to the Text widget
        scrollbar = Scrollbar(frame, command=text_widget.yview)
        scrollbar.pack(side='right', fill='y')
        text_widget.config(yscrollcommand=scrollbar.set)

        os.remove("temp/reduced.jpg")

    def copy_to_clipboard(self, bytecode):
        self.root.clipboard_clear()
        self.root.clipboard_append(bytecode)
        self.root.update()  # now it stays on the clipboard after the window is closed
