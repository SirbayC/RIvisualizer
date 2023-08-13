# import necessary packages
import os
import requests
import re
from datetime import datetime
from tkinter import *
from PIL import ImageTk, Image
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt


def Create_plot(start_date, end_date):
    print("Creating from")
    print(start_date)
    print(end_date)
    # retrieve data from website
    URL = "https://web.archive.org/web/20220414174609/https://dspb.ro/rata-de-incidenta/"
    page = requests.get(URL)
    results = BeautifulSoup(page.content, "html.parser")
    data = results.find_all("div", class_ = "entry-content")
    dataset = str(data).split("<p>")
    del dataset[:2]
    dataset.reverse()

    # process data
    my_dict = {}
    first_pass = True
    actual_first_date = datetime.now()
    actual_end_date = datetime.now()
    for entry in dataset:
        date = re.search(r'^\S*', entry)[0]
        value = re.search(r'(?<=valoarea de ).*?(?=</p>)', entry)[0]
        date_obj = datetime.strptime(date, "%d.%m.%Y")
        if start_date <= date_obj <= end_date:
            if first_pass:
                actual_first_date = date_obj
                first_pass = False
            actual_end_date = date_obj
            # print(date_obj)
            my_dict[date_obj] = float(value)

    # set the layout
    fig = plt.figure()
    fig.patch.set_facecolor('#FBEEE6')
    csfont = {'fontname': 'Consolas'}
    plt.title(
        f'Rata de incidență in București între {actual_first_date.strftime("%d.%m.%Y")} și {actual_end_date.strftime("%d.%m.%Y")}',
        **csfont)
    plt.xticks(rotation = 45)
    plt.plot(my_dict.keys(), my_dict.values(), color = "#DFB15B")
    plt.tight_layout()

    # styling
    plt.grid(color = 'w', linestyle = 'solid')
    ax = plt.gca()
    ax.set_facecolor('#CAD8DB')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors = 'gray', direction = 'out')
    for tick in ax.get_xticklabels():
        tick.set_color('black')
    for tick in ax.get_yticklabels():
        tick.set_color('black')

    # show and save
    plt.savefig('graph.png', dpi = 300)
    # plt.show()


# create GUI
root = Tk()
root.geometry("700x500")
root.iconbitmap("icon.ico")
root.title('RI Visualiser')
root.configure(bg = "#AAC9CE")


def Click_reset():
    os.remove('graph.png')
    for widget in root.winfo_children():
        widget.grid_forget()
    Label_2.grid(column = 0, row = 0, columnspan = 2, sticky = 'e', padx = 50, pady = 20)
    Button_da.grid(column = 0, row = 1, columnspan = 1, sticky = 'e', padx = 50)
    Button_nu.grid(column = 1, row = 1, columnspan = 1, sticky = 'w', padx = 50)


def Clear_screen():
    Label_1.grid_forget()
    Label_2.grid_forget()
    Button_da.grid_forget()
    Button_nu.grid_forget()


def Click_showimg():
    img = Image.open('graph.png')
    img = img.resize((500, 375))
    img = ImageTk.PhotoImage(img)
    panel = Label(root, image = img)
    panel.image = img
    panel.grid(column = 0, row = 0, padx = 100, pady = 20)


def Click_da():
    start_date = datetime(2020, 1, 1)
    end_date = datetime.now()
    Create_plot(start_date, end_date)
    Clear_screen()
    Click_showimg()
    Button_reset.grid(column = 0, row = 1)


