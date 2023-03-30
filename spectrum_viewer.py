import seabreeze #Paqueteria para lectura de datos
seabreeze.use('cseabreeze')
from seabreeze.spectrometers import Spectrometer
import seatease.spectrometers as s #paqueteria para la simulacion
import numpy as np #Operaciones matemáticas
import tkinter as tk#Interfaz de Usuario
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt #Graficación
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure

running = True
cont=0
def electric_noise():
    ruido = np.load('datos.npy')
    x=ruido[0,:]
    y=ruido[1,:]
    return y


def time_selection():
    try:
        num=int(time_entry.get())
        mul=u_time.get()
        time_unit=['mus','ms','s','']
        time_exp=[1,10**3,10**6,0]
        mult=int(time_exp[time_unit.index(mul)])
        if num*mult>=3000:
            time_int=num*mult
            try:
                scans=int(scAv_entry.get())
                if scans<0:
                    scans=5
            except:
                scans=5
            try:
                w_start=int(lambda_inf.get())
                w_end =int(lambda_sup.get())
                if w_start<w_end:
                    x_r=np.round(x)
                    x_r=x_r.tolist()
                    st=x_r.index(w_start)
                    en=x_r.index(w_end)
            except:
                st=0
                en=-1
        show_spectrum(st,en,scans,time_int)
    except:
        pass


def read_selection():
    try:
        w_start=int(lambda_inf.get())
        w_end =int(lambda_sup.get())
        if w_start<w_end:
                    x_r=np.round(x)
                    x_r=x_r.tolist()
                    st=x_r.index(w_start)
                    en=x_r.index(w_end)
                    try:
                        scans=int(scAv_entry.get())
                        if scans<0:
                            scans=5
                    except:
                        scans=5
                    try:
                        num=int(time_entry.get())
                        mul=u_time.get()
                        time_unit=['mus','ms','s','']
                        time_exp=[1,10**3,10**6,0]
                        mult=int(time_exp[time_unit.index(mul)])
                        if num*mult>=3000:
                            time_int=num*mult
                        else:
                            time_int=3000
                    except:
                        time_int=3000
                    show_spectrum(st,en,scans,time_int)
    except:
        pass


def scans_av():
    try:
        scans=int(scAv_entry.get())
        if scans>0:
            try:
                w_start=int(lambda_inf.get())
                w_end =int(lambda_sup.get())
                if w_start<w_end:
                    x_r=np.round(x)
                    x_r=x_r.tolist()
                    st=x_r.index(w_start)
                    en=x_r.index(w_end)
            except:
                st=0
                en=-1
            try:
                num=int(time_entry.get())
                mul=u_time.get()
                time_unit=['mus','ms','s','']
                time_exp=[1,10**3,10**6,0]
                mult=int(time_exp[time_unit.index(mul)])
                if num*mult>=3000:
                    time_int=num*mult
                else:
                    time_int=3000
            except:
                time_int=3000    
            show_spectrum(st,en,scans,time_int)
    except:
        pass

# Define a function to start the loop
def on_start():
   global running
   running=True
   read_selection()
   scans_av()
   time_selection()

# Define a function to stop the loop
def on_stop():
     global running
     running=False

bgc='#D5F6FB'
bgc1='white'
fgc='gray'
font='Courier'
app = Tk()
app.title("Spectrum Viewer")
app.geometry('1140x700')
app.configure(bg=bgc)
try:
    spec=Spectrometer.from_first_available()
except:
    spec = s.Spectrometer.from_first_available()
activo=BooleanVar;st=IntVar;en=IntVar;scans=IntVar;time_int=IntVar;
x=spec.wavelengths();st=0;en=len(x); scans=5; time_int=3000;activo=False
def show_spectrum(st,en,scans,time_int):
    cont=0
    global running
    limit=10;
    while cont<limit and running:
        pausa=False;cscans=0
        while not pausa:    
            # Set integration time
            spec.integration_time_micros(time_int) # 10 ms
            # Print intensities
            x=spec.wavelengths()
            y=spec.intensities()
            x1=x[st:en]
            y1=y[st:en]
            y_prom=0
            if cscans==scans:
                y_prom=y_prom+y1
                pausa=True
            cscans+=1
        if cont==limit:
            running=False
            break
        cont=cont+1
        ax.clear()
        ax.plot(x1,y_prom/scans, color='blue')
        canvas1.draw( )
       
        


xmin=np.min(np.round(x))
xmax=np.max(np.round(x))
num=int((xmax-xmin)/100)+1
wvr=np.linspace(xmin,xmax,num=num)
wvrstr=[]
for i in range(len(wvr)):
    wvrstr.append(str(int(wvr[i])))


frm = tk.Frame(app)
frm.config(bg=bgc1)
fig= Figure(figsize=(10,7), dpi=80)
ax=fig.add_subplot(111)
canvas1 = FigureCanvasTkAgg(fig, master=frm)#frm)  # A tk.DrawingArea.


