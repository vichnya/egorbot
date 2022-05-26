import telebot #импорт библиотеки для подключения и работы с тг ботом

# tuple(кортеж) из 10 городов для опрделения прогноза погоды
sitys_weatther = ('London',
                  'Tokyo',
                  'Paris',
                  'St. Petersburg',
                  'Los Angeles',
                  'Rome',
                  'Prague',
                  'New York',
                  'Beijing',
                  'Anapa'
                  )
#frozenset(неизменяемое множество) из 10 городов для расписания электричек
sitys_tutu = ['Сортавала',
              'Яккима',
              'Выборг',
              'Каменногорск',
              'Суоярви',
              'Элисенваара',
              'Леппясюрья',
              'Лоймола',
              'Маткаселькя',
              'Пийтсиеки'
              ]
sitys_tutu = frozenset(sitys_tutu)

#dict(словарь): ключи - 10 городов, зачения - ИКАО(код аэропорта)
sitys_AIR_ICAO = {
    'Paris': 'LFPG',
    'London': 'EGLL',
    'Vienna': 'LOWW',
    'Rome': 'LIRF',
    'Prague': 'LKPR',
    'Madrid': 'LEMD',
    'Amsterdam': 'EHAM',
    'Frankfurt am Main': 'EDDF',
    'Berlin': 'EDDB',
    'Barcelona': 'LEBL'
}

def weatherAPI(sitys):
    """Функция по работе с API по прогнозу погоды """
    import requests #импорт библиотеки для работы с API
    import random #импорт библиотеки рандомайзера
    import datetime #импорт библиотеки для работы с датой и временем

    sity = random.choice(sitys) #переменной sity присваиваем значение рандомного города из sitys
    now = datetime.datetime.now() + datetime.timedelta(days=7) #переменной now присваиваем значение текущей даты и времени с разностью плюс 7 дней

    # создаем словарь с настройками запроса к API
    ID = {
      'key': '92f34abe07b24a8cbaa125324221205', #id в системе(доступен после регистрации)
      'lang': 'ru', #язык ответа
      'q': sity, #город
      'days': 1, #количесто дней прогноза
      'dt': now.strftime("%Y-%m-%d"), #дата(переменная now) в формате(год-месяц-день)
    }

    URL = "http://api.weatherapi.com/v1/forecast.json" #ссылка-запрос к API
    res = requests.get(URL, params=ID) #запрос к API с параметрами: ссылка; настройки(params) равны словарю ID
    data = res.json() #в переменную data помещаем значение запроса в формате json

    weatherapi = [] #создаем пустой список
    weatherapi.append(f"Прогноз погоды на {now.strftime('%d.%m.%Y')}:\n") #добавляем в список строку x7
    weatherapi.append(f"Город: {ID['q']}")
    weatherapi.append(f"Описание: {data['forecast']['forecastday'][0]['day']['condition']['text']}")
    weatherapi.append(f"Средняя температура за сутки: {data['forecast']['forecastday'][0]['day']['avgtemp_c']} °C")
    weatherapi.append(f"Максимальная скорость ветра: {data['forecast']['forecastday'][0]['day']['maxwind_kph']} км/ч")
    weatherapi.append(f"Общее количество осадков: {data['forecast']['forecastday'][0]['day']['totalprecip_mm']} мм")
    weatherapi.append(f"Средняя влажность: {data['forecast']['forecastday'][0]['day']['avghumidity']} %")

    answer = '' #переменной answer присваиваем знаячение пустой строки
    for i in weatherapi: # в цикле для каждого элемента списка weatherapi делаем:
      answer += i + '\n' #переменную answer конкотинируем(присоединяем) с элементом списка weatherapi


    return answer # из функции возвращаем переменную answer


