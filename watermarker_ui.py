from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab

class watermarker_app():

    def __init__(self):
        self.window = Tk()
        self.window.title("Watermarker")

        self.editing = False
        self.text_angle= 0
        self.watermark_list = []

        self.open = Button(text="Open", command=self.open_image)
        self.open.grid(row=2, column= 1)
        self.save = Button(text= "Save", command= self.save_file)
        self.save.grid(row=2, column= 2)

        self.image = Canvas(bg= "grey", width= 500, height= 500)
        self.watermark = self.image.create_text(250,250,text= "Open Image to Begin", fill= "white", angle=0)
        self.image.grid(row= 1, column= 1, columnspan= 2)

        self.controls = LabelFrame(width= 300, height= 700, text= "Controls",  padx= 15, pady= 15)
        self.controls.grid(row=1, rowspan= 2, column= 3)

        self.rotates = LabelFrame(master= self.controls, text= "Rotate", bg='white', padx= 15, pady= 15)
        self.rotates.grid(row=1, column=1)
        self.clockwise_img = self.image_resize("images/clockwise.png",(50,50))
        self.clockwise = Button(master= self.rotates, image= self.clockwise_img, command= lambda: self.rotate_text("clock"))
        self.clockwise.grid(row= 1, column= 1)
        self.anticlockwise_img = self.image_resize("images/anti-clockwise.png",(50,50))
        self.anticlockwise = Button(master= self.rotates, image= self.anticlockwise_img, command= lambda: self.rotate_text("anti"))
        self.anticlockwise.grid(row= 1, column = 2)

        self.patterns= LabelFrame(master= self.controls, text= "Instances", padx= 15, pady= 15)
        self.patterns.grid(row= 1, column= 2)
        self.pattern_var = StringVar(value= "single")
        self.single_img = self.image_resize('images/single.png',(50,50))
        self.single= Radiobutton(master= self.patterns, image= self.single_img, variable= self.pattern_var, value= "single", indicatoron=0, command=self.pattern_watermark)
        self.single.grid(row=1, column= 1)
        self.multiple_img = self.image_resize('images/multiple.png', (50, 50))
        self.multiple = Radiobutton(master=self.patterns, image=self.multiple_img, variable= self.pattern_var, value='multiple', indicatoron=0, command= self.pattern_watermark)
        self.multiple.grid(row=1, column=2)

        self.opacity = Scale(master= self.controls, label= "Opacity", from_= 0, to= 100, orient= HORIZONTAL, length= 200)
        self.opacity.set(100)
        self.opacity.grid(row= 2, column= 1, columnspan= 2)

        self.font_controls = LabelFrame(master= self.controls, text= "Font Options", padx= 15, pady=15)
        self.font_controls.grid(row= 3, column= 1, columnspan= 2)
        self.text = Text(master= self.font_controls, width= 15, height= 10, highlightbackground="black")
        self.text.bind("<KeyRelease>", lambda e: self.update_watermark())
        self.text.grid(row= 1, rowspan= 3, column= 1)
        self.fontsizes = [9,10,11,12,14,18,24,36,54,66]
        self.size_var = IntVar(master= self.window)
        self.size_var.set(self.fontsizes[0])
        self.fontsize = OptionMenu(self.font_controls, self.size_var, *self.fontsizes)
        self.fontsize.grid(row=1, column=2)

        self.fonts= ["Garamond", "Helvetica", "Courier New", "Brush Script", "Impact", "Old English Text MT"]
        self.font_var = StringVar(master= self.window)
        self.font_var.set(self.fonts[0])
        self.font_type = OptionMenu(self.font_controls, self.font_var, *self.fonts)
        self.font_type.grid(row= 2, column= 2)

        self.colours = ["⚫Black", "🔴Red", "🟢Green", "🔵Blue", "⚪️White", "🟡Yellow"]
        self.col_var = StringVar(master= self.window)
        self.col_var.set(self.colours[0])
        self.font_col = OptionMenu(self.font_controls, self.col_var, *self.colours)
        self.font_col.grid(row= 3, column= 2)

        self.window.mainloop()

    def image_resize(self, image_file, dimensions):
        image= Image.open(image_file)
        resized_image = image.resize(dimensions)
        tk_image = ImageTk.PhotoImage(resized_image)
        return tk_image

    def open_image(self):
        filename = filedialog.askopenfilename()
        if filename:
            # Need to scale image according to its previous dimensions not just make it square
            self.background_img = self.image_resize(filename, (500,500))
            self.image.config(background='white')
            self.image.delete(self.watermark)
            self.image.create_image(250, 250, image=self.background_img)
            self.editing = True

    # Do I need this or just use watermark_text??
    def update_watermark(self, *positions):
        self.image.delete(self.watermark)
        if self.editing:
            text = self.text.get('1.0', END)
            col = self.col_var.get()
            col = ''.join(c for c in col if c.isalpha())
            font = (self.font_var.get(), self.size_var.get())
            if not positions:
                self.watermark = self.image.create_text(250,250,text= text, fill= col, font= font, angle= self.text_angle)
            else:
                self.watermark_list = []
                for i, pos in enumerate(positions):
                    x,y = pos
                    self.watermark_list.append(self.image.create_text(x,y,text= text, fill= col, font= font, angle= self.text_angle))


    def rotate_text(self, direction):
        if self.editing:
            if direction == "clock":
                self.text_angle -= 5
            elif direction == "anti":
                self.text_angle += 5
            self.image.itemconfig(self.watermark, angle= self.text_angle)
            for i in range(len(self.watermark_list)):
                self.image.itemconfig(self.watermark_list[i], angle= self.text_angle)

    def pattern_watermark(self):
        if self.editing:
            self.image.delete(self.watermark)
            for i in range(len(self.watermark_list)):
                self.image.delete(self.watermark_list[i])
            if self.pattern_var.get() == 'single':

                self.update_watermark()
            elif self.pattern_var.get() == "multiple":
                positions = [(x,y) for x in range(0,500,100) for y in range(0,500,100)]
                self.update_watermark(*positions)

    def save_file(self):
        x0 = self.image.winfo_rootx()
        y0 = self.image.winfo_rooty()
        x1 = x0 + self.image.winfo_width()
        y1 = y0 + self.image.winfo_height()
        final_image = ImageGrab.grab(bbox=(x0, y0, x1, y1))

        filepath = filedialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension=".png")
        if not filepath:
            return #i.e. user cancelled
        else:
            final_image.save(filepath)
            print(f"Watermarked image saved to: {filepath}")