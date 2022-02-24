import tkinter as tk
import requests
from PIL import Image, ImageTk
import mysql.connector

########### GET INFORMATION ###########

# Mysql Info
HOST = "localhost"
USER = "root"
PASSWORD = "@@root123"
DATABASE = "weather"


def format_response(weather_json):
    try:
        city = weather_json['name']
        conditions = weather_json['weather'][0]['description']
        temp = str(weather_json['main']['temp']) +  '°F'
        humidity = str(weather_json['main']['humidity']) + '%'
        wind_speed = str(weather_json['wind']['speed']) + 'm/s'
        final_str = 'City: %s \nConditions: %s \nTemperature: %s \nHumidity: %s \nWind Speed : %s' % (city, conditions, temp, humidity, wind_speed)
    except:
        final_str = 'There was a problem retrieving that \ninformation'
    add_record(city, conditions, temp[:-2], humidity[:-1], wind_speed[:-3])
    return final_str


def get_weather(city):
    weather_key = 'edffd1bf975a74d5d10e58c5ac8be2d3'
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': 'edffd1bf975a74d5d10e58c5ac8be2d3', 'q': city, 'units':'imperial'}
    response = requests.get(url, params=params)
    print(response.json())
    weather_json = response.json()

    results['text'] = format_response(response.json())

    # Open weather icon
    icon_name = weather_json['weather'][0]['icon']
    size = int(lower_frame.winfo_height()*0.25)
    img = ImageTk.PhotoImage(Image.open('./img/'+icon_name+'.png').resize((size, size)))
    weather_icon.delete("all")
    weather_icon.create_image(0,0, anchor='nw', image=img)
    weather_icon.image = img

def add_record(city, conditions, temp, humidity, wind_speed):
    print(city, conditions, temp, humidity, wind_speed)
    dbase = mysql.connector.connect(host="localhost",user=USER,passwd=PASSWORD,database=DATABASE)
    db = dbase.cursor()

    db.execute("use weather;")
    db.execute(f"INSERT INTO weather_data VALUES('{city}', '{conditions}', {temp}, {humidity}, {wind_speed}, now())")
    dbase.commit()
    dbase.close()
    
########### PAST RECORDS ###########

def past_records():
    new = tk.Tk()
    new.minsize(600, 200)
    new.title('Past Records')
    #fr = tk.frame(new)
    #fr.place(relx=0.02, rely=0.02, relheight=0.96, relwidth=0.96)

    dbase = mysql.connector.connect(host="localhost",user=USER,passwd=PASSWORD,database=DATABASE)
    db = dbase.cursor()
    db.execute("SELECT * FROM weather_data")
    records=db.fetchall()
    print(records)
    
    l = ['CITY', 'CONDITIONS', 'TEMP', 'HUMIDITY', 'WIND SPEED', 'RECORDED AT']
    for i in range(len(l)):
        if i==5:
            tk.Label(new,font=('Courier', 14, 'bold'),bg='#8ecae6',text=l[i],width=20).grid(row=0,column=i,pady=10, padx=3)
        tk.Label(new,font=('Courier', 14, 'bold'),bg='#8ecae6',text=l[i],width=15).grid(row=0,column=i,pady=10, padx=3)
    i=1
    for record in records:
        tk.Label(new,font=('Courier', 12),bg='#8ecae6',text=record[0],width=15).grid(row=i+1,column=0,pady=10)
        tk.Label(new,font=('Courier', 12),bg='#8ecae6',text=record[1],width=15).grid(row=i+1,column=1,pady=10)
        tk.Label(new,font=('Courier', 12),bg='#8ecae6',text=record[2],width=15).grid(row=i+1,column=2,pady=10)
        tk.Label(new,font=('Courier', 12),bg='#8ecae6',text=record[3],width=15).grid(row=i+1,column=3,pady=10)
        tk.Label(new,font=('Courier', 12),bg='#8ecae6', text=record[4], width=15).grid(row=i+1, column=4,pady=10)
        tk.Label(new, font=('Courier', 12),bg='#8ecae6',text=record[5], width=20).grid(row=i+1, column=5,pady=10)
        i+=1
    exit_button = tk.Button(new, text='EXIT', font=('Courier', 12, 'bold'), command=new.destroy)
    exit_button.grid(row=i+1, columnspan=6, sticky=tk.NSEW)

    new.mainloop()


########### TKINTER ###########

app = tk.Tk()
app.title('Weather App')
HEIGHT = 500
WIDTH = 600
app.resizable(width=False, height=False)

C = tk.Canvas(app, height=HEIGHT, width=WIDTH)
background_image= tk.PhotoImage(file='./land.png')
background_label = tk.Label(app, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

C.pack()

frame = tk.Frame(app,  bg='#ff7438', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

textbox = tk.Entry(frame, font =('Courier', 12), borderwidth=10, relief='flat')
textbox.place(relwidth=0.65, relheight=1)
textbox.insert(-1, 'Enter City Name')

submit = tk.Button(frame, text='Get Weather', font =('Courier', 12, 'bold'), command=lambda: get_weather(textbox.get()))
submit.place(relx=0.7, relheight=1, relwidth=0.3)

lower_frame = tk.Frame(app, bg='#ff7438', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.5, anchor='n')

bg_color = 'white'
results = tk.Label(lower_frame, anchor='nw', justify='left', bd=4)
results.config(font=('Courier', 12), bg=bg_color)
results.place(relwidth=1, relheight=1)

weather_icon = tk.Canvas(results, bg=bg_color, bd=0, highlightthickness=0)
weather_icon.place(relx=.75, rely=0, relwidth=1, relheight=0.5)

past = tk.Button(app, text='Past Records', font =('Courier', 12, 'bold'), command=lambda: past_records())
past.place(rely=0.79, relx=0.125, relheight=0.07, relwidth=0.75)
exit_button = tk.Button(app, text='Exit', font=('Courier', 12, 'bold'), command=app.destroy)
exit_button.place(rely=0.87, relx=0.125, relheight=0.07, relwidth=0.75)

app.mainloop()