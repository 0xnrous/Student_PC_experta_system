from tkinter import *
from tkinter import ttk
import tkinter as tk
#from pyknow import *
from experta import *
dictlist = [dict() for x in range(16)]


root = tk.Tk()
root.geometry("750x450") 
root.title("PC Builder")
root.configure(bg="#32402f")  # Set background color for the root window
root.resizable(False, False)  # stops the user from maximizing the window 


for i in range(16):
    s = "./Builds/build"+str(i+1)+".txt"
    with open (s, "r") as myfile:
        dictlist[i] = dict(item.rstrip("\n").split(":") for item in myfile)
        
CPU_dict = {}
GPU_dict = {}
HardDrive_dict = {}
Motherboard_dict = {}

with open ("CPU.txt", "r") as myfile:
    CPU_dict = dict(item.rstrip("\n").split(":") for item in myfile)
with open ("GPU.txt", "r") as myfile:
    GPU_dict = dict(item.rstrip("\n").split(":") for item in myfile)
with open ("INTHD.txt", "r") as myfile:
    HardDrive_dict = dict(item.rstrip("\n").split(":") for item in myfile)
with open ("Motherboard.txt", "r") as myfile:
    Motherboard_dict = dict(item.rstrip("\n").split(":") for item in myfile)

CPU = StringVar()
GPU = StringVar()
MB = StringVar()
HD = StringVar()
budget = StringVar()
usage = StringVar()

BUILDS = StringVar()

arr = []

class Engine(KnowledgeEngine):
    Spec = []
    budget = 0
    CPU =''
    GPU =''
    MB = ''
    HD = ''
    usage1 = ''
    
    def get_budget_usage(self,usage1,budget):
        #self.budget = input("What is your budget? ")
        self.budget = budget
        self.declare(Fact(budget = self.budget))
        #usage = input("What is your usage for the PC? ")
        self.usage1 = usage1
        self.declare(Fact(usage=self.usage1))
        
    
    def getSpec(self,Spec):
        self.Spec = Spec
        counter = 0
        for item in self.Spec:
            if item == '':
                counter = counter +1
                if(counter == 4):
                    self.declare(Fact(allclear = True))
        if(counter < 4):
            self.declare(Fact(allclear = False))
            
    def Display(self,i):
        name = dictlist[i]['name']
        usage = dictlist[i]['usage']
        cpu = dictlist[i]['CPU']
        gpu = dictlist[i]['GPU']
        mb = dictlist[i]['Motherboard']
        hd = dictlist[i]['Hard Drive']
                
        listbox.insert(END,"Name : " + name)
        listbox.insert(END,"Usage : " + usage)
        listbox.insert(END,"CPU : " + cpu)
        listbox.insert(END,"GPU : " + gpu)
        listbox.insert(END,"Motherboard : " + mb)
        listbox.insert(END,"Hard Drive : " + hd)
        listbox.insert(END,"\n_____________________________________________________________________________________\n")

    @Rule(OR(~Fact(CPU=W()),
             ~Fact(GPU=W()),
             ~Fact(HardDrive=W()),
             ~Fact(Motherboard=W())))
    def defRules(self):
        for word in self.Spec:
            if word in CPU_dict.keys():
                self.CPU = word
                self.declare(Fact(CPU=word))
            if word in GPU_dict.keys():
                self.GPU = word
                self.declare(Fact(GPU=word))
            if word in HardDrive_dict.keys():
                self.HD = word
                self.declare(Fact(HardDrive=word))
            if word in Motherboard_dict.keys():
                self.MB = word
                self.declare(Fact(Motherboard=word))
      

    # Usage for GUI to show results  
    @Rule(AND(Fact(usage='Gaming'),
             ~Fact(CPU=W()),
             ~Fact(GPU=W()),
             ~Fact(HardDrive=W()),
             ~Fact(Motherboard=W()),
             Fact(allclear = True)))
    def showgaming(self):
        for i in range(len(dictlist)):
            if 'Gaming' in dictlist[i]['usage']:
                self.Display(i)
                
    
    @Rule(AND(Fact(usage='Education'),
             ~Fact(CPU=W()),
             ~Fact(GPU=W()),
             ~Fact(HardDrive=W()),
             ~Fact(Motherboard=W()),
             Fact(allclear = True)))
    def showedu(self):
        for i in range(len(dictlist)):
            if 'Education' in dictlist[i]['usage']:
                self.Display(i)
    
    @Rule(AND(Fact(usage='Internet'),
             ~Fact(CPU=W()),
             ~Fact(GPU=W()),
             ~Fact(HardDrive=W()),
             ~Fact(Motherboard=W()),
             Fact(allclear = True)))
    def showinternet(self):
        for i in range(len(dictlist)):
            if 'Internet' in dictlist[i]['usage']:
                self.Display(i)
    
    
    
