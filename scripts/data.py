time_titles = ['Horas']

for i in range(0, 24):
    for o in range(0, 4):
        if o == 0:
            minutes = '00'
        elif o == 1:
            minutes = '15'
        elif o == 2:
            minutes = '30'
        elif o == 3:
            minutes = '45'
        if i < 10:
            hour = '0'+str(i)
        else:
            hour = str(i)
    
        time_titles.append(hour+':'+minutes)