def tutuAPI(sitys):
    """Функция по работе с API по расписанию электричек """
    import requests #импорт библиотеки для работы с API
    import random #импорт библиотеки рандомайзера

    # dict(словарь): ключи - 10 городов, зачения - код станции
    SITY_CODE = {
        'Сортавала': '2004266',
        'Яккима': '2004261',
        'Выборг': '2004682',
        'Каменногорск': '2005351',
        'Суоярви': '2004282',
        'Элисенваара': '2004258',
        'Леппясюрья': '2004276',
        'Лоймола': '2004278',
        'Маткаселькя': '2004270',
        'Пийтсиеки': '2004280'
    }

    sity = random.choice(list(sitys)) #переменной sity присваиваем значение рандомного города из sitys, обращенного в список
    term = '2004004'  # код станции спб-Финл.
    term2 = SITY_CODE[sity] # код станции из словаря SITY_CODE с ключем равным переменной sity

    URL = f'https://suggest.travelpayouts.com/search?service=tutu_trains&term={term}&term2={term2}' #ссылка-запрос к API с параметрами: код станции отправления, код станции прибытия

    res = requests.get(URL) #запрос к API с параметром ссылка
    data = res.json() #в переменную data помещаем значение запроса в формате json

    tutuapi = [] #создаем пустой список
    tutuapi.append("Расписание электрички\n") #добавляем в список строку x8
    tutuapi.append(f"Номер поезда: {data['trips'][0]['trainNumber']}")
    tutuapi.append(f"Примерная цена: {data['trips'][0]['categories'][0]['price']} ₽")
    tutuapi.append("Cтанция отправления: Санкт-Петербург(Финл.)")
    tutuapi.append(f"Cтанция назначения: {sity}")
    tutuapi.append(f"Время отправления: {data['trips'][0]['departureTime']}")
    tutuapi.append(f"Время прибытия: {data['trips'][0]['arrivalTime']}")
    tutuapi.append(f"Купи билет на tutu.ru:\nhttps://www.tutu.ru/{data['url']}")

    answer = '' #переменной answer присваиваем знаячение пустой строки
    for i in tutuapi: # в цикле для каждого элемента списка tutuapi делаем:
        answer += i + '\n' #переменную answer конкотинируем(присоединяем) с элементом списка tutuapi

    return answer # из функции возвращаем переменную answer


def airAPI(sitys):
    """Функция по работе с API по информации о рейсах """
    import requests #импорт библиотеки для работы с API
    import random #импорт библиотеки рандомайзера
    import datetime #импорт библиотеки для работы с датой и временем

    sity_begin = random.choice(list(sitys)) # переменной sity_begin присваиваем рандомное значение из sitys, обращенного в список
    sity_end = random.choice(list(sitys)) # переменной sity_end присваиваем рандомное значение из sitys, обращенного в список
    while sity_begin == sity_end: #пока sity_begin равно sity_end выполняем:
        sity_end = random.choice(list(sitys)) #переменной sity_end переприсваиваем рандомное значение из sitys, обращенного в список

    air_begin = sitys[sity_begin] #переменной air_begin присваиваем значение из sytys по ключу раному переменной sity_begin(ИКАО аэропорта вылета)
    air_end = sitys[sity_end] #переменной air_end присваиваем значение из sytys по ключу раному переменной sity_end(ИКАО аэропорта прилета)

    now = datetime.datetime.now() - datetime.timedelta(days=3) #переменной now присваиваем значение текущей даты и времени с разностью минус 3 дня
    time_begin = str(int(now.timestamp())) #переменной time_begin присваиваем значение текущей даты и времени(now), обращенное в целое число(int), обращенное в строку(str)

    now = datetime.datetime.now() #переменной now присваиваем значение текущей даты и времени
    time_end = str(int(now.timestamp())) #переменной time_end присваиваем значение текущей даты и времени(now), обращенное в целое число(int), обращенное в строку(str)

    URL = f"https://opensky-network.org/api/flights/departure?airport={air_begin}&begin={time_begin}&end={time_end}" #ссылка-запрос к API с параметрами: ИКАО аэропорта вылета, время начала поиска, время конца поиска

    res = requests.get(URL) #запрос к API с параметром ссылка
    data = res.json() #в переменную data помещаем значение запроса в формате json

    for i in range(len(data) - 1): #в цикле для каждого числа в диапозоне значений от 0 до длины списка data минус 1
        if data[i]['estArrivalAirport'] == air_end: #если значение из data с индексом равном i по ключу estArrivalAirport равно ИКАО прилета
            number_data = i #переменной number_data присваеваем значение индекса
            break #выходим из цикла
    try: #запускаем обработчик исключений
        airapi = [] #создаем пустой список
        airapi.append(f"Информация о рейсах:\n") #добавляем в список строку x9
        airapi.append(f"Номер самолета: {data[number_data]['icao24']}")
        airapi.append(f"Город вылета: {sity_begin}")
        airapi.append(f"Аэропорт вылета: {data[number_data]['estDepartureAirport']}")
        airapi.append(f"Дата и время вылета: {datetime.datetime.utcfromtimestamp(data[number_data]['firstSeen']).strftime('%d.%m.%Y %H:%M')}")
        airapi.append(f"Город прибытия: {sity_end}")
        airapi.append(f"Аэропорт прибытия: {data[number_data]['estArrivalAirport']}")
        airapi.append(f"Дата и время прибытия: {datetime.datetime.utcfromtimestamp(data[number_data]['lastSeen']).strftime('%d.%m.%Y %H:%M')}")
        airapi.append(f"Время в пути: {datetime.datetime.utcfromtimestamp(data[number_data]['lastSeen'] - data[number_data]['firstSeen']).strftime('%H ч. %M мин.')}")

        answer = '' #переменной answer присваиваем знаячение пустой строки
        for j in airapi: # в цикле для каждого элемента списка airapi делаем:
            answer += j + '\n' #переменную answer конкотинируем(присоединяем) с элементом списка airapi
    except: # если выпало исключение(Error)
        answer = f"Из {sity_begin} в {sity_end} за прошедшие 3 дня самолетов не вылетало" #переменной answer присваиваем значение строки

    return answer # из функции возвращаем переменную answer


