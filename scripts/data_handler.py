def get_flights_gantt_data(flights):
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

def process_personel_et(operation_type, start_time, end_time, times_parameter, et_parameter):
    start_hour = int(start_time[0:2])
    start_minutes = int(start_time[3:5])
    start_time_minutes = start_hour*60 + start_minutes

    end_hour = int(end_time[0:2])
    end_minutes = int(end_time[3:5])
    end_time_minutes = end_hour*60 + end_minutes

    date_times_minutes = []
    if (operation_type == 'DESPACHO'):
        for i in range(0, len(times_parameter)):
            if et_parameter[i + 1] == 'ETA':
                date_times_minutes.append(times_parameter[i + 1] + start_time_minutes)
            if et_parameter[i + 1] == 'ETD':
                date_times_minutes.append(times_parameter[i + 1] + end_time_minutes)
            



