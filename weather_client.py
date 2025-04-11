import requests  # For sending HTTP requests to access weather data from the API
import time  # For adding delays or handling time-based functionality

def get_ordinal(n):     #This will be used in the print statement of multiple cities weather
    if 10 <= n % 100 <= 20:     #checks if the last two digits is between 10 and 20 then assign 'th' as suffix
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")  #automatically add suffix to 1,2,3 and then add th to any other number outside that
    return f"{n}{suffix}"       #returns something like 1st if n=1

print("Welcome to Khadijat's Weather App")      #Yeah, that's my app
while True:     #This breaks when the decision == "quit"
    choice = int(input("-------------------------------------------\nWhat would like to do?\n1. Get weather condition for a city?\n2.Get weather conditions of multiple cities.\n3. Get weather forecasts for the next 5 days \n1, 2  or 3? "))
    if choice ==1:
        city = input("-------------------------------------------\nEnter a city name: ")
        url = "https://api.openweathermap.org/data/2.5/weather?q=" + city +"&{api-key}"
        data = requests.get(url).json()     #saving the data as json file
        temperature=int(data['main']['temp'] -273.15)       #converting the fahrenheit temperature to Celsius
        condition = data['weather'][0]['main']
        cond_icon = data['weather'][0]['icon']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        output1 ="The weather condition of " + city + " is given below:" + "\n" + condition +  "\n" + "Temperature: " + str(temperature) + "°C" +"\n"+ "Humidity: " +str(humidity) +"\n" + "Wind Speed: " +str(wind_speed)
        print(output1 + "\n-------------------------------------------")
    elif choice==2:
        num = int(input("How many cities do you wish to get weather conditions for? "))     #number of cities to get data for
        count = 0       #This will be incremented as user enter the names of the cities and ends when it equals num
        cities =[]      #This is used to save the cities the user want to get their information
        while count <  num:
            ord = get_ordinal(count + 1)       #calling the get_ordinal function to get order of count
            city = input("Enter the "+ ord +" city name: ")
            count += 1      #increase the number of cities entered until it equal num
            cities.append(city)     #add the city entered to the cities list
        for city in cities:     #iterating over each city, to get weather data
            url = "https://api.openweathermap.org/data/2.5/weather?q=" + city +"&{api-key}"
            data = requests.get(url).json()
            temperature=int(data['main']['temp'] -273.15)
            condition = data['weather'][0]['main']
            cond_icon = data['weather'][0]['icon']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            output2 ="The weather condition of " + city + " is given below:" + "\n" + condition +  "\n" + "Temperature: " + str(temperature) + "°C" +"\n"+ "Humidity: " +str(humidity) +"\n" + "Wind Speed: " +str(wind_speed)
            print(output2 + "\n-------------------------------------------")      #This prints information for each city
    elif choice ==3:        #for 5 day forecast
        city = input("-------------------------------------------\nEnter a city name: ")
        url ="https://api.openweathermap.org/data/2.5/forecast?q=" + city+ "&{api-key}"
        data = requests.get(url).json()
        index = [0, 1, 2, 3, 4]     #This is for each day in the 'list' in the API data. 
        print("The weather condition for "+city+" for the next 5 days are: ")
        for i in index:
            temperature=int(data['list'][i]['main']['temp'] -273.15)
            condition = data['list'][i]['weather'][0]['main']
            humidity = data['list'][i]['main']['humidity']
            wind_speed = data['list'][i]['wind']['speed']
            output1 = condition +  "\n" + "Temperature: " + str(temperature) + "°C" +"\n"+ "Humidity: " +str(humidity) +"\n" + "Wind Speed: " +str(wind_speed)
            print(output1 + "\n-------------------------------------------")
    else:
        print("You haven't selected a valid option")        # for options different from 1,2 or 3
    
    '''
    I want to ask the user to choose between selection and quit if they enter options different from 1,2,3 in choice
    if they enter seletion, it will break and go back to choice
    if they enter quit, it will exit
    if they enter anything else, it will repeat 'decision'
    '''
    while True:
        decision = input("Do you wish to make another selection or quit? (Type 'selection' to continue or 'quit' to exit): ").strip().lower()
        
        if decision == "selection":
            break  # This should go back to the main loop
        elif decision == "quit":
            print("Have a nice day ☀️")
            exit() 
        else:
            print("You haven't selected a valid option.")
