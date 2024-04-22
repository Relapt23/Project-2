from tkinter import *
from tkinter import ttk
import random
from math import *
import asyncio
from time import *
from async_tkinter_loop import async_mainloop, async_handler
import matplotlib.pyplot as plt
data_base = {}


class SensorInfo:
    def __init__(self,name,val,delta_min,delta_max):
        self.name=name
        self.val=val
        self.delta_min=delta_min
        self.delta_max=delta_max


def ran(min, max,t):
    res = min + (((sin(t/150)+1)/2) * (max - min))
    result = round(random.uniform(res*0.95, res*1.05),2) 
    return result


def update_items(table,sensors):
    table.delete(*table.get_children())
    for sensor in sensors:
        name = sensor.name
        val = sensor.val
        delta = str(sensor.delta_min)+'-'+str(sensor.delta_max)
        if int(sensor.val)<int(sensor.delta_min) or int(sensor.val)>int(sensor.delta_max):
            table.insert('', 'end', values=[name,val,delta], tags = ('oddrow',))
        else:
            table.insert('', 'end', values=[name,val,delta])

# формирование графика при выделении датчика
def item_selected(event):
    sensor = ""
    for selected_items in table.selection():
        item = table.item(selected_items)
        sensor = item["values"][0]
        if sensor in data_base.keys():
            y_val=data_base[sensor]
            fig = plt.figure(figsize=(8,4))
            ax = fig.add_subplot(111)
            ax.set(title=sensor, xlim=[0, 30], ylim=[min(y_val),max(y_val)], ylabel='Значение', xlabel='Дни')
            y=data_base[sensor]
            x=range(1,len(y)+1)
            plt.plot(x,y)
            plt.savefig(fname='graf4.png')


root= Tk()
root.title('Climat-control system')
root.geometry("1250x500")
icon =PhotoImage(file="save_nature.png")
root.iconphoto(False,icon)
root.configure(background='white')



# Текстовые поля
Label_right = ttk.Label(text='Оценка показателей', font=('Arial', 14),background='white')
Label_right.place(x= 150, y=25)
Label_left = ttk.Label(text='Текущее состояние датчиков', font=('Arial', 14),background='white')
Label_left.place(x=770, y= 25)
# блок с рекомендациями
frame_right = Frame(borderwidth=1, relief=SOLID, height= 585, width=650,background='white')
reco_info = ttk.Label(frame_right, text='Рекомендация:', font=('Arial', 14),background='white')
reco_info.place(x=15, y= 10)
frame_right.place( x= 10, y= 70)
frame_recommend=Frame(frame_right, borderwidth= 1, relief='solid', height=150, width=600,background='white')

# ссылка на переменную с изменяемыми рекомендациями
reco_label = ttk.Label(frame_recommend, text='Снизить интенсивность полива', font=('Arial', 12),background='white')
reco_label.place(x= 10, y= 10)
frame_recommend.place( x= 10, y = 40)

# блок с обоснованием рекомендации
reco_info_label = ttk.Label(frame_right, text='Обоснования рекомендации:', font=('Arial', 14),background='white')
reco_info_label.place(x=15, y= 200)
frame_reco_info =Frame(frame_right, borderwidth=1, relief=SOLID, height=350, width=600,background='white')
frame_reco_info.place(x=10, y= 230)

# создание таблицы
columns = ('name', 'val','delta')
table = ttk.Treeview(columns=columns, show='headings',selectmode='extended')
table.tag_configure('oddrow', background='orange')
table.place(x=670,y= 70,)
table.column('#1', stretch=YES)
table.column('#2', stretch=YES, anchor='center')
table.column('#3', stretch=YES, anchor='center')
table.heading('name', text='Показатель')
table.heading('val', text='Значение')
table.heading('delta', text='Диапазон нормы')
style = ttk.Style()
style.theme_use('classic')


# Прорисовка графика
graph = PhotoImage(file="graf4.png")
graph_label=ttk.Label(image=graph)
graph_label.place(x=670, y=320)
# заполнение таблицы показаний датчиков
async def update_val():
    t = 0
    while True:
        sensors = [
            SensorInfo('Влажность воздуха', ran(17,40,t), 17,40), 
            SensorInfo('Влажность почвы', ran(50,55,t), 50,55), 
            SensorInfo('Температура воздуха', ran(4, 27, t), 4,27), 
            SensorInfo('Температура раствора', ran(0,27,t), 0,27), 
            SensorInfo('Давление', ran(750,780,t), 750,780), 
            SensorInfo('Уровень раствора', ran(13,15,t), 13,15), 
            SensorInfo('Кислотность раствора', ran(75,80,t),75,80), 
            SensorInfo('Содержание ионов', ran(30,35,t),30,35), 
            SensorInfo('Освещенность', ran(30,67,t),30,67),
        ]
        update_items(table,sensors)
        await asyncio.sleep(3)
        # Построение графика
        for i in range(len(sensors)):
            if sensors[i].name not in data_base.keys():
                    data_base[sensors[i].name] = [sensors[i].val]
            else:
                data_base[sensors[i].name].append(sensors[i].val)
            if len(data_base[sensors[i].name]) > 30:
                data_base[sensors[i].name].pop(0)
            # Обновление графика
            graph = PhotoImage(file="graf4.png")
            graph_label=ttk.Label(image=graph)
            graph_label.place(x=670, y=320)
        t += 3
table.bind("<<TreeviewSelect>>", item_selected)
graph_label.destroy()
async_handler(update_val)()


async_mainloop(root)