def sett_file(file="positive_thoughts.txt"):
    """Функция для чтения из файла """
    load = [] #создаем пустой список
    file_r = open(file, mode='r', errors='ignore') #переменной file_r присваиваем значение возвращенное из фунции открытия файла для чтения(при этом вызывая ее)
    lines = file_r.readlines() #переменной lines присваиваем список из file_r, считанный построчно
    file_r.close() #закрываем файл

    for l in lines: #для каждого элемента в списке lines:
        sett = l.split('.') #переменной sett присваиваем список значений, сгенерированный из строки, которую разделили по знаку '.'
        sett[1] = sett[1].strip('\n') #удаляем из эелемента списка sett с индексем 1 часть строки равной '\n'
        load.append(sett[1]) #добавлям в список load эелемент списка sett с индексем 1

    return(load) #возвращаем из функции список load

bot = telebot.TeleBot('5384267499:AAEi_cDYq-dQ1AONFKxpUdzNfhKYFxml_LA') #подключение к боту с помощью параметра token

@bot.message_handler(commands=['start']) #встроенный из библиотеки декоратор, вызывающий функцию bot_start при получении команды 'start'
def bot_start(message):
    """Функция - ответ c приветственным сообщением и клавиатурой"""
    keyboard = telebot.types.ReplyKeyboardMarkup() #создаем Reply клавиатуру
    noprice = telebot.types.KeyboardButton('Бесплатно') #создаем кнопку с подписью 'Бесплатно'
    price = telebot.types.KeyboardButton('Платно') #создаем кнопку с подписью 'Платно'
    keyboard.add(noprice, price) #добавляем в клавиатуру кнопки
    bot.send_message(message.chat.id,
                     'Привет, {username}'.format(username=message.from_user.username),
                     parse_mode='html',
                     reply_markup=keyboard) #отправляем сообщение в чат


@bot.message_handler(content_types=['text']) #встроенный из библиотеки декоратор, вызывающий функцию bot_message при получении текстового сообщения
def bot_message(message):
    """Функция - ответ при соответстующем сообщении"""
    import random #импорт библиотеки рандомайзера
    if (message.text == 'Бесплатно'): #если сообщение соответствует 'Бесплатно', то
        bot.send_message(message.chat.id, random.choice(sett_file(file="positive_thoughts.txt"))) #отправляем сообщение в чат с рандомным элементом из списка возвращенного из sett_file
    elif (message.text == 'Платно'):#или если сообщение соответствует 'Платно', то
        random_number = random.randint(1, 3) #переменной random_number присваиваем рандомное значение от 1 до 3
        if random_number == 1: #если random_number равна 1
            bot.send_message(message.chat.id, weatherAPI(sitys_weatther)) #отправляем сообщение в чат с значением возвращщенным из weatherAPI с параметром sitys_weatther
        elif random_number == 2: #или если random_number равна 2
            bot.send_message(message.chat.id, tutuAPI(sitys_tutu)) #отправляем сообщение в чат с значением возвращщенным из tutuAPI с параметром sitys_tutu
        elif random_number == 3: #или если random_number равна 3
            bot.send_message(message.chat.id, airAPI(sitys_AIR_ICAO)) #отправляем сообщение в чат с значением возвращщенным из airAPI с параметром sitys_AIR_ICAO


bot.polling(none_stop=True) #постоянная работа бота