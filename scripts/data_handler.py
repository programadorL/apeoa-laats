def get_flights_gantt_data(flights):
    '''
        Este metodo se utiliza para recolectar la informacion necesaria para generar diagramas de gantt
        de todos los vuelos de un dia especifico. Recibe un dataset de los vuelos previamente recolectados.
        Con el dataset, genera un arreglo llamado 'flights_tags' en donde se almacena la informacion de cada
        operador y el numero de vuelo anexados con un '-'. Luego en otro arreglo llamado 'flights_periods',
        almacena pares ordenados de la fecha de inicio y fecha de finalizacion del vuelo en formato datetime
        de javascript.

        Parametros:
            flights -> Array

        Ver en app.py:
            flights()
        
        Salida:
            flights_tags (Array) ej. ['AMERICAN-356/431', ... , 'JETBLUE-541/541']
            flights_periods (Array) ej. [['2023-01-01T00:00:00', '2023-01-01T00:10:00'], ... , ['2023-01-01T01:30:00', '2023-01-01T02:00:00']]
            
    '''
    flights_tags = []
    flights_periods = []
    if flights:
        for flight in flights:
            flight_tag = flight[8] + ' - ' + flight[7]
            flights_tags.append(flight_tag)
            if flight[0] < 10:
                flight_day = '0' + str(flight[0])
            else:
                flight_day = str(flight[0])
            if flight[1] < 10:
                flight_month = '0' + str(flight[1])
            else:
                flight_month = str(flight[1])
            flight_date = str(flight[2]) + '-' + flight_month + '-' + flight_day
            if flight[5] == None:
                flight[5] = flight[6]
            if flight[6] == None:
                flight[6] = flight[5]    
            flight_starting_time = flight_date + 'T' + str(flight[5])
            flight_ending_time = flight_date + 'T' + str(flight[6])
            time_period = [flight_starting_time, flight_ending_time]
            flights_periods.append(time_period)
    return flights_tags, flights_periods
            



