from json import loads, dump, load
import datetime
import requests

url = 'https://api.open-meteo.com/v1/forecast?latitude=54.1961&longitude=37.6182&hourly=temperature_2m,apparent_temperature,precipitation_probability,cloud_cover&timezone=Europe%2FMoscow'


def get_weather7() -> str:
    return requests.get(url).text


def write_json(data):
    with open('assets/weather.json', 'w') as file:
        dump(data, file)

def get_emoji(value: int) -> str:
    if 0<= value < 20:
        return '☀️'
    elif 20 <= value < 40:
        return '🌤'
    elif 40 <= value < 60:
        return '⛅️'
    elif 60 <= value < 80:
        return '🌥'
    elif 80 <= value <= 100:
        return '☁️'

def update_weather():
    data : str = get_weather7()
    today = datetime.date.today()
    data : dict = loads(data)
    print()
    d: dict = {'dates': []}
    for i in range(7):
        day = today + datetime.timedelta(days=i)
        sub_d: dict = {}
        weather_list = []
        prec_list = []
        feels_like= []
        cloud_cover = []
        for i, hour in enumerate(data['hourly']['time']):
            if f'{day}' in hour:
                weather_list.append(data['hourly']['temperature_2m'][i])
                prec_list.append(data['hourly']['precipitation_probability'][i])
                feels_like.append(data['hourly']['apparent_temperature'][i])
                cloud_cover.append(data['hourly']['cloud_cover'][i])
        min_w, max_w = min(weather_list), max(weather_list)
        sub_d['date'] = f'{day}'
        sub_d['min_max'] = tuple([min_w, max_w])
        sub_d['07:45'] = [weather_list[8], feels_like[8], prec_list[8], get_emoji(cloud_cover[8])]
        sub_d['09:40'] = [weather_list[10], feels_like[10], prec_list[10], get_emoji(cloud_cover[10])]
        sub_d['11:35'] = [weather_list[12],feels_like[12],prec_list[12], get_emoji(cloud_cover[12])]
        sub_d['13:40'] = [weather_list[14],feels_like[14],prec_list[14], get_emoji(cloud_cover[14])]
        sub_d['15:35'] = [weather_list[16],feels_like[16],prec_list[16], get_emoji(cloud_cover[16])]
        sub_d['17:30'] = [weather_list[18],feels_like[18],prec_list[18], get_emoji(cloud_cover[18])]
        sub_d['18:00'] = [weather_list[18],feels_like[18],prec_list[18], get_emoji(cloud_cover[18])]
        sub_d['19:40'] = [weather_list[20],feels_like[20],prec_list[20], get_emoji(cloud_cover[20])]

        d['dates'].append(sub_d)
    print(d)
    write_json(d)


def dwn_weather():
    with open('assets/weather.json', 'r') as file:
        data = load(file)
    return data


def get_day_weather(day_date: str):
    data = dwn_weather()
    for date in data['dates']:
        if date['date'] == day_date:
            return date


update_weather()



