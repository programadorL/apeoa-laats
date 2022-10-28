import pyodbc
from datetime import datetime
from datetime import timedelta
import math

server = 'mysqllaats.database.windows.net'
database = 'aatl'
username = 'AdminLaats'
password = 'Fn_1_5Laats' 
driver= '{ODBC Driver 17 for SQL Server}'

def colab(no_correlativo1, mes):

    print(type(no_correlativo1))
    print(type(mes))
    print(no_correlativo1, mes)

    try: 
        with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM itinerarios WHERE departamento = 'PXS' And mes="+str(mes)+" And tipo_aeronave <> '' and tipo_operacion <> 'RECEPCION';")
                results = cursor.fetchall()
                itinerarios = results
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)

    try: 
        with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM aeronaves;")
                results = cursor.fetchall()
                aeronaves = results
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)

    try: 
        with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM operadores;")
                results = cursor.fetchall()
                operadores = results
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e) 

    try: 
        with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM parametros_personal_pxs;")
                results = cursor.fetchall()
                parametros_personal_pxs = results
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)

    try: 
        with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM configuracion_personal_vuelos_pxs;")
                results = cursor.fetchall()
                configuracion_personal_vuelos_pxs = results
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)

    try: 
        with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM tiempos_personal_pxs;")
                results = cursor.fetchall()
                tiempos_personal_pxs = results
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)

    try: 
        with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM et_parametros_personal_pxs;")
                results = cursor.fetchall()
                et_parametros_personal_pxs = results
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)

    join_aeronaves_operadores = []
    for aeronave in aeronaves:
        for operador in operadores:
            if aeronave[2] == operador[0]:
                join_dict = {'id_aeronave': aeronave[0], 'tipo_aeronave': aeronave[1], 'operador': operador[1]}
                join_aeronaves_operadores.append(join_dict)
                break

    join_itinerarios_aeronaves_operadores = []
    for itinerario in itinerarios:
        for join in join_aeronaves_operadores:
            if (itinerario[10] == join['operador'] and itinerario[14] == join['tipo_aeronave']):
                dia = itinerario[2]
                mes = itinerario[3]
                if dia < 10:
                    dia = '0'+str(dia)
                else:
                    dia = str(dia)
                if mes < 10:
                    mes = '0'+str(mes)
                else:
                    mes = str(mes)
                year = str(itinerario[1])
                fecha = year + '-' + mes + '-' + dia
                join_dict = {'no_correlativo': itinerario[0], 'fecha': fecha, 'tipo_operacion': itinerario[11], 'id_aeronave': join['id_aeronave']}
                join_itinerarios_aeronaves_operadores.append(join_dict)
                break
        

    dias = 30
    horas = dias * 24
    lapsos = horas * 4 + 1

    cantidad_posiciones = 7
    eje_y = cantidad_posiciones + 3

    matriz_freq =  [[0 for x in range(lapsos)] for y in range(eje_y)] 

    eta_despacho = '01:15:00'
    eta_transito = '00:00:10'
    etd_pernocta = '01:30:00'

    vuelos = []
    for itinerario in itinerarios:
        for config in configuracion_personal_vuelos_pxs:
            if (itinerario[0] == config[0]):
                no_correlativo = itinerario[0]
                tipo_operacion = itinerario[11]
                eta = itinerario[7]
                etd = itinerario[8]
                if tipo_operacion == 'DESPACHO':
                    eta = eta_despacho
                if tipo_operacion == 'PERNOCTA':
                    etd = etd_pernocta
                eta = datetime.strptime(str(eta), '%H:%M:%S')
                etd = datetime.strptime(str(etd), '%H:%M:%S')
                diff = etd - eta
                vuelo = {'no_correlativo': no_correlativo, 'tipo_operacion': tipo_operacion, 'eta': eta, 'etd': etd, 'diff': diff}
                vuelos.append(vuelo)
                break

    data_lapsos = []
    for vuelo in vuelos:
        no_correlativo = vuelo['no_correlativo']
        eta_horas = int(str(vuelo['eta'])[11:13])
        etd_horas = int(str(vuelo['etd'])[11:13])
        diff_horas = etd_horas - eta_horas
        eta_minutos = int(str(vuelo['eta'])[14:16])
        etd_minutos = int(str(vuelo['etd'])[14:16])
        eta = vuelo['eta']
        etd = vuelo['etd']
        lapsos_eta = 0
        lapsos_etd = 0
        #Para ETA
        if eta_minutos < 15:
            lapsos_eta = 4
        if eta_minutos >= 15 and eta_minutos < 30:
            lapsos_eta = 3
        if eta_minutos >= 30 and eta_minutos < 45:
            lapsos_eta = 2
        if eta_minutos > 45:
            lapsos_eta = 4
        #Para ETD
        if etd_minutos > 0 and etd_minutos < 15:
            lapsos_etd = 1
        if etd_minutos >= 15 and eta_minutos < 30:
            lapsos_etd = 2
        if etd_minutos >= 30 and eta_minutos < 45:
            lapsos_etd = 3
        if etd_minutos > 45:
            lapsos_etd = 4
            
        #diff horas
        if diff_horas > 1:
            total_lapsos = lapsos_eta + lapsos_etd + diff_horas*4
        else:
            total_lapsos = lapsos_eta + lapsos_etd
        data_lapsos.append({'no_correlativo': no_correlativo, 'eta': eta, 'etd': etd, 'lapsos_eta': lapsos_eta, 'lapsos_etd': lapsos_etd, 'total_lapsos': total_lapsos})

    lapsos = data_lapsos
    data = join_itinerarios_aeronaves_operadores

    info_vuelos = []
    for lapso in lapsos:
        for dato in data:
            if (lapso['no_correlativo'] == dato['no_correlativo']):
                vuelo = {'no_correlativo': dato['no_correlativo'], 'fecha': dato['fecha'], 'tipo_operacion': dato['tipo_operacion'], 'id_aeronave': dato['id_aeronave'], 'eta': lapso['eta'], 'etd': lapso['etd'], 'total_lapsos': lapso['total_lapsos']}
                info_vuelos.append(vuelo)
                break
    
    agents = ["CF","O", "AR", "AM", "AF", "ARX", "AL"]
    agentes = []
    tiempos = []
    for vuelo in info_vuelos:
        no_correlativo2 = vuelo['no_correlativo']
        for parametro in parametros_personal_pxs:
            if (vuelo['tipo_operacion'] == parametro[2] and vuelo['id_aeronave'] == parametro[1]):
                id_parametro = parametro[0]
                for tiempo_personal in tiempos_personal_pxs:
                    if tiempo_personal[0] == id_parametro:

                        for parametro_x in et_parametros_personal_pxs:
                            if parametro_x[0] == id_parametro:
                                et_parametro = parametro_x
                                break


                        year = int(vuelo['fecha'][0:4])
                        month = int(vuelo['fecha'][5:7])
                        day = int(vuelo['fecha'][8:10])

                        flight_eta_time = str(vuelo['eta'].time())
                        
                        eta_hour = int(flight_eta_time[0:2])
                        eta_minutes = int(flight_eta_time[3:5])
                        init_month_datetime = datetime(year, month, 1)
                        init_flight_datetime = datetime(year, month, day, eta_hour, eta_minutes, 0)

                        time_delta = init_flight_datetime - init_month_datetime  
                        eta_total_seconds = time_delta.total_seconds()
                        eta_total_minutes = eta_total_seconds/60

                        flight_etd_time = str(vuelo['etd'].time())
                        
                        etd_hour = int(flight_etd_time[0:2])
                        etd_minutes = int(flight_etd_time[3:5])
                        init_month_datetime = datetime(year, month, 1)
                        final_flight_datetime = datetime(year, month, day, etd_hour, etd_minutes, 0)

                        time_delta = final_flight_datetime - init_month_datetime  
                        etd_total_seconds = time_delta.total_seconds()
                        etd_total_minutes = etd_total_seconds/60
                        
                        #suma/resta minutos de cada posicion

                        '''
                            1. Tomar el dato de la cantidad de personal por posicion.
                            2. Hacer time delta de minutos a eta y etd => https://www.adamsmith.haus/python/answers/how-to-subtract-minutes-from-a-datetime-in-python#:~:text=timedelta()%20to%20subtract%20minutes,this%20timedelta%20from%20a%20datetime.
                            3. Hacer append en una lista.
                            4. Recorrer la lista por posicion y sumar las celdas de la matriz freq con las cantidades de personal.
                        '''
                        #cantidad personal 
                        for i in range(0, 7):
                            if i < 0:
                                index = i * 2 + 1
                            else:
                                index = (i-1) * 2 + 1
                            #print(parametro[i], tiempo_personal[index], tiempo_personal[index+1], et_parametro[index], et_parametro[index + 1])
                            if tiempo_personal[index] > 0:
                                position_minutes_entry = timedelta(minutes=tiempo_personal[index])
                            else:
                                position_minutes_entry = timedelta(minutes=abs(tiempo_personal[index]))
                            if tiempo_personal[index + 1] > 0:
                                position_minutes_exit = timedelta(minutes=tiempo_personal[index + 1])
                            else:
                                position_minutes_exit = timedelta(minutes=abs(tiempo_personal[index + 1]))

                            
                            if et_parametro[index] != '' and et_parametro[index+1] != '':
                                if et_parametro[index] == 'ETA':
                                    position_time_entry = init_flight_datetime - position_minutes_entry
                                elif et_parametro[index] == 'ETD':
                                    position_time_entry = final_flight_datetime - position_minutes_entry

                                if et_parametro[index] == 'ETA':
                                    position_time_exit = init_flight_datetime - position_minutes_exit
                                elif et_parametro[index] == 'ETD':
                                    position_time_exit = final_flight_datetime - position_minutes_exit

                                entry_time_delta = position_time_entry - init_month_datetime 
                                position_time_entry_seconds = entry_time_delta.total_seconds()
                                position_lapse_start =  math.ceil((position_time_entry_seconds/60)/15)

                            
                                exit_time_delta = position_time_exit - init_month_datetime 
                                position_time_exit_seconds = exit_time_delta.total_seconds()
                                position_lapse_end =  math.ceil((position_time_exit_seconds/60)/15)

                                if (no_correlativo1 == no_correlativo2):
                                    pos_en = str(position_time_entry).replace(' ', 'T')
                                    pos_ex = str(position_time_exit).replace(' ', 'T')
                                    print(agents[i], position_time_entry, position_time_exit)
                                    tiempos.append([pos_en, pos_ex])
                                    agentes.append(agents[i])

                                for o in range(position_lapse_start, position_lapse_end):
                                    matriz_freq[i][o] = matriz_freq[i][o] + parametro[i+3]

                        
                        #eta_lapses = math.ceil(eta_total_minutes/15)
                        #etd_lapses = math.ceil(etd_total_minutes/15)

                        #print(eta_lapses, etd_lapses)

    #personal asignado
    personal_lapse = 0 
    personel = {'crew_chief':9, 'supervisores':4, 'operadores':10, 'agentes':46}
    for i in range(0, len(matriz_freq[0])):
        per_disp = 0
        for o in range(0, 6):
            personal_lapse = personal_lapse + matriz_freq[o][i]
        matriz_freq[7][i] = personal_lapse
        if matriz_freq[0][i] > 0:
            per_disp = per_disp + personel['crew_chief']
        if matriz_freq[1][i] > 0:
            per_disp = per_disp + personel['operadores']
        if matriz_freq[2][i] > 0 or matriz_freq[3][i] > 0 or matriz_freq[4][i] > 0 or matriz_freq[5][i] > 0 or matriz_freq[6][i] > 0:
            per_disp = per_disp + personel['agentes']

        matriz_freq[8][i] = per_disp

        matriz_freq[9][i] = matriz_freq[8][i] - matriz_freq[7][i]
        personal_lapse = 0

    #for row in matriz_freq:
        #print(row)
    return tiempos, agentes, matriz_freq