def Click_nu():
    Clear_screen()

    start_date = datetime.now()
    end_date = datetime.now()

    start_date_fixed = False
    end_date_fixed = False

    # query 1
    Label_3 = Label(root, text = '> Precizează intervalul dorit (folosește formatul dd.mm.yyyy sau \nintrodu "azi")',
                    font = ("Consolas", 12), bg = "#AAC9CE", justify = LEFT)
    Label_3.grid(column = 0, row = 0, sticky = 'w', padx = 50, pady = (30, 15))

    # query 2
    Label_4 = Label(root, text = "Introdu data de începere: ", font = ("Consolas", 12), bg = "#AAC9CE")
    Label_4.grid(column = 0, row = 1, sticky = 'w', padx = (50, 0), pady = 15)
    Entry_1 = Entry(root, width = 15, font = ("Consolas", 12), background = "#E6D7BC")
    Entry_1.grid(column = 0, row = 1, sticky = 'w', padx = (290, 0), pady = 15)

    def Click_3():
        input_start = Entry_1.get()
        if len(input_start) > 0:
            nonlocal start_date_fixed
            start_date_fixed = True

            input_start = Entry_1.get()
            if input_start != 'azi':
                nonlocal start_date
                start_date = datetime.strptime(input_start, "%d.%m.%Y")
            Button_3.grid_forget()

            img = Image.open('tick.png')
            img = img.resize((20, 20))
            img = ImageTk.PhotoImage(img)
            panel = Label(root, image = img, borderwidth = 0)
            panel.image = img
            panel.grid(column = 0, row = 1, sticky = 'w', padx = (450, 0), pady = 15)
        else:
            Label_9 = Label(root, text = "Data de începere nu este validă!", font = ("Consolas", 10),
                            bg = "#AAC9CE")
            Label_9.grid(column = 0, row = 4, sticky = 'w', padx = (50, 0))
            root.after(1500, Label_9.destroy)

    Button_3 = Button(root, text = "Confirmă", font = ("Consolas", 12), command = Click_3, bg = "#DFB15B",
                      borderwidth = 1)
    Button_3.grid(column = 0, row = 1, sticky = 'w', padx = 450, pady = 15)

    # query 3
    Label_5 = Label(root, text = "Introdu data de final: ", font = ("Consolas", 12), bg = "#AAC9CE")
    Label_5.grid(column = 0, row = 2, sticky = 'w', padx = (50, 0), pady = 15)
    Entry_2 = Entry(root, width = 15, font = ("Consolas", 12), background = "#E6D7BC")
    Entry_2.insert(END, 'azi')
    Entry_2.grid(column = 0, row = 2, sticky = 'w', padx = (290, 0), pady = 15)

    def Click_4():
        if start_date_fixed:
            nonlocal end_date
            input_end = Entry_2.get()
            if input_end != 'azi':
                end_date = datetime.strptime(input_end, "%d.%m.%Y")
            if start_date < end_date:
                nonlocal end_date_fixed
                end_date_fixed = True

                Button_4.grid_forget()

                img = Image.open('tick.png')
                img = img.resize((20, 20))
                img = ImageTk.PhotoImage(img)
                panel = Label(root, image = img, borderwidth = 0)
                panel.image = img
                panel.grid(column = 0, row = 2, sticky = 'w', padx = (450, 0), pady = 15)
            else:
                Label_8 = Label(root, text = "Data de începere nu este înaintea celei de final!", font = ("Consolas", 10),
                                bg = "#AAC9CE")
                Label_8.grid(column = 0, row = 4, sticky = 'w', padx = (50, 0))
                root.after(1500, Label_8.destroy)
        else:
            Label_7 = Label(root, text = "Data de începere nu a fost fixată!", font = ("Consolas", 10), bg = "#AAC9CE")
            Label_7.grid(column = 0, row = 4, sticky = 'w', padx = (50, 0))
            root.after(1500, Label_7.destroy)

    Button_4 = Button(root, text = "Confirmă", font = ("Consolas", 12), command = Click_4, bg = "#DFB15B",
                      borderwidth = 1)
    Button_4.grid(column = 0, row = 2, sticky = 'w', padx = 450, pady = 15)

    # query 4
    def Click_5():
        if start_date_fixed and end_date_fixed:
            for widget in root.winfo_children():
                widget.grid_forget()
            Create_plot(start_date, end_date)
            Click_showimg()
            Button_reset.grid(column = 0, row = 1)
        else:
            Label_6 = Label(root, text = "Data de începere / final nu a fost fixată!", font = ("Consolas", 10), bg = "#AAC9CE")
            Label_6.grid(column = 0, row = 4, sticky = 'w', padx = (50, 0))
            root.after(1500, Label_6.destroy)

    Button_5 = Button(root, text = "> Creează grafic", font = ("Consolas", 12), command = Click_5, bg = "#DFB15B",
                      borderwidth = 1)
    Button_5.grid(column = 0, row = 3, sticky = 'w', padx = 50, pady = 15)


Label_1 = Label(root, text = "> Bine ai venit la serviciul de vizualizare a ratei de incidență.",
                font = ("Consolas", 12), bg = "#AAC9CE")
Label_1.grid(column = 0, row = 1, columnspan = 2, sticky = 'w', padx = 50, pady = (30, 15))
Label_2 = Label(root,
                text = "> La nivelul Municipiului Bucuresti, DSP a raportat valorile între \n 05.02.2021 și 10.03.2022. Vrei să folosești tot intervalul de timp \n disponibil?",
                font = ("Consolas", 12), bg = "#AAC9CE", justify = LEFT)
Label_2.grid(column = 0, row = 2, columnspan = 2, sticky = 'e', padx = 50)
Button_da = Button(root, text = "> Da", font = ("Consolas", 12), command = Click_da, bg = "#DFB15B", height = 2,
                   width = 10, borderwidth = 1)
Button_da.grid(column = 0, row = 3, columnspan = 1, sticky = 'e', pady = 30, padx = 50)
Button_nu = Button(root, text = "> Nu", font = ("Consolas", 12), command = Click_nu, bg = "#DFB15B", height = 2,
                   width = 10, borderwidth = 1)
Button_nu.grid(column = 1, row = 3, columnspan = 1, sticky = 'w', pady = 30, padx = 50)
Button_reset = Button(root, text = "> Resetează", font = ("Consolas", 12), command = Click_reset, bg = "#DFB15B",
                      height = 2, width = 15, borderwidth = 1)

root.mainloop()

# delete graph after closing
try:
    os.remove('graph.png')
except:
    print('Niciun grafic nu a fost creat')

