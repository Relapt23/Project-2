from tkinter import *
from tkinter import ttk
import random
from math import *
import asyncio
from time import *
from async_tkinter_loop import async_mainloop, async_handler
import matplotlib.pyplot as plt
from gpt import perform_request_chatGPT 
data_base = {} 
deviation_counter = {}
recommendations = {
    'Увеличить:': set(),
    'Снизить:': set(),
    'Датчики, требующие калибровки:': set()
}
new_delta = {
    'Влажность воздуха': [40,60], 
    'Влажность почвы':[90,95],
    'Температура воздуха':[22,24], 
    'Температура раствора':[15,19], 
    'Давление':[0.95,1.05], 
    'Уровень раствора':[13,15], 
    'Кислотность раствора':[5.1,5.9], 
    'Содержание ионов':[900,1100], 
    'Освещенность':[100,150],
}


class SensorInfo:
    def __init__(self,name,val,delta_min,delta_max,si):
        self.name=name
        self.val=val
        self.delta_min=delta_min
        self.delta_max=delta_max
        self.si=si

hardcoded_chart = {
    'Влажность воздуха': {"currentIteration": 0, "values": [40,40.1, 40.3,40.5,40.4,40.3,40.8,42,43.5,45,39,38,38.5,39.1,41,41.6,43,45,46.5,48,48.3,47,48,50,52,55,57,57.5,60.2,61,62,61.7,60,3,59.9,59.3,57,56.5,55,55.1,55.2,57,55,53,52.4,50], }, 
    'Влажность почвы': {"currentIteration": 0, "values": [89, 90.1, 90.2, 90.3, 90.3, 90.5, 91, 90.6, 90.9, 89.7, 89.9, 90.0, 91.1, 91.1, 91, 89.9, 89, 88.5, 88, 89, 91.8, 91.9, 92.0, 92.0, 92.3, 92, 92.3, 92.4, 92.5, 92.6, 92.7, 92.5, 92.7, 93.0, 93.0, 93.1, 93.2, 93.3, 93.4, 93.5, 93.6, 93.7, 93.8, 93.9, 94.0], },
    'Температура воздуха': {"currentIteration": 0, "values": [22.0, 22.1, 22.2, 22.3, 22.4, 22.5, 22.6, 22.7, 22.8, 22.9, 23.0, 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7, 23.8, 23.9, 24.0, 23.9, 23.8, 23.7, 23.6, 23.5, 23.4, 23.3, 23.2, 23.1, 23.0, 22.9, 22.8, 22.7, 22.6, 22.5, 22.4, 22.3, 22.2, 22.1, 22.0, 22.1, 22.2, 22.3, 22.4], }, 
    'Температура раствора': {"currentIteration": 0, "values": [15.0, 15.1, 15.0, 14, 15, 15.1, 15.3, 15.7, 15.8, 15.9, 16.0, 16.4, 16.2, 16.3, 16.4, 16.9, 17.4, 17.8, 18.6, 19.1, 19.4, 20, 21.5, 21, 20.5, 20, 19.5, 19, 18.6, 18.9, 18.4, 18.3, 18.2, 18.1, 18.3, 18.5, 18.6, 18.3, 18.4, 18.2, 19.1, 19, 18.8, 18.7, 18.6], }, 
    'Давление': {"currentIteration": 0, "values": [1,1,1,1,1,1,1,1,1,1,1,1.02,1.03,1.02,1.03,1.04,1.05,1.04,1.02,1.01,1,1,1,1,1,1,1.01,1.03,1.02,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], }, 
    'Уровень раствора': {"currentIteration": 0, "values": [13.0, 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 13.7, 13.8, 13.9, 14.0, 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7, 14.8, 14.9, 15.0, 14.9, 14.8, 14.7, 14.6, 14.5, 14.4, 14.3, 14.2, 14.1, 14.0, 13.9, 13.8, 13.7, 13.6, 13.5, 13.4, 13.3, 13.2, 13.1, 13.0, 13.1, 13.2, 13.3, 13.4], }, 
    'Кислотность раствора': {"currentIteration": 0, "values": [5.1, 5.2, 5.3, 5.3, 5.5, 5.3, 5.2, 5.1, 5.0, 4.9, 5.1, 5.2, 5.1, 5.0, 4.9, 4.8, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.3, 5.2, 5.3, 5.2, 5.1, 5.0, 5.0, 5.1, 5.2, 5.4, 5.3, 5.5, 5.6, 5.7, 5.9, 6, 5.5, 5.6, 5.7, 5.8, 5.9, 5.9, 5.8], }, 
    'Содержание ионов': {"currentIteration": 0, "values": [900, 905, 910, 915, 910, 890, 900, 910, 940, 930, 950, 950, 960, 965, 970, 960, 940, 985, 990, 995, 1100, 1105, 1110, 1015, 1020, 1000, 1030, 1070, 1040, 1050, 1050, 1040, 1000, 995, 1010, 1075, 1080, 1085, 1090, 1095, 1100, 905, 910, 915, 920], }, 
    # 'Освещенность': {"currentIteration": 0, "values": [1,2,3,4,5,6,6], },
}


