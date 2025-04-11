import pytest
import requests
from unittest.mock import patch


'''
I will test all the code. Since It will be difficult to test data that's updated each time
a call is made to the API, I will create a fake data for all the tests.
They will have similar information with the original data
'''

def test_single_city_weather(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: "London")     # a mock city, london  
    fake_response = {              # Defining the fake response from the API
        "main": {"temp": 295.15, "humidity": 60},
        "weather": [{"main": "Clear", "icon": "01d"}],
        "wind": {"speed": 5.2}
    }
    with patch('requests.get') as mock_get:         # using Patch requests.get to return the fake response
        mock_get.return_value.json.return_value = fake_response

        # Single city code
        city = input("-------------------------------------------\nEnter a city name: ")
        url = "https://api.openweathermap.org/data/2.5/weather?q=" + city +"&appid=75623c2594f55bcc8d987fb0f841b528"
        data = requests.get(url).json()
        temperature = int(data['main']['temp'] - 273.15)
        condition = data['weather'][0]['main']
        cond_icon = data['weather'][0]['icon']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        output1 = "The weather condition of " + city + " is given below:" + "\n" + condition +  "\n" + "Temperature: " + str(temperature) + "°C" +"\n"+ "Humidity: " + str(humidity) +"\n" + "Wind Speed: " + str(wind_speed)
        print(output1 + "\n-------------------------------------------")
        

    captured = capsys.readouterr()      # This wil capture the output and assert
    assert "The weather condition of London is given below:" in captured.out
    assert "Clear" in captured.out
    assert "Temperature: 22°C" in captured.out 
    assert "Humidity: 60" in captured.out
    assert "Wind Speed: 5.2" in captured.out


'''
Testing the multiple cities code. Number of cities will be two
and the cities will be London and Paris
'''

def test_multiple_cities_weather(monkeypatch, capsys):
    '''I will simulate input sequence:
        Number of cities: 2
        City names: London, Paris
        '''
    
    inputs = iter(["2", "London", "Paris"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))    #This mock the built-in input function to simulate user input from the inputs iterator

    fake_response = {       # Defining the fake response returned for both cities
        "main": {"temp": 295.15, "humidity": 55},
        "weather": [{"main": "Sunny", "icon": "01d"}],
        "wind": {"speed": 3.5}
    }

    # The get_ordinal function as defined in the code
    def get_ordinal(n):         #the ordinal function i defined for the print statement
        if 10 <= n % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"

    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = fake_response

        # multiple cities code 
        num = int(input("How many cities do you wish to get weather conditions for? "))
        count = 0
        cities = []
        while count < num:
            ord = get_ordinal(count + 1)
            city = input("Enter the " + ord + " city name: ")
            count += 1
            cities.append(city)
        for city in cities:
            url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=75623c2594f55bcc8d987fb0f841b528"
            data = requests.get(url).json()
            temperature = int(data["main"]["temp"] - 273.15)
            condition = data["weather"][0]["main"]
            cond_icon = data["weather"][0]["icon"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            output2 ="The weather condition of " + city + " is given below:" + "\n" + condition +  "\n" + "Temperature: " + str(temperature) + "°C" +"\n"+ "Humidity: " +str(humidity) +"\n" + "Wind Speed: " +str(wind_speed)
            print(output2 + "\n-------------------------------------------")
        

    # Check that both cities are in the printed output
    captured = capsys.readouterr()
    assert "The weather condition of London is given below:" in captured.out
    assert "The weather condition of Paris is given below:" in captured.out
    assert "Temperature: 22°C" in captured.out  # 295.15K - 273.15 = 22°C
    assert "Humidity: 55" in captured.out
    assert "Wind Speed: 3.5" in captured.out


def test_five_day_forecast(monkeypatch, capsys):
    # Simulate user input
    inputs = iter(["Lagos", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Create a fake 5-day forecast response
    fake_response = {
        "list": [
            {
                "main": {"temp": 300.15, "humidity": 60},
                "weather": [{"main": "Rain"}],
                "wind": {"speed": 4.2},
            }
        ] * 5  # Same data repeated 5 times for simplicity
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = fake_response

        #  5 days forecast code 
        city = input("-------------------------------------------\nEnter a city name: ")
        url = (
            "https://api.openweathermap.org/data/2.5/forecast?q="
            + city
            + "&appid=75623c2594f55bcc8d987fb0f841b528"
        )
        data = requests.get(url).json()
        index = [0, 1, 2, 3, 4]
        print("The weather condition for " + city + " for the next 5 days are: ")
        for i in index:
            temperature = int(data["list"][i]["main"]["temp"] - 273.15)
            condition = data["list"][i]["weather"][0]["main"]
            humidity = data["list"][i]["main"]["humidity"]
            wind_speed = data["list"][i]["wind"]["speed"]
            output1 = (
                condition
                + "\nTemperature: "
                + str(temperature)
                + "°C\nHumidity: "
                + str(humidity)
                + "\nWind Speed: "
                + str(wind_speed)
            )
            print(output1 + "\n-------------------------------------------")
        # This simulates the rest of the interactive loop
        decision = input(
            "Do you wish to make another selection or quit? (Type 'selection' to continue or 'quit' to exit): "
        ).strip().lower()
        if decision == "selection":
            pass
        elif decision == "quit":
            print("Have a nice day ☀️")
        else:
            print("You haven't selected a valid option.")
        # === End of code block ===

    # Assert output
    captured = capsys.readouterr()
    assert "The weather condition for Lagos for the next 5 days are:" in captured.out
    assert captured.out.count("Temperature: 27°C") == 5  # 300.15 - 273.15 = 27°C
    assert captured.out.count("Humidity: 60") == 5
    assert captured.out.count("Wind Speed: 4.2") == 5
    assert "Have a nice day ☀️" in captured.out