#Controles
control_frm = tk.Frame(app,width=500, height=670)
control_frm.config(bg=bgc1)
#Integration Time
inT_frm = tk.Frame(control_frm)
inT_frm.config(bg=bgc1)
#Title
inT_label=tk.Label(text="Integration Time",master=inT_frm)
inT_label.config(fg=fgc,    # Foreground
             bg=bgc1,   # Background
             font=(font,12))
#Time integration
time_entry = ttk.Entry(width=10,master=inT_frm)
time_entry.config(font=(font,11))
#Time unity
u_time= ttk.Combobox(
    state="readonly",
    values=['mus','ms','s'],
    width=5,
    master=inT_frm)
u_time.config(font=(font,11))
#Apply button
inTbtn_frm = tk.Frame(control_frm,width=500, height=670)
inTbtn_frm.config(bg=bgc1)
selectioninT = ttk.Button(text="Apply",master=inTbtn_frm,command=time_selection)
s = ttk.Style()
s.configure('.', font=('Helvetica', 11))


#Wavelength Range
wvr_frm = tk.Frame(control_frm)
wvr_frm.config(bg=bgc1)
#Title
wvr_label=tk.Label(text="Wavelength Range",master=wvr_frm)
wvr_label.config(fg=fgc,    # Foreground
             bg=bgc1,   # Background
             font=(font,12))
#Minimum value
lambda_inf= ttk.Combobox(
    state="readonly",
    values=wvrstr,
    width=5,
    master=wvr_frm)
lambda_inf.config(font=(font,11))
#Maximum value
lambda_sup=ttk.Combobox(
    state="readonly",
    values=wvrstr,
    width=5,
    master=wvr_frm)
lambda_sup.config(font=(font,11))
#Apply button
wvrbtn_frm = tk.Frame(control_frm,width=500, height=670)
wvrbtn_frm.config(bg=bgc1)
selectionwvr = ttk.Button(text="Apply",master=wvrbtn_frm,command=read_selection)


#Dark field
df_frm= tk.Frame(control_frm)
df_frm.config(bg=bgc1)
df_label=tk.Label(text="Dark Field",master=df_frm)
df_label.config(fg=fgc,    # Foreground
             bg=bgc1,   # Background
             font=(font,12))
df_checkbox = ttk.Checkbutton(text="Activate",master=df_frm)


#Scans per Average
scAv_frm= tk.Frame(control_frm)
scAv_frm.config(bg=bgc1)
scAv_label=tk.Label(text="Scans per Average",master=scAv_frm)
scAv_label.config(fg=fgc,    # Foreground
             bg=bgc1,   # Background
             font=(font,12))
scAv_entry = ttk.Entry(width=3,master=scAv_frm)
scAv_entry.config(font=(font,11))
selectionscAv = ttk.Button(text="Apply",master=scAv_frm,command=scans_av)


Spc_frm=tk.Frame(control_frm)
Spc_frm.config(bg=bgc1)
selectionSpc = ttk.Button(text="Save Spectrum",master=Spc_frm) #command=show_selection)

run_frm=tk.Frame(frm)
run_frm.config(bg=bgc1)
play_checkbox = ttk.Button(text="Play",master=run_frm,command=on_start)
pause_checkbox = ttk.Button(text="Pause",master=run_frm,command=on_stop)

control_frm.pack(side='left',padx=30,pady=10)
inT_frm.pack()
inT_label.pack(padx=10,pady=10)
time_entry.pack(side='left',padx=10,pady=10)
u_time.pack(side='right',padx=10,pady=10)
inTbtn_frm.pack(padx=10,pady=10)
selectioninT.pack()


wvr_frm.pack()
wvr_label.pack(padx=10,pady=10)
lambda_inf.pack(side='left',padx=10,pady=10)
lambda_sup.pack(side='right',padx=10,pady=10)
wvrbtn_frm.pack(padx=10,pady=10)
selectionwvr.pack()


df_frm.pack()
df_label.pack(side='left',padx=10,pady=10)
df_checkbox.pack(side='right',padx=10,pady=10)


scAv_frm.pack()
scAv_label.pack(padx=10,pady=10)
scAv_entry.pack(side='left',padx=10,pady=10)
selectionscAv.pack(side='right',padx=10,pady=10)


Spc_frm.pack()
selectionSpc.pack(side='right',padx=10,pady=10)
frm.pack(side='right',padx=30,pady=20)

canvas1.draw()  
canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#app.after(scans*time_int, show_spectrum(st,en,scans,time_int))
selectioninT = ttk.Button(text="Apply",master=inTbtn_frm) #command=show_selection)
run_frm.pack()
play_checkbox.pack(side='left',padx=5,pady=10)
pause_checkbox.pack(side='right',padx=10,pady=10)

app.mainloop()