# 1
    @Rule(AND(Fact(CPU=W()),
              NOT(Fact(GPU=W())),
              NOT(Fact(Motherboard=W())),
              NOT(Fact(HardDrive=W())),
              Fact(budget=W())))
    def build1(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.CPU in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(CPU_dict[self.CPU])
                cost += (int(Motherboard_dict[dictlist[i]['Motherboard']]) + 
                        int(HardDrive_dict[dictlist[i]['Hard Drive']]) + int(GPU_dict[dictlist[i]['GPU']]))
                if cost <= int(self.budget):
                    self.Display(i)

# 2 
    @Rule(AND(NOT(Fact(CPU=W())),
              Fact(GPU=W()),
              NOT(Fact(Motherboard=W())),
              NOT(Fact(HardDrive=W())),
              Fact(budget=W())))
    def build2(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.GPU in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(GPU_dict[self.GPU])
                cost += (int(Motherboard_dict[dictlist[i]['Motherboard']]) + 
                        int(HardDrive_dict[dictlist[i]['Hard Drive']]) + int(CPU_dict[dictlist[i]['CPU']]))
                if cost <= int(self.budget):
                    self.Display(i)
       
# 3             
    @Rule(AND(NOT(Fact(CPU=W())),
              NOT(Fact(GPU=W())),
              Fact(Motherboard=W()),
              NOT(Fact(HardDrive=W())),
              Fact(budget=W())))
    def build3(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.MB in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(Motherboard_dict[self.MB])
                cost += (int(GPU_dict[dictlist[i]['GPU']]) + 
                        int(HardDrive_dict[dictlist[i]['Hard Drive']]) + int(CPU_dict[dictlist[i]['CPU']]))
                if cost <= int(self.budget):
                    self.Display(i)
    
# 4
    @Rule(AND(NOT(Fact(CPU=W())),
              NOT(Fact(GPU=W())),
              NOT(Fact(Motherboard=W())),
              Fact(HardDrive=W()),
              Fact(budget=W())))
    def build4(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.HD in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(HardDrive_dict[self.HD])
                cost += (int(GPU_dict[dictlist[i]['GPU']]) + 
                        int(Motherboard_dict[dictlist[i]['Motherboard']]) + int(CPU_dict[dictlist[i]['CPU']]))
                if cost <= int(self.budget):
                    self.Display(i)
    
# 5 
    @Rule(AND(Fact(CPU=W()),
              Fact(GPU=W()),
              NOT(Fact(Motherboard=W())),
              NOT(Fact(HardDrive=W())),
              Fact(budget=W())))
    def build12(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.CPU in dictlist[i].values() and self.GPU in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(CPU_dict[self.CPU]) + int(GPU_dict[self.GPU])
                cost += int(Motherboard_dict[dictlist[i]['Motherboard']]) + int(HardDrive_dict[dictlist[i]['Hard Drive']])
                if cost <= int(self.budget):
                    self.Display(i)


# 8
    @Rule(AND(NOT(Fact(CPU=W())),
              NOT(Fact(GPU=W())),
              Fact(Motherboard=W()),
              Fact(HardDrive=W()),
              Fact(budget=W())))
    def build34(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.MB in dictlist[i].values() and self.HD in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(HardDrive_dict[self.HD]) + int(Motherboard_dict[self.MB])
                cost += int(CPU_dict[dictlist[i]['CPU']]) + int(GPU_dict[dictlist[i]['GPU']])
                if cost <= int(self.budget):
                    self.Display(i)
# 9   
    @Rule(AND(Fact(CPU=W()),
              NOT(Fact(GPU=W())),
              Fact(Motherboard=W()),
              NOT(Fact(HardDrive=W())),
              Fact(budget=W())))
    def build13(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.MB in dictlist[i].values() and self.CPU in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(Motherboard_dict[self.MB]) + int(CPU_dict[self.CPU])
                cost += int(GPU_dict[dictlist[i]['GPU']]) + int(HardDrive_dict[dictlist[i]['Hard Drive']])
                if cost <= int(self.budget):
                    self.Display(i)
# 10     
    @Rule(AND(NOT(Fact(CPU=W())),
              Fact(GPU=W()),
              NOT(Fact(Motherboard=W())),
              Fact(HardDrive=W()),
              Fact(budget=W())))
    def build24(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.GPU in dictlist[i].values() and self.HD in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(GPU_dict[self.GPU]) + int(HardDrive_dict[self.HD])
                cost += int(CPU_dict[dictlist[i]['CPU']]) + int(Motherboard_dict[dictlist[i]['Motherboard']])
                if cost <= int(self.budget):
                    self.Display(i)
# 11 
    @Rule(AND(Fact(CPU=W()),
              NOT(Fact(GPU=W())),
              NOT(Fact(Motherboard=W())),
              Fact(HardDrive=W()),
              Fact(budget=W())))
    def build14(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.CPU in dictlist[i].values() and self.HD in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(CPU_dict[self.CPU]) + int(HardDrive_dict[self.HD])
                cost += int(GPU_dict[dictlist[i]['GPU']]) + int(Motherboard_dict[dictlist[i]['Motherboard']])
                if cost <= int(self.budget):
                    self.Display(i)
 # 12   
    @Rule(AND(NOT(Fact(CPU=W())),
              Fact(GPU=W()),
              Fact(Motherboard=W()),
              NOT(Fact(HardDrive=W())),
              Fact(budget=W())))
    def build23(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.GPU in dictlist[i].values() and self.MB in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(GPU_dict[self.GPU]) + int(Motherboard_dict[self.MB])
                cost += int(CPU_dict[dictlist[i]['CPU']]) + int(HardDrive_dict[dictlist[i]['Hard Drive']])
                if cost <= int(self.budget):
                    self.Display(i)
 # 13    
    @Rule(AND(Fact(CPU=W()),
              Fact(GPU=W()),
              Fact(Motherboard=W()),
              NOT(Fact(HardDrive=W())),
              Fact(budget=W())))
    def build123(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.GPU in dictlist[i].values() and self.MB in dictlist[i].values() and self.CPU in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(GPU_dict[self.GPU]) + int(Motherboard_dict[self.MB]) + int(CPU_dict[self.CPU])
                cost += int(HardDrive_dict[dictlist[i]['Hard Drive']])
                if cost <= int(self.budget):
                    self.Display(i)
  # 14                  
    @Rule(AND(NOT(Fact(CPU=W())),
              Fact(GPU=W()),
              Fact(Motherboard=W()),
              Fact(HardDrive=W()),
              Fact(budget=W())))
    def build234(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.GPU in dictlist[i].values() and self.MB in dictlist[i].values() and self.HD in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(GPU_dict[self.GPU]) + int(Motherboard_dict[self.MB]) + int(HardDrive_dict[self.HD])
                cost += int(CPU_dict[dictlist[i]['CPU']])
                if cost <= int(self.budget):
                    self.Display(i)
     
 # 15
    @Rule(AND(Fact(CPU=W()),
              NOT(Fact(GPU=W())),
              Fact(Motherboard=W()),
              Fact(HardDrive=W()),
              Fact(budget=W())))
    def build134(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.CPU in dictlist[i].values() and self.MB in dictlist[i].values() and self.HD in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(CPU_dict[self.CPU]) + int(Motherboard_dict[self.MB]) + int(HardDrive_dict[self.HD])
                cost += int(GPU_dict[dictlist[i]['GPU']])
                if cost <= int(self.budget):
                    self.Display(i)
  # 16   
    @Rule(AND(Fact(CPU=W()),
              Fact(GPU=W()),
              NOT(Fact(Motherboard=W())),
              Fact(HardDrive=W()),
              Fact(budget=W())))
    def build124(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if self.GPU in dictlist[i].values() and self.CPU in dictlist[i].values() and self.HD in dictlist[i].values() and dictlist[i]["usage"] == self.usage1:
                cost += int(GPU_dict[self.GPU]) + int(CPU_dict[self.CPU]) + int(HardDrive_dict[self.HD])
                cost += int(Motherboard_dict[dictlist[i]['Motherboard']])
                if cost <= int(self.budget):
                    self.Display(i)
                    
 # 17
    @Rule(AND(Fact(CPU=W()),
              Fact(GPU=W()),
              Fact(Motherboard=W()),
              Fact(HardDrive=W()),
              Fact(budget=W())))
    def build1234(self):
        cost = 0
        for i in range(len(dictlist)):
            cost = 0
            if (self.GPU in dictlist[i].values() and self.CPU in dictlist[i].values() 
                and self.HD in dictlist[i].values() and self.MB in dictlist[i].values()) and dictlist[i]["usage"] == self.usage1:
                cost += int(GPU_dict[self.GPU]) + int(CPU_dict[self.CPU]) + int(HardDrive_dict[self.HD]) + int(Motherboard_dict[self.MB])
                if cost <= int(self.budget):
                    self.Display(i)                        



# Define build function
def build():
    clear_listbox()
    CPU = entry2.get()
    GPU = entry3.get()
    HD = entry4.get()
    MB = entry5.get()
    budget = entry1.get()
    usage1 = dropDown.get()
    
    arr.append(CPU)
    arr.append(GPU)
    arr.append(HD)
    arr.append(MB)
    engine = Engine()
    engine.reset()
    engine.getSpec(arr)
    engine.get_budget_usage(usage1, budget)
    engine.run()
    
def clear_listbox():
    listbox.delete(0, "end")
    arr.clear()


greeting_text = "Hello! 🙌🏾 \n\n\nA startup for computer science students to build a \nPC based on your requirements and budget. 💻 👨🏾‍💻"

greeting = tk.Label(root, text=greeting_text, fg="#faf2e9", bg="#32402f", font=("Courier", 12, "bold"), anchor="w", width=60, padx=110, pady=40)
greeting.pack(side="top", fill="x")  # Use pack instead of grid


# Define frames
topFrame = tk.Frame(root, bg="#f0f0f0")
topFrame.pack(fill="both", expand=True)

leftFrame = tk.Frame(topFrame, bg="#32402f")
leftFrame.pack(side="left", padx=10, pady=10)

rightFrame = tk.Frame(topFrame, bg="#32402f")
rightFrame.pack(side="right", padx=10, pady=10)


# Create labels and entries
label1 = tk.Label(leftFrame, text="Usage:", font=("Arial", 12), bg="#32402f", fg="#faf2e9")
label1.grid(row=0, column=0, padx=10, pady=5, sticky="e")

# Style for the Combobox
style = ttk.Style()
style.theme_create("combostyle", parent="alt", settings={
    "TCombobox": {"configure": {"selectbackground": "#32402f", "fieldbackground": "#faf2e9", "arrowcolor": "#faf2e9", "background": "#faf2e9", "foreground": "#333333", "bordercolor": "#32402f"}}})
style.theme_use("combostyle")

dropDown = ttk.Combobox(leftFrame, values=['Gaming', 'Internet', 'Education'], width=20)
dropDown.grid(row=0, column=1, padx=10, pady=5, sticky="w")
dropDown.set("Select usage")  # Initial text displayed in the combobox

label2 = tk.Label(leftFrame, text="Budget:", 
                  fg="#faf2e9", bg="#32402f", 
                  font=("Courier", 12), 
                  wraplength=300, justify="left", 
                  anchor="w", width=6, padx=3, pady=2)
label2.grid(row=1, column=0, padx=10, pady=5, sticky="e")

# Configure style for the Entry widget
entry_style = {
    "TEntry": {
        "configure": {"foreground": "#100F13", "background": "#32402f", "font": ("Courier", 20)}
    }
}

style.theme_create("entrystyle", parent="alt", settings=entry_style)
style.theme_use("entrystyle")

entry1 = ttk.Entry(leftFrame)
entry1.grid(row=1, column=1, padx=10, pady=5)
entry1.insert(0, "Enter your budget $")


# Create labels and entries
label3 = tk.Label(leftFrame, text="CPU:", font=("Arial", 12), bg="#32402f", fg="#faf2e9")
label3.grid(row=2, column=0, padx=10, pady=5, sticky="e")

label4 = tk.Label(leftFrame, text="GPU:", font=("Arial", 12), bg="#32402f", fg="#faf2e9")
label4.grid(row=3, column=0, padx=10, pady=5, sticky="e")

label5 = tk.Label(leftFrame, text="Hard Drive:", font=("Arial", 12), bg="#32402f", fg="#faf2e9")
label5.grid(row=4, column=0, padx=10, pady=5, sticky="e")

label6 = tk.Label(leftFrame, text="Motherboard:", font=("Arial", 12), bg="#32402f", fg="#faf2e9")
label6.grid(row=5, column=0, padx=10, pady=5, sticky="e")

# Define style for the Entry widget
entry_style = {
    "foreground": "#100F13",  # Change to black foreground color
    "background": "#32402f",  # Change to white background color
    "font": ("Courier", 12)
}


entry2 = ttk.Entry(leftFrame, style="TEntry", **entry_style)
entry2.grid(row=2, column=1, padx=10, pady=5)
entry2.insert(0,"")


entry3 = ttk.Entry(leftFrame, style="TEntry", **entry_style)
entry3.grid(row=3, column=1, padx=10, pady=5)
entry3.insert(0,"")


entry4 = ttk.Entry(leftFrame, style="TEntry", **entry_style)
entry4.grid(row=4, column=1, padx=10, pady=5)
entry4.insert(0,"")


entry5 = ttk.Entry(leftFrame, style="TEntry", **entry_style)
entry5.grid(row=5, column=1, padx=10, pady=5)
entry5.insert(0,"")



# Create build button
button1 = ttk.Button(leftFrame, text="Build!", command=build)
button1.grid(row=6, column=0, padx=10, pady=20, sticky="e")

# Create clear button next to build button
clear_button = ttk.Button(leftFrame, text="Clear!", command=clear_listbox)
clear_button.grid(row=6, column=1, padx=10, pady=20, sticky="e")  # Change sticky to "e"

# Create listbox
label7 = tk.Label(rightFrame, text="Available Builds:", font=("Arial", 12), bg="#f0f0f0")
label7.pack(pady=5)

scrollbar = ttk.Scrollbar(rightFrame)
scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(rightFrame, yscrollcommand=scrollbar.set, width=50, height=20)  # Increase width and height
listbox.pack(fill="both", padx=10, pady=15)

scrollbar.config(command=listbox.yview)


# Run the GUI
root.mainloop()