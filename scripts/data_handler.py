def get_flights_gantt_data(flights):
    flights_tags = []
    flights_periods = []
    if flights:
        for flight in flights:
            flight_tag = flight[8] + ' - ' + flight[7]
            flights_tags.append(flight_tag)
            flight_date = flight[9].replace('/', '-', 2)
            if flight[5] == None:
                flight[5] = flight[6]
            if flight[6] == None:
                flight[6] = flight[5]    
            flight_starting_time = flight_date + 'T' + str(flight[5])
            flight_ending_time = flight_date + 'T' + str(flight[6])
            time_period = [flight_starting_time, flight_ending_time]
            flights_periods.append(time_period)
        print(flights_tags)
        print(flights_periods)
