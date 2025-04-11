import requests
import time
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

def getweather(canvas):
    city = textfield.get()
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + city +"&appid=75623c2594f55bcc8d987fb0f841b528"
    data = requests.get(url).json()
    temperature=int(data['main']['temp'] -273.15)
    condition = data['weather'][0]['main']
    cond_icon = data['weather'][0]['icon']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    output = condition +  "\n" + str(temperature) + "°C"
    output2 ="Humidity: " +str(humidity) +"\n" + "Wind Speed: " +str(wind_speed)
    

    icon_url = f"http://openweathermap.org/img/wn/{cond_icon}@2x.png"
    response = requests.get(icon_url)
    icon_data = response.content
    icon_image = Image.open(BytesIO(icon_data))
    icon_photo = ImageTk.PhotoImage(icon_image)

    icon_label.config(image=icon_photo)
    icon_label.image = icon_photo

    label1.config(text = output)
    label2.config(text = output2)

canvas = tk.Tk()
canvas.geometry("900x700")
canvas.title("Khadijat Weather App")
image = Image.open("bg.jpg")
resized_image = image.resize((900, 700), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(resized_image)
canva = tk.Canvas(canvas, width=900, height=700)
canva.pack(fill="both", expand=True)
canva.create_image(0, 0, image=photo, anchor='nw')

#canva.image = photo

f = ("poppins", 15, "bold")
t = ("poppins", 30, "bold")

textfield =tk.Entry(canvas, justify= 'center', font = t)
canva.create_window(450, 50, window=textfield)
textfield.focus()
textfield.bind('<Return>', getweather)

label1 = tk.Label(canva, font = t, bg= "skyblue" )
canva.create_window(450, 260, window=label1)
label2 = tk.Label(canvas, font= f, bg="skyblue")
canva.create_window(450, 350, window=label2)

icon_label = tk.Label(canvas, bg="skyblue")
canva.create_window(450, 150, window=icon_label)

canvas.mainloop()