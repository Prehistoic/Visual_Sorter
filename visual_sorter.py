from tkinter import *
from tkinter.messagebox import *
import random
from time import sleep

class Sorter_interface:
    def __init__(self,parent):
        self.tab_values = []
        self.canvas_width = 1000
        self.sleep_delay = 0.001

        self.myParent = parent
        self.myParent.bind_all("<Button-4>",self.rolling_up)
        self.myParent.bind_all("<Button-5>",self.rolling_down)

        self.menubar = Menu(self.myParent)
        menu1 = Menu(self.menubar, tearoff=0)
        menu1.add_command(label="Bubble sort", command=self.visual_bubblesort)
        menu1.add_command(label="Quick sort", command=self.visual_quicksort)
        menu1.add_command(label="Insertion sort", command=self.visual_insertionsort)
        menu1.add_command(label="Selection sort", command=self.visual_selectionsort)
        self.menubar.add_cascade(label="Choose sorting algorithm", menu=menu1)
        self.menubar.add_command(label="Help", command=self.alert_help)
        self.menubar.add_command(label="Quit", command=self.myParent.quit)
        self.myParent.config(menu=self.menubar)

        self.lbl1 = Label(self.myParent, text="")
        self.lbl1.pack()

        self.myCanvas = Canvas(self.myParent, width=self.canvas_width, height=500, background='white')
        self.myCanvas.pack()

        self.myContainer = Frame(parent)
        self.myContainer.pack()

        self.lbl2 = Label(self.myContainer, text="")
        self.lbl2.pack()

        self.myScale = Scale(self.myContainer, orient='horizontal', from_=2, to=self.canvas_width//2, command=self.new_scale)
        self.myScale.set(self.canvas_width//4)
        self.myScale.pack()

    def rolling_up(self, event):
        scale_value = self.myScale.get()
        self.myScale.set(scale_value+1)

    def rolling_down(self,event):
        scale_value = self.myScale.get()
        self.myScale.set(scale_value-1)

    def alert_help(self):
        showinfo('Help','To use this tool, just choose a number of rectangles with the scrollbar and then choose an algorithm in the menu bar to sort the rectangles !')

    def new_scale(self,scale_value):
        self.myCanvas.delete("all")
        self.tab_values=[]
        rect_width = self.canvas_width/int(scale_value)
        for i in range(1,int(scale_value)+1):
            rect_height = random.randint(0,500)
            self.tab_values.append(rect_height)
            self.myCanvas.create_rectangle(i*rect_width,500-rect_height,(i-1)*rect_width,500,fill='blue')
        self.myCanvas.update_idletasks()

    def swap(self,index1,index2):
        tmp = self.tab_values[index1]
        self.tab_values[index1] = self.tab_values[index2]
        self.tab_values[index2] = tmp
        self.redraw_canvas([index1,index2])

    def redraw_canvas(self,highlighted_indexes):
        self.myCanvas.delete("all")
        scale_value = self.myScale.get()
        rect_width = self.canvas_width/scale_value
        for i in range(1,scale_value+1):
            rect_height=self.tab_values[i-1]
            if(highlighted_indexes.count(i)>0):
                self.myCanvas.create_rectangle(i*rect_width,500-rect_height,(i-1)*rect_width,500,fill='yellow')
            else:
                self.myCanvas.create_rectangle(i*rect_width,500-rect_height,(i-1)*rect_width,500,fill='green')
        self.myCanvas.update_idletasks()
        sleep(self.sleep_delay)

    def partition(self,low,high):
        pivot = self.tab_values[high]
        i = low-1
        for j in range(low,high):
            if(self.tab_values[j]<pivot):
                i+=1
                self.swap(i,j)
        self.swap(i+1,high)
        return i+1

    def quicksort_algorithm(self,low,high):
        if(low < high):
            part = self.partition(low,high)
            self.quicksort_algorithm(low,part-1)
            self.quicksort_algorithm(part+1,high)

    def visual_quicksort(self):
        self.myScale.config(state=DISABLED)
        scale_value = self.myScale.get()
        self.sleep_delay = 0.01
        self.quicksort_algorithm(0,scale_value-1)
        self.redraw_canvas([])
        self.myScale.config(state=NORMAL)

    def bubblesort_algorithm(self,len):
        sorted = False
        while(not sorted):
            swapped = 0
            for i in range(len-1):
                if self.tab_values[i]>self.tab_values[i+1]:
                    swapped+=1
                    self.swap(i,i+1)
            if(swapped==0):
                sorted = True

    def visual_bubblesort(self):
        self.myScale.config(state=DISABLED)
        scale_value = self.myScale.get()
        self.sleep_delay = 0.00001
        self.bubblesort_algorithm(scale_value)
        self.redraw_canvas([])
        self.myScale.config(state=NORMAL)

    def selectionsort_algorithm(self,len):
        for i in range(len):
            min_index = i
            for j in range(i,len):
                if(self.tab_values[min_index]>self.tab_values[j]):
                    min_index = j
            self.swap(i,min_index)

    def visual_selectionsort(self):
        self.myScale.config(state=DISABLED)
        scale_value = self.myScale.get()
        self.sleep_delay = 0.05
        self.selectionsort_algorithm(scale_value)
        self.redraw_canvas([])
        self.myScale.config(state=NORMAL)

    def insertionsort_algorithm(self,len):
        for i in range(1,len):
            key = self.tab_values[i]
            j = i-1
            while j >= 0 and key < self.tab_values[j] :
                    self.tab_values[j+1] = self.tab_values[j]
                    j -= 1
            self.tab_values[j+1] = key
            self.redraw_canvas([i,j+1])

    def visual_insertionsort(self):
        self.myScale.config(state=DISABLED)
        scale_value = self.myScale.get()
        self.sleep_delay = 0.05
        self.insertionsort_algorithm(scale_value)
        self.redraw_canvas([])
        self.myScale.config(state=NORMAL)

root = Tk()
root.title('Visual sorter')
root.geometry("1200x600")
sorter = Sorter_interface(root)
root.mainloop()