def ran(min, max,t):
    res = min + (((sin(t/150)+1)/2) * (max - min))
    result = round(random.uniform(res*0.95, res*1.05),2) 
    return result

def get_hardcoded_chart(key):
    dict = hardcoded_chart[key]
    current = dict["currentIteration"]
    result = dict["values"][current]
    dict["currentIteration"]+=1
    return result

def update_items(table,sensors):
    table.delete(*table.get_children())
    for sensor in sensors:
        name = sensor.name
        val = sensor.val
        delta = str(sensor.delta_min)+'-'+str(sensor.delta_max)+str(sensor.si)
        if float(sensor.val)<float(sensor.delta_min) or float(sensor.val)>float(sensor.delta_max):
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
            fig = plt.figure(figsize=(6,4))
            ax = fig.add_subplot(111)
            ax.set(title=sensor, xlim=[0, 30], ylim=[min(y_val),max(y_val)], ylabel='Значение', xlabel='Дни')
            y=data_base[sensor]
            x=range(1,len(y)+1)
            plt.plot(x,y)
            plt.savefig(fname='graf4.png')


def click():
    window = Tk()
    window.title("Изменение диапазона")
    window.geometry("200x100")
    sensors = [
            'Влажность воздуха', 
            'Влажность почвы',
            'Температура воздуха', 
            'Температура раствора', 
            'Давление', 
            'Уровень раствора', 
            'Кислотность раствора', 
            'Содержание ионов', 
            'Освещенность',
    ]
    def enter_new_delta():
        new_delta[combobox.get()] = [int(entry_min.get()),int(entry_max.get())]


    combobox = ttk.Combobox(window,values=sensors,font=('Arial', 12),state='readonly')
    combobox.pack(fill=X, ipadx=6,ipady=6)
    entry_min = ttk.Entry(window,width=2)
    entry_min.place(x=120,y=40)
    entry_max = ttk.Entry(window,width=2)
    entry_max.place(x=150,y=40)
    get_button = ttk.Button(window, text="Выбор", command=enter_new_delta)
    get_button.place(anchor='center',x=100,y=80)
    label = ttk.Label(window,text='Новый диапазон:', font=('Arial', 10))
    label.place(x=10,y=40)
    tire = ttk.Label(window,text=' - ', font=('Arial', 10))
    tire.place(x=135,y=40)


def click_GPT():
    res = perform_request_chatGPT(data_base,entry_plan,entry_fact)
    text55.insert("1.0", res.content)

def click2():
    if float(entry_plan.get()) > float(entry_fact.get()):
        click_GPT()
        

root= Tk()
root.title('Climat-control system')
root.geometry("1250x800")
icon =PhotoImage(file="save_nature.png")
root.iconphoto(False,icon)
root.configure(background='white')	

# Текстовые поля
Label_right = ttk.Label(text='Оценка показателей', font=('Arial', 14),background='white')
Label_right.place(x= 150, y=25)
Label_left = ttk.Label(text='Текущее состояние датчиков', font=('Arial', 14),background='white')
Label_left.place(x=770, y= 25)
# блок с рекомендациями
frame_right = Frame(borderwidth=1, relief=SOLID, height= 750, width=650,background='white')
reco_info = ttk.Label(frame_right, text='Рекомендация:', font=('Arial', 14),background='white')
reco_info.place(x=15, y= 10)
frame_right.place( x= 10, y= 70)
frame_recommend=Frame(frame_right, borderwidth= 1, relief='solid', height=150, width=600,background='white')
# Поля для заполнения план/факта урожая
Label_plan_fact = ttk.Label(text='Заполните ожидаемый и полученный урожай:', font=('Arial', 12), background='white')
Label_plan_fact.place(x=700,y=350)
entry_plan = ttk.Entry(width=3)
entry_plan.place(x=1050,y=350)
entry_fact = ttk.Entry(width=3)
entry_fact.place(x=1100,y=350)
Plan_fact_button = ttk.Button(text="Подтвердить", command=click2)
Plan_fact_button.place(x=950, y=375)
# ссылка на переменную с изменяемыми рекомендациями
reco_label = ttk.Label(frame_recommend, text='', font=('Arial', 12),background='white')   
reco_label.place(x= 10, y= 10)
frame_recommend.place( x= 10, y = 40)

