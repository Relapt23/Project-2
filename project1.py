from tkinter import *
from tkinter import ttk
import random
from math import *
import asyncio
from time import *
from async_tkinter_loop import async_mainloop, async_handler


def ran(min, max,t):
    res = min + (((sin(t/150)+1)/2) * (max - min))
    result = round(random.uniform(res*0.95, res*1.05),2) 
    return result


def update_items(table,sensors):
    table.delete(*table.get_children())
    for sensor in sensors:
        name = sensor[0]
        val = sensor[1]
        delta = str(sensor[2])+'-'+str(sensor[3])
        if int(sensor[1])<int(sensor[2]) or int(sensor[1])>int(sensor[3]):
            table.insert('', 'end', values=[name,val,delta], tags = ('oddrow',))
        else:
            table.insert('', 'end', values=[name,val,delta])
    


root= Tk()
root.title('Climat-control system')
root.geometry("300x250+400+250")
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


# заполнение таблицы показаний датчиков
async def update_val():
    t = 0
    while True:
        sensors = [
            ('Влажность воздуха', ran(17,40,t), 17,55), 
            ('Влажность почвы', ran(50,55,t), 50,55), 
            ('Температура воздуха', ran(4, 27, t), 4,27), 
            ('Температура раствора', ran(0,27,t), 0,27), 
            ('Давление', ran(750,780,t), 750,780), 
            ('Уровень раствора', ran(13,15,t), 13,15), 
            ('Кислотность раствора', ran(75,80,t),75,80), 
            ('Содержание ионов', ran(30,35,t), 30,35), 
            ('Освещенность', ran(30,67,t), 30,67),
        ]
        update_items(table,sensors)
        await asyncio.sleep(3)
        t += 3

async_handler(update_val)()
async_mainloop(root)