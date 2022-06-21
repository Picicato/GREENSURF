from tkinter import *
import time
import threading
import psutil
from emissions_tracker import (EmissionsTracker,OfflineEmissionsTracker,track_emissions)
from system_info import *
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import ImageTk, Image


gui = Tk()

def init_Gui():
	gui.iconbitmap(r'greensurf_icon.ico')
	gui.title("GREENSURF")
	gui.minsize(width=1024, height=600)
	gui.maxsize(width=1024, height=600)
	gui.geometry("1024x600")
	gui.config(bg='#212121')

	w_title = Canvas(gui, width=1000, height=70, highlightbackground="#3B3B3B", bg='#3B3B3B')
	w_title.place(x=10,y=10)
	w_title.create_text(150, 40, text="GREENSURF", fill="white", font=('Helvetica 30 bold'))
	w_graph = Canvas(gui, width = 600, height=420, highlightbackground="#3B3B3B", bg='#3B3B3B')
	w_graph.place(x=10, y=100)
	w_timer_title = Canvas(gui, width=378, height=35, highlightbackground="#3B3B3B", bg='#3B3B3B')
	w_timer_title.place(x=630, y=100)
	w_timer_title.create_text(135, 20, text="Durée de fonctionnement :", fill="white", font=('Helvetica 14 bold'))
	w_timer_display = Canvas(gui, width=378, height=60, highlightbackground="#3B3B3B", bg='#212121')
	w_timer_display.place(x=630, y=135)
	w_emissions_title = Canvas(gui, width=378, height=35, highlightbackground="#3B3B3B", bg='#3B3B3B')
	w_emissions_title.place(x=630, y=210)
	w_emissions_title.create_text(155, 20, text="Emissions totales (kg.CO₂eq) :", fill="white", font=('Helvetica 14 bold'))
	w_emissions_display = Canvas(gui, width=378, height=60, highlightbackground="#3B3B3B", bg='#212121')
	w_emissions_display.place(x=630, y=245)
	w_cost_title = Canvas(gui, width=378, height=35, highlightbackground="#3B3B3B", bg='#3B3B3B')
	w_cost_title.place(x=630, y=320)
	w_cost_title.create_text(105, 20, text="Coûts financier (€) :", fill="white", font=('Helvetica 14 bold'))
	w_cost_display = Canvas(gui, width=378, height=60, highlightbackground="#3B3B3B", bg='#212121')
	w_cost_display.place(x=630, y=355)
	w_cpu = Canvas(gui, width = 420, height=50, highlightbackground="#006902", bg='#006902')
	w_cpu.place(x=80, y=535)
	w_cpu.create_text(170, 20, text=cpuname(), fill="white", font=('Helvetica 12 bold'))
	w_cpu_label = Canvas(gui, width = 60, height=50, highlightbackground="#212121", bg='#212121')
	w_cpu_label.place(x=10,y=535)
	w_cpu_label.create_text(30, 25, text="CPU", fill="white", font=('Helvetica 20 bold'))
	w_gpu = Canvas(gui, width = 420, height=50, highlightbackground="#006902", bg='#006902')
	w_gpu.place(x=590, y=535)
	w_gpu.create_text(120, 20, text=gpuname(), fill="white", font=('Helvetica 12 bold'))
	w_gpu_label = Canvas(gui, width = 60, height=50, highlightbackground="#212121", bg='#212121')
	w_gpu_label.place(x=520,y=535)
	w_gpu_label.create_text(30, 25, text="GPU", fill="white", font=('Helvetica 20 bold'))

initialized = False
if not initialized:
	init_Gui()
	with open("data.txt","w") as file:
	    file.write('')
	initialized = True

def clock():
	string=""
	time_monitor= ["00","01","02","03","04","05","06","07","08","09","10","12","13","14",
			"15","16","17","18","19","20","21","22","23","24","25","26","27","28",
			"29","30","31","32","33","34","35","36","37","38","39","40","41","42",
			"43","44","45","46","47","48","49","50","51","52","53","54","55","56",
			"57","58","59"]
	s,m,h=0,0,0
	while 1:
		string=time_monitor[h]+":"+time_monitor[m]+":"+time_monitor[s]
		label = Label(text=string,fg='white',bg='#212121', font=('Helvetica', 30))
		label.place(x=640, y=140)
		time.sleep(1.0)
		if s>=58 and not m>=58:
			s=0
			m+=1
		elif m>=58 and s>=58:
			m=0
			s=0
			h+=1
		else:
			s+=1

fig = Figure(figsize=(7,5),dpi=80,facecolor='#3B3B3B')

ax = fig.add_subplot(111)

ax.set_xlabel("time (s)")
ax.set_ylabel("emission (kg.CO₂eq)")
ax.grid()
graph = FigureCanvasTkAgg(fig, master=gui)
graph.get_tk_widget().place(x=30,y=110)

def data_points():
	f = open("data.txt", "r")
	data = f.readlines()
	f.close()
	if (data != ""):
		l = []
		for i in range(len(data)):
			x= float(data[i].rstrip("\n"))
			x = "{:.6f}".format(float(x))
			l.append(x)
		return l

def plotter():
	while 1:
		ax.cla()
		ax.grid()
		dpts = data_points()
		ax.plot(dpts, marker='', color='green')
		graph.draw()
		time.sleep(1.0)

def emission_fun():
	i,co2=0,0
	tracker = EmissionsTracker()
	while 1:
		tracker.start()
		tracker.stop()
		packets = psutil.net_io_counters()
		bytes_sent = packets[0]
		bytes_received = packets[1]
		total_bytes = bytes_sent + bytes_received

		power = open("total_power_draw.txt","r")
		consumption = power.read()
		consumption = float(consumption)+total_bytes * 1.52E-10
		power.close()

		w_emissions_display = Canvas(gui, width=378, height=60, highlightbackground="#3B3B3B", bg='#212121')
		w_emissions_display.place(x=630, y=245)
		emission_label = Label(fg='white',bg='#212121', text = str(consumption*0.055),font=('Helvetica', 20))
		emission_label.place(x=640, y=255)
		w_cost_display = Canvas(gui, width=378, height=60, highlightbackground="#3B3B3B", bg='#212121')
		w_cost_display.place(x=630, y=355)
		cost_label = Label(fg='white',bg='#212121',text = str(float(consumption)*0.1740),font=('Helvetica', 20))
		cost_label.place(x=640, y=365)

		with open("data.txt","a") as file:
			file.write(str(consumption*0.055-co2)+'\n')
		co2=consumption*0.055
		i+=1
		time.sleep(1.0)

threading.Thread(target = clock,daemon = True).start()
threading.Thread(target = emission_fun,daemon = True).start()
threading.Thread(target=plotter,daemon=True).start()

gui.mainloop()