# блок с обоснованием рекомендации
reco_info_label = ttk.Label(frame_right, text='Обоснования рекомендации:', font=('Arial', 14),background='white')
reco_info_label.place(x=15, y= 200)
frame_reco_info =Frame(frame_right, borderwidth=1, relief=SOLID, height=500, width=600,background='white')
frame_reco_info.place(x=10, y= 230)

# создание таблицыq
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
# Создание окна изменения диапазона датчиков
btn = ttk.Button(text='Изменение диапазона',command=click)
btn.place(x=800,y=300)
# Создание кпопки для запроса к ChatGPT
ChatGPT_btn = ttk.Button(text='Запрос рекомендаций', command=click_GPT)
ChatGPT_btn.place(x=1000,y=300)
text55 = Text(frame_reco_info,font=('Arial', 10),background='white',wrap='word', height=30,width=83)
text55.place(x=10, y=10)

# заполнение таблицы показаний датчиков
async def update_val():
    # Прорисовка графика
    graph = PhotoImage(file="graf4.png")
    graph_label=ttk.Label(image=graph)
    t = 0
    while True:
        sensors = [
            SensorInfo('Влажность воздуха', get_hardcoded_chart('Влажность воздуха'), new_delta['Влажность воздуха'][0],new_delta['Влажность воздуха'][1],',%'), 
            SensorInfo('Влажность почвы', get_hardcoded_chart('Влажность почвы'), new_delta['Влажность почвы'][0],new_delta['Влажность почвы'][1],',%'), 
            SensorInfo('Температура воздуха', get_hardcoded_chart('Температура воздуха'), new_delta['Температура воздуха'][0],new_delta['Температура воздуха'][1],',℃'), 
            SensorInfo('Температура раствора', get_hardcoded_chart('Температура раствора'), new_delta['Температура раствора'][0],new_delta['Температура раствора'][1],',℃'), 
            SensorInfo('Давление', get_hardcoded_chart('Давление'), new_delta['Давление'][0],new_delta['Давление'][1],',атм'), 
            SensorInfo('Уровень раствора', get_hardcoded_chart('Уровень раствора'), new_delta['Уровень раствора'][0],new_delta['Уровень раствора'][1],',см'), 
            SensorInfo('Кислотность раствора', get_hardcoded_chart('Кислотность раствора'), new_delta['Кислотность раствора'][0],new_delta['Кислотность раствора'][1],',pH'), 
            SensorInfo('Содержание ионов', get_hardcoded_chart('Содержание ионов'), new_delta['Содержание ионов'][0],new_delta['Содержание ионов'][1],',шт'), 
            SensorInfo('Освещенность', ran(new_delta['Освещенность'][0],new_delta['Освещенность'][1],t), new_delta['Освещенность'][0],new_delta['Освещенность'][1],',лк'),
        ]
        update_items(table,sensors)
        await asyncio.sleep(3)
        # Построение графика
        for sensor in sensors:
            if sensor.name not in data_base.keys():
                data_base[sensor.name] = [sensor.val]
                deviation_counter[sensor.name]=[0,0,0]
            data_base[sensor.name].append(sensor.val)
            if sensor.val < sensor.delta_min:
                deviation_counter[sensor.name][0] += 1
            elif sensor.val > sensor.delta_max:
                deviation_counter[sensor.name][1] += 1
            if sensor.delta_min<= sensor.val<= sensor.delta_max:
                deviation_counter[sensor.name][2] += 1
            else:
                deviation_counter[sensor.name][2] = 0

            if len(data_base[sensor.name]) > 30:
                data_base[sensor.name].pop(0)
        for name in deviation_counter.keys():
            if deviation_counter[name][0] > 5:
                recommendations['Увеличить:'].add(name)
                if deviation_counter[name][2] >=3:
                    recommendations['Увеличить:'].remove(name)   
                    deviation_counter[name][0] = 0   
            elif deviation_counter[name][1] > 5:
                recommendations['Снизить:'].add(name)
                if deviation_counter[name][2] >=3:
                    recommendations['Снизить:'].remove(name)
                    deviation_counter[name][1] = 0
            elif deviation_counter[name][0] > 5 and deviation_counter[name][1] > 5:
                recommendations['Датчики, требующие калибровки:'].add(name)
                recommendations['Увеличить:'].remove(name)
                recommendations['Снизить:'].remove(name)
                     
        result = ''
        for key, values in recommendations.items():
            result += str(key) + '\n'
            for value in values:
                result += '- ' + str(value) + '\n'
        reco_label.config(text=result)
            # Обновление графика
        graph_label.destroy()
        graph = PhotoImage(file="graf4.png")
        graph_label=ttk.Label(image=graph)
        graph_label.place(x=670, y=415)
        t += 3
table.bind("<<TreeviewSelect>>", item_selected)
async_handler(update_val)()
async_mainloop(root)

