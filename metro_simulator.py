import os

script_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(script_dir, 'metro_data.txt') 
#  joining datafile to program

def data_extraction(file_path): 
    with open(file_path, mode='r', encoding='utf-8') as file:
        data = file.read()
    
    start_marker = '<$'
    end_marker = '$>'
    start_index = data.find(start_marker)
    end_index = data.find(end_marker)
    
    frequency = list(data[start_index:end_index].split(','))
    del frequency[0]
    frequencyup = []
    for f in frequency:
        frequencyup.append(int(f.strip()))
    
    N_blueline_start ='<Blue_main_line'
    N_blueline_end = 'Blue_main_line>'
    T_blueline_start = '<tBlue_main_line'
    T_blueline_end = 'tBlue_main_line>'
    blueline, timelist_blueline = data_extract(N_blueline_start,N_blueline_end,T_blueline_start,T_blueline_end,data)

    N_magentaline_start ='<Magenta_line'
    N_magentaline_end = 'Magenta_line>'
    T_magentaline_start = '<tMagenta_line'
    T_magentaline_end = 'tMagenta_line>'

    magentaline, timelist_magentaline = data_extract(N_magentaline_start,N_magentaline_end,T_magentaline_start,T_magentaline_end,data)

    N_Blue_side_line_start ='<Blue_side_line'
    N_Blue_side_line_end = 'Blue_side_line>'
    T_Blue_side_line_start = '<tBlue_side_line'
    T_Blue_side_line_end = 'tBlue_side_line>'   

    bluesideline , timelist_bluesideline = data_extract(N_Blue_side_line_start,N_Blue_side_line_end,T_Blue_side_line_start,T_Blue_side_line_end,data)
    return blueline, timelist_blueline , magentaline, timelist_magentaline , bluesideline , timelist_bluesideline, frequencyup
 
def data_extract(N_start,N_end,T_start,T_end,data):
    start_idx = data.find(N_start)
    end_idx = data.find(N_end)
    linenames = list(data[start_idx:end_idx].split('-'))
    del linenames[0] 
    del linenames[-1]
  
    data_updated = []
    for i in linenames:
        data_updated.append(i.strip().lower())
    del linenames
    linenames = data_updated.copy()
    del data_updated
    
    strt_index_time = data.find(T_start) + len(T_start)
    end_index_time = data.find(T_end)
    time_string = data[strt_index_time:end_index_time].strip()
    tuple_starting = time_string.find(T_start)
    time_string = time_string[tuple_starting+2:]
    
    time_list_raw = time_string.split('#')
    
    del time_list_raw[-1]
    temp =[]
    timelist_line = []
    for i in time_list_raw:
        temp = list(i.strip())
        timelist_line.append( (int(temp[1]), int(temp[3])) )
    del temp
    del time_list_raw
    
    return linenames, timelist_line

def data_extraction2(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        data = file.read()

    bstrt  = "<blue_metro_start"
    bend   = "blue_metro_start>"

    mstrt  = "<magenta_metro_start"
    mend   = "magenta_metro_start>"

    bsstrt = "<blueside_metro_start"
    bsend  = "blueside_metro_start>"

    b_start_index = data.find(bstrt)
    b_end_index   = data.find(bend, b_start_index + len(bstrt))
    blue_block = data[b_start_index + len(bstrt) : b_end_index].strip()
    blue_metrostart = blue_block.split('#')
    del blue_metrostart[-1]
    del blue_metrostart[0]

    m_start_index = data.find(mstrt)
    m_end_index   = data.find(mend, m_start_index + len(mstrt))
    magenta_block = data[m_start_index + len(mstrt) : m_end_index].strip()
    magenta_metrostart = magenta_block.split('#')
    del magenta_metrostart[-1]
    del magenta_metrostart[0]
 
    bs_start_index = data.find(bsstrt)
    bs_end_index   = data.find(bsend, bs_start_index + len(bsstrt))
    blueside_block = data[bs_start_index + len(bsstrt) : bs_end_index].strip()
    blueside_metrostart = blueside_block.split('#')
    del blueside_metrostart[-1]
    del blueside_metrostart[0]

    return blue_metrostart, magenta_metrostart, blueside_metrostart

def main1():
    blueline, timelist_blueline ,magentaline , timelist_mahentaline , bluesideline , timelist_bluesideline, frequency= data_extraction(file_path)
    print("--------------------------------------------------------------------------------------------------------------------------------")
    print("WELCOME TO THE METRO ROUTE TRACKER AND TRAVEL TIME CALCULATOR")
    
    source = input("Enter source station: ").strip().lower()
    if not (source in blueline or source in magentaline or source in bluesideline):
        print("no such source station found")
        print("try agin: ")
        exit()
    destination = input("Enter destination station: ").strip().lower()   
    if not (destination in blueline or destination in magentaline or destination in bluesideline):
        print("no such destination station found")
        print("try agin: ")
        exit()
    if source == destination:
        print("source and destination cannot be same: ")
        print("try again")
        exit()     
           

    current_time = input("enter time in 24 hr format <HH MM> : ").strip().split()
    total_minutes = time_into_min(current_time)
    if total_minutes > 1410 or total_minutes < 360:
        print("metro not availabe at this time")
        exit()
    
    interchange_station = []
    phase_time = []
    travel_time = 0
    phase1_time = 0
    phase2_time = 0

    
    if source in blueline and destination in blueline: 
        source_index = blueline.index(source)
        destination_index = blueline.index(destination)
    
        if source_index == destination_index:
            print("Source and destination stations are the same.")
            return
        k = -1
        if source_index < destination_index:
            k =0
        else :
            k = 1
        travel_time = timecaluction(source_index, destination_index, timelist_blueline)
      
    elif source in magentaline and destination in magentaline:

        source_index = magentaline.index(source)
        destination_index = magentaline.index(destination)
    
        if source_index == destination_index:
            print("Source and destination stations are the same.")
            return
        k = -1
        if source_index < destination_index:
            k =0
        else :
            k = 1
        travel_time = timecaluction(source_index, destination_index,timelist_mahentaline)

    elif source in bluesideline and destination in bluesideline:

        source_index = bluesideline.index(source)
        destination_index = bluesideline.index(destination)
    
        if source_index == destination_index:
            print("Source and destination stations are the same.")
            return
        k = -1
        if source_index < destination_index:
            k =0
        else :
            k = 1
        travel_time = timecaluction(source_index, destination_index, timelist_bluesideline)

    elif source in blueline and destination in magentaline:
         #case 1 through botanical garden
        travel_time1 = timecaluction(blueline.index(source), blueline.index("botanical garden"), timelist_blueline)
        case1phase1_time = travel_time1
        case1phase2_time = timecaluction(magentaline.index("botanical garden"), magentaline.index(destination), timelist_mahentaline)
        travel_time1 = case1phase1_time + case1phase2_time
        #case 2 through janakpuri west
        travel_time2 = timecaluction(blueline.index(source), blueline.index("janakpuri west"), timelist_blueline)
        case2phase1_time = travel_time2
        case2phase2_time = timecaluction(magentaline.index("janakpuri west"), magentaline.index(destination), timelist_mahentaline)
        travel_time2 = case2phase1_time + case2phase2_time
        if travel_time1 < travel_time2:
             interchange_station.append("botanical garden")
             phase_time.append(case1phase1_time)
             phase_time.append(case1phase2_time)
             travel_time = travel_time1
        else:
            interchange_station.append("janakpuri west")
            phase_time.append(case2phase1_time)
            phase_time.append(case2phase2_time)
            travel_time = travel_time2

    elif source in magentaline and destination in blueline:
        #case 1 through botanical garden
        travel_time1 = timecaluction(magentaline.index(source), magentaline.index("botanical garden"), timelist_mahentaline)
        case1phase1_time = travel_time1
        case1phase2_time = timecaluction(blueline.index("botanical garden"), blueline.index(destination), timelist_blueline)
        travel_time1 = case1phase1_time + case1phase2_time
        #case 2 through janakpuri west
        travel_time2 = timecaluction(magentaline.index(source), magentaline.index("janakpuri west"), timelist_mahentaline)
        case2phase1_time = travel_time2
        case2phase2_time = timecaluction(blueline.index("janakpuri west"), blueline.index(destination), timelist_blueline)
        travel_time2 = case2phase1_time + case2phase2_time
        if travel_time1 < travel_time2:
             interchange_station.append("botanical garden")
             phase_time.append(case1phase1_time)
             phase_time.append(case1phase2_time)
             travel_time = travel_time1
        else:
            interchange_station.append("janakpuri west")
            phase_time.append(case2phase1_time)
            phase_time.append(case2phase2_time)
            travel_time = travel_time2
 
    elif source in blueline and destination in bluesideline:
        #through yamuna bank
        travel_time1 = timecaluction(blueline.index(source), blueline.index("yamuna bank"), timelist_blueline)
        phase_time.append(travel_time1)
        phase_time.append(timecaluction(bluesideline.index("yamuna bank"), bluesideline.index(destination), timelist_bluesideline))
        travel_time = phase_time[0] + phase_time[1]
        interchange_station.append("yamuna bank")

    elif source in bluesideline and destination in blueline:
        #through yamuna bank
        travel_time1 = timecaluction(bluesideline.index(source), bluesideline.index("yamuna bank"), timelist_bluesideline)
        phase1_time = travel_time1
        phase_time.append(travel_time1)
        phase2_time = timecaluction(blueline.index("yamuna bank"), blueline.index(destination), timelist_blueline)
        phase_time.append(phase2_time)
        travel_time = phase1_time + phase2_time
        interchange_station.append("yamuna bank")
    
    elif source in magentaline and destination in bluesideline:
        # case 1 through botanical garden and yamuna bank
        case1phase1_time = timecaluction(magentaline.index(source), magentaline.index("botanical garden"), timelist_mahentaline)
        case1phase2_time = timecaluction(blueline.index("botanical garden"), blueline.index("yamuna bank"), timelist_blueline)
        case1phase3_time = timecaluction(bluesideline.index("yamuna bank"), bluesideline.index(destination), timelist_bluesideline)
        case1travel_time = case1phase1_time + case1phase2_time + case1phase3_time
    
        #case 2 through janakpuri west and yamuna bank
        case2phase1_time = timecaluction(magentaline.index(source), magentaline.index("janakpuri west"), timelist_mahentaline)
        case2phase2_time = timecaluction(blueline.index("janakpuri west"), blueline.index("yamuna bank"), timelist_blueline)
        case2phase3_time = timecaluction(bluesideline.index("yamuna bank"), bluesideline.index(destination), timelist_bluesideline) 
        case2travel_time = case2phase1_time + case2phase2_time + case2phase3_time

        if case1travel_time < case2travel_time:
            interchange_station.append("botanical garden")
            interchange_station.append("yamuna bank")
            phase_time.append(case1phase1_time)
            phase_time.append(case1phase2_time)
            phase_time.append(case1phase3_time)
            travel_time = case1travel_time
        else:
            interchange_station.append("janakpuri west")
            interchange_station.append("yamuna bank")
            phase_time.append(case2phase1_time)
            phase_time.append(case2phase2_time)
            phase_time.append(case2phase3_time)
            travel_time = case2travel_time

    elif source in bluesideline and destination in magentaline:
        # case 1 through yamuna bank and botanical garden
        case1phase1_time = timecaluction(bluesideline.index(source), bluesideline.index("yamuna bank"), timelist_bluesideline)
        case1phase2_time = timecaluction(blueline.index("yamuna bank"), blueline.index("botanical garden"), timelist_blueline)
        case1phase3_time = timecaluction(magentaline.index("botanical garden"), magentaline.index(destination), timelist_mahentaline)
        case1travel_time = case1phase1_time + case1phase2_time + case1phase3_time
    
        #case 2 through yamuna bank and janakpuri west
        case2phase1_time = timecaluction(bluesideline.index(source), bluesideline.index("yamuna bank"), timelist_bluesideline)
        case2phase2_time = timecaluction(blueline.index("yamuna bank"), blueline.index("janakpuri west"), timelist_blueline)
        case2phase3_time = timecaluction(magentaline.index("janakpuri west"), magentaline.index(destination), timelist_mahentaline) 
        case2travel_time = case2phase1_time + case2phase2_time + case2phase3_time

        if case1travel_time < case2travel_time:
            interchange_station.append("yamuna bank")
            interchange_station.append("botanical garden")
            phase_time.append(case1phase1_time)
            phase_time.append(case1phase2_time)
            phase_time.append(case1phase3_time)
            travel_time = case1travel_time
        else:
            interchange_station.append("yamuna bank")
            interchange_station.append("janakpuri west")
            phase1_time = case2phase1_time
            phase2_time = case2phase2_time
            phase3_time = case2phase3_time
            phase_time.append(case2phase1_time)
            phase_time.append(case2phase2_time)
            phase_time.append(case2phase3_time)
            travel_time = case2travel_time

    printer(total_minutes,source, destination, interchange_station, phase_time, travel_time)

def timecaluction(source_index, destination_index, timelist):
    k = -1
    if source_index < destination_index:
            k =0
    else :
            k = 1
    travel_time = 0
    if k == 0:
            for i in range(source_index, destination_index):
                travel_time = travel_time + timelist[i+1][0]
    else:
            for i in range(destination_index, source_index):
                travel_time = travel_time + timelist[i][1]
    return travel_time

def printer(total_minutes, source, destination, interchange_station, phase_time, travel_time):
    blueline, timelist_blueline, magentaline, timelist_magentaline, bluesideline, timelist_bluesideline, frequency = data_extraction(file_path)
    stationnames = [blueline, magentaline, bluesideline]
    timeline = [timelist_blueline, timelist_magentaline, timelist_bluesideline]
    
    # this is use metro_timings function in recursive way (but such that it dont repeat the case which has already been dopne )
    src_mask = [False, False, False] 
    
    # Target is the next station we are visiting (either destination or first interchange)
    first_target = interchange_station[0] if len(interchange_station) > 0 else destination

    if source in blueline and first_target in blueline:
        src_mask[0] = True
    elif source in magentaline and first_target in magentaline:
        src_mask[1] = True
    elif source in bluesideline and first_target in bluesideline:
        src_mask[2] = True
    
    #  prin is what tells the function that which part has to be taken or printed
    prin = [False, True, True]
    sfwd, sbck = metro_timing(source, prin, src_mask, total_minutes)
    

    
    dest_mask = [False, False, False]
    last_stop = interchange_station[-1] if len(interchange_station) > 0 else source

    if destination in blueline and last_stop in blueline:
        dest_mask[0] = True
    elif destination in magentaline and last_stop in magentaline:
        dest_mask[1] = True
    elif destination in bluesideline and last_stop in bluesideline:
        dest_mask[2] = True

    dfwd, dbck = metro_timing(destination, prin, dest_mask, total_minutes)
    

    total_minutes1 = total_minutes
    list_interchange = []
    
    # For intermediate interchanges, we can check for all 
    mutliple_all = [True, True, True] 

    if len(interchange_station) > 0:
        interchangetime = total_minutes
        for i in range(len(interchange_station)):
            interchangetime += phase_time[i] 
            a, b = metro_timing(interchange_station[i], prin, mutliple_all, interchangetime) # considering edge case when there could be a train from source but trains arenot available from the interchange stations , so -1 is being is passed to a / b depending the same
            list_interchange.append([a, b])

    # checking if the source has trains by checing for -1
    strains = False
    if sfwd[0] != -1: strains = True
    if sbck[0] != -1: strains = True
    
    if not strains:
        print(f"Sorry, your journey cannot be completed because metro stops at {source}")
        exit()

    # checking interchange for the same...
    if len(interchange_station) > 0:
        for i in range(len(list_interchange)):
            itrains = False
            if list_interchange[i][0][0] != -1: itrains = True
            if list_interchange[i][1][0] != -1: itrains = True
            
            if not itrains:
                print(f"Sorry, your journey cannot be completed because metro stops at {interchange_station[i]} before reaching {destination}")
                exit()
    
    # Check Destination if trains are stoping before reachong the destination (edge case, journey around 23 : 00)
    linee = []
    if len(interchange_station) == 0:
        if source in blueline and destination in blueline: linee = blueline
        elif source in magentaline and destination in magentaline: linee = magentaline
        elif source in bluesideline and destination in bluesideline: linee = bluesideline
        
        if linee and linee.index(source) < linee.index(destination):
            if dfwd[0] == -1 and sfwd[0] != -1:
                 print(f"Sorry , your jouney cannot be complete because metro stops before reaching the {destination}")
                 exit()
        elif linee:
             if dbck[0] == -1 and sbck[0] != -1:
                 print(f"Sorry , your jouney cannot be complete because metro stops before reaching the {destination}")
                 exit()

    print("")
    print("")
    print(f"source ---> {source} ")
    if len(interchange_station)!=0:
        for indx , value in enumerate(interchange_station):
            print(f" interachange {indx+1}  ---> {value}")
    print(f"destination ---> {destination}")
    
    # Convert times
    for f in range(len(sfwd)):
        if sfwd[f] != -1: sfwd[f] = timeconvertor(sfwd[f])
    for b in range(len(sbck)):
        if sbck[b] != -1: sbck[b] = timeconvertor(sbck[b])
    for n in list_interchange:
        for m in n:
            for p in range(len(m)):
                if m[p] != -1: m[p] = timeconvertor(m[p])

    if len(interchange_station) == 0:
        print(f"future metro from {source} to {destination} are: ")
        
    
        linee_direct = []
        if source in blueline and destination in blueline: 
            linee_direct = blueline
        elif source in magentaline and destination in magentaline: 
            linee_direct = magentaline
        elif source in bluesideline and destination in bluesideline: 
            linee_direct = bluesideline

        if linee_direct:
            if linee_direct.index(source) < linee_direct.index(destination):
                # Moving Forward
                for f in sfwd: 
                    if f != -1: time_printer(f)
            else:
                # Moving Backward
                for b in sbck:
                    if b != -1: time_printer(b)
            
    else:
        print(f"future metro from the {source} :")
        # Use Source Mask to pick only the valid line timings
        linee_start = []
        if src_mask[0]: linee_start = blueline
        elif src_mask[1]: linee_start = magentaline
        elif src_mask[2]: linee_start = bluesideline
        
        if linee_start.index(source) < linee_start.index(interchange_station[0]):
             for f in sfwd:
                 if f != -1: 
                    time_printer(f)
        else:
             for b in sbck:
                 if b != -1: 
                    time_printer(b)

        for i in range(len(interchange_station)):
            print(f"time taken to reach {interchange_station[i]} is {phase_time[i]} minutes")
            print(f"Arrive at {interchange_station[i]} at :")
            if i == 0:
                time_printer(timeconvertor(total_minutes + phase_time[0])) 
            if i == 1:
                time_printer(timeconvertor(total_minutes + phase_time[0] + phase_time[1] + 4))
            
            print(f"future metro from {interchange_station[i] } are at :")
            
            next_stop = interchange_station[i+1] if i + 1 < len(interchange_station) else destination
            linee_int = []
            if interchange_station[i] in blueline and next_stop in blueline: linee_int = blueline
            elif interchange_station[i] in magentaline and next_stop in magentaline: linee_int = magentaline
            elif interchange_station[i] in bluesideline and next_stop in bluesideline: linee_int = bluesideline
            
            timings_to_print = []
            if linee_int and linee_int.index(interchange_station[i]) < linee_int.index(next_stop):
                 timings_to_print = list_interchange[i][0] # Forward
            else:
                 timings_to_print = list_interchange[i][1] # Backward

            for p in timings_to_print:
                if p == -1:
                    print(" No metro available (End of Service)")
                    exit()
                else:
                    time_printer(p)
                                            
        linee2 = []
        if destination in blueline and interchange_station[-1] in blueline:
            linee2 = blueline
        elif destination in magentaline and interchange_station[-1] in magentaline:
            linee2 = magentaline
        elif destination in bluesideline and interchange_station[-1] in bluesideline:
            linee2 = bluesideline
        h = stationnames.index(linee2)
        time_from_interchange_to_destination = timecaluction(linee2.index(interchange_station[-1]),linee2.index(destination),timeline[h])
        print(f"time taken to reach {destination} from {interchange_station[-1]} is {time_from_interchange_to_destination } minutes                // 4 minutes of interchange time has been incooperated")
    
    print(f"Arrive at {destination} at :")
    time_printer(timeconvertor(total_minutes1 + travel_time + 4*len(interchange_station)))
    print(" ")
    print(f" Total travel time from {source} to {destination} --> {travel_time + 4*len(interchange_station)} minutes")
    print(" ")
    fare = fare_calculator(travel_time + 4*len(interchange_station))
    print(f"your fair for the journey is  {fare} rupees")

def timeconvertor(minutes):
    hours = (minutes // 60) % 24
    mins = minutes % 60
    return [hours , mins]

def fare_calculator(total_time_minutes):
    fare = 0
    if total_time_minutes <= 15:
        fare = 10
    elif 15 < total_time_minutes <= 40:
        fare = 30
    elif 40 < total_time_minutes <= 70:
        fare = 50
    else:
        fare = 60 
    return fare

def time_into_min(time):
    try:
        assert len(time) == 2
        time[0] = int(time[0])
        time[1]= int(time[1])
        hr = time[0]
        mins = time[1]
        assert hr in range(0,24)
        assert mins in range(0,60) 
        return hr*60 + mins
    except:
        print("invalid time format") 
        exit() 

def time_printer(lst):
    print(f" {lst[0]} hr : {lst[1]} min")
    
def main2(): 
    #function for finding next possible metro timings
    blueline, timelist_blueline ,magentaline , timelist_mahentaline , bluesideline , timelist_bluesideline, frequency= data_extraction(file_path)
    station = input("enter sation name: ")
    if not (station in blueline or station in magentaline or station in bluesideline):
        print("no such source station found")
        print("try agin: ")
        exit()

    
    time = input("enter time in 24 hr format <HH MM> : ").strip().split()

    total_minutes = time_into_min(time)
    if total_minutes > 1410 or total_minutes < 360:
        print("metro not available at this time for your journey")
        exit()
    prin = [True,True,False]
    multiple = [True,True,True]
    metro_timing(station,prin,multiple,total_minutes)

def metro_timing(station,prin,mutliple,total_minutes): 
    
    blueline, timelist_blueline ,magentaline , timelist_magentaline , bluesideline , timelist_bluesideline,frequency = data_extraction(file_path)
    
    blueline_metrostart, magentaline_metrostart, bluesideline_metrostart = data_extraction2(file_path)
    
    line = []
    temp_list = []
    if mutliple[0]:
        if station in blueline:
            line = blueline.copy()
            time = []
            if station not in blueline_metrostart:
                
                temp_list = blueline_metrostart.copy()
                temp_list.append(station)
                temp_list.sort(key = blueline.index)
                index = blueline.index(station)
                
                p = temp_list.index(station)
                time.append(timecaluction(blueline.index(temp_list[p-1]),index,timelist_blueline)) # front jouney
                time.append(timecaluction(blueline.index(temp_list[p+1]),index,timelist_blueline)) # back journey
            else:
                time.append(0)
                time.append(0)
            if prin[0] == True:
                mutliple[0] = False
            if True: 
                if prin[0]:
                    if station != line[0] and station != line[-1]:
                        print(f" Earliest metro can be boarded from {station} towards {line[-1]} at :")
                        time_printer(timeconvertor(time[0]+60*6))
                        print(f" Earliest metro can be boarded from {station} towards {line[0]} at :")
                        time_printer(timeconvertor(time[1]+60*6))
                        print(f" Last metro can be boarded from {station} towards {line[-1]} at :")
                        time_printer(timeconvertor(time[0]+60*23))
                        print(f" Last metro can be boarded from {station} towards {line[0]} at :")
                        time_printer(timeconvertor(time[1]+60*23))
                    else:
                        if station == line[0]:
                            print(f" Earliest metro can be boarded from {station} towards {line[-1]} at :")
                            time_printer(timeconvertor(time[0]+60*6))
                            print(f" Last metro can be boarded from {station} towards {line[-1]} at :")
                            time_printer(timeconvertor(time[0]+60*23))
                        else:
                            print(f" Earliest metro can be boarded from {station} towards {line[0]} at :")
                            time_printer(timeconvertor(time[1]+60*6))
                            print(f" Earliest metro can be boarded from {station} towards {line[0]} at :")
                            time_printer(timeconvertor(time[1]+60*23))
                        
                if prin[1]:
                    forward_freq = []
                    backward_freq = []
                    forward_freq = list(map(lambda x : x + time[0], frequency))
                    backward_freq = list(map(lambda x : x + time[1], frequency))

                    forward_timings = [x for x in forward_freq if x >= total_minutes]
                    backward_timings =[x for x in backward_freq if x >= total_minutes]
                    
                    forward_timings_ = []
                    backward_timings_ = []
                    if len(forward_timings)>3:
                        forward_timings_ = forward_timings[:3]
                    else:
                        forward_timings_ = forward_timings.copy()
                    if len(forward_timings) == 0:
                        forward_timings_.append(-1)
                    if len(backward_timings)>3:
                        backward_timings_ = backward_timings[:3]
                    else:
                        backward_timings_= backward_timings.copy()
                    if len(backward_timings) == 0:
                        backward_timings_.append(-1)
                    if prin[2]:
                        if station == line[-1]:
                            forward_timings_ = [-1]
                        if station == line[0]:
                            backward_timings_ = [-1]
                        return forward_timings_,backward_timings_ 
                    if forward_timings_[0] != -1:
                        for f in range(len(forward_timings_)):
                            forward_timings_[f] = timeconvertor(forward_timings_[f])
                    if backward_timings_[0]!= -1:
                        for b in range(len(backward_timings_)):
                            backward_timings_[b] = timeconvertor(backward_timings_[b])

                    print("-------------------------------------------------------------------------------")
                    if station != line[0] and station != line[-1]:
                        if forward_timings_[0] != -1:
                            print(f"Future metro timings from {station} towards {line[-1]} are at:")
                            for f in forward_timings_:
                                time_printer(f)
                        else:
                            print(f"No train available from {station} towrds {line[-1]} ")
                        if backward_timings_[0]!= -1:
                            print(f"Future metro timings from {station} towards {line[0]} are at:")
                            for b in backward_timings_:
                                time_printer(b)
                        else:
                            print(f"No train available from {station} towrds {line[0]} ")

                    else:
                        if station == line[0]:
                            if forward_timings_[0] != -1:
                                print(f"Future metro timings from {station} towards {line[-1]} are at:")
                                for f in forward_timings_:
                                    time_printer(f)
                            else:
                                print(f"No train available from {station} towrds {line[-1]} ")
                            
                        else:
                            if backward_timings_[0]!= -1:

                                print(f"Future metro timings from {station} towards {line[0]} are at:")
                                for b in backward_timings_:
                                    time_printer(b)
                            else:
                                print(f"No train available from {station} towrds {line[0]} ")

            return metro_timing(station,prin,mutliple,total_minutes) # using recursive method but multiple keeps the track which part has been considered, this is used for interchange stations
    
    if mutliple[1]:
        if station in magentaline:
            line = magentaline.copy()
            time = []
            if station not in magentaline_metrostart:
                
                temp_list = magentaline_metrostart.copy()
                temp_list.append(station)
                temp_list.sort(key = magentaline.index)
                index = magentaline.index(station)
                
                p = temp_list.index(station)
                time.append(timecaluction(magentaline.index(temp_list[p-1]),index,timelist_magentaline))
                time.append(timecaluction(magentaline.index(temp_list[p+1]),index,timelist_magentaline))
            else:
                time.append(0)
                time.append(0)

            if prin[0] == True:
                mutliple[1]=False
            if True:
                if prin[0]:
                    if station != line[0] and station != line[-1]:
                        print(f" Earliest metro can be boarded from {station} towards {line[-1]} at :")
                        time_printer(timeconvertor(time[0]+60*6))
                        print(f" Earliest metro can be boarded from {station} towards {line[0]} at :")
                        time_printer(timeconvertor(time[1]+60*6))
                        print(f" Last metro can be boarded from {station} towards {line[-1]} at :")
                        time_printer(timeconvertor(time[0]+60*23))
                        print(f" Last metro can be boarded from {station} towards {line[0]} at :")
                        time_printer(timeconvertor(time[1]+60*23))
                    else:
                        if station == line[0]:
                            print(f" Earliest metro can be boarded from {station} towards {line[-1]} at :")
                            time_printer(timeconvertor(time[0]+60*6))
                            print(f" Last metro can be boarded from {station} towards {line[-1]} at :")
                            time_printer(timeconvertor(time[0]+60*23))
                        else:
                            print(f" Earliest metro can be boarded from {station} towards {line[0]} at :")
                            time_printer(timeconvertor(time[1]+60*6))
                            print(f" Earliest metro can be boarded from {station} towards {line[0]} at :")
                            time_printer(timeconvertor(time[1]+60*23))
                if prin[1]:
                    forward_freq = []
                    backward_freq = []
                    forward_freq = list(map(lambda x : x + time[0], frequency))
                    backward_freq = list(map(lambda x : x + time[1], frequency))

                    forward_timings = [x for x in forward_freq if x >= int(total_minutes)]
                    backward_timings =[x for x in backward_freq if x >= int(total_minutes)]
                    
                    forward_timings_ = []
                    backward_timings_ = []
                    if len(forward_timings)>3:
                        forward_timings_ = forward_timings[:3]
                    else:
                        forward_timings_ = forward_timings.copy()
                    if len(forward_timings) == 0:
                        forward_timings_.append(-1)
                    if len(backward_timings)>3:
                        backward_timings_ = backward_timings[:3]
                    else:
                        backward_timings_ = backward_timings.copy()
                    if len(backward_timings) == 0:
                        backward_timings_.append(-1)
                    if prin[2]:
                        if station == line[-1]:
                            forward_timings_ = [-1]
                        if station == line[0]:
                            backward_timings_ = [-1]
                        return forward_timings_,backward_timings_ 
                    if forward_timings_[0] != -1:
                        for f in range(len(forward_timings_)):
                            forward_timings_[f] = timeconvertor(forward_timings_[f])
                    if backward_timings_[0]!= -1:
                        for b in range(len(backward_timings_)):
                            backward_timings_[b] = timeconvertor(backward_timings_[b])

                    print("-------------------------------------------------------------------------------")
                    if station != line[0] and station != line[-1]:
                        if forward_timings_[0] != -1:
                            print(f"Future metro timings from {station} towards {line[-1]} are at:")
                            for f in forward_timings_:
                                time_printer(f)
                        else:
                            print(f"No train available from {station} towrds {line[-1]} ")
                        if backward_timings_[0]!= -1:
                            print(f"Future metro timings from {station} towards {line[0]} are at:")
                            for b in backward_timings_:
                                time_printer(b)
                        else:
                            print(f"No train available from {station} towrds {line[0]} ")

                    else:
                        if station == line[0]:
                            if forward_timings_[0] != -1:
                                print(f"Future metro timings from {station} towards {line[-1]} are at:")
                                for f in forward_timings_:
                                    time_printer(f)
                            else:
                                print(f"No train available from {station} towrds {line[-1]} ")
                            
                        else:
                            if backward_timings_[0]!= -1:

                                print(f"Future metro timings from {station} towards {line[0]} are at:")
                                for b in backward_timings_:
                                    time_printer(b)
                            else:
                                print(f"No train available from {station} towrds {line[0]} ")


            return metro_timing(station,prin,mutliple,total_minutes)
    if mutliple[2] :
        if station in bluesideline:
            line = bluesideline.copy()
            time = []
            if station not in bluesideline_metrostart:
                
                temp_list = bluesideline_metrostart.copy()
                temp_list.append(station)
                temp_list.sort(key = bluesideline.index)
                index = bluesideline.index(station)
                
                p = temp_list.index(station)
                time.append(timecaluction(bluesideline.index(temp_list[p-1]),index,timelist_bluesideline))
                time.append(timecaluction(bluesideline.index(temp_list[p+1]),index,timelist_bluesideline))
        
            else:
                time.append(0)
                time.append(0) 

            if prin[0] == True:
                mutliple[2]=False
            if True:
                if prin[0]:
                    if station != line[0] and station != line[-1]:
                        print(f" Earliest metro can be boarded from {station} towards {line[-1]} at :")
                        time_printer(timeconvertor(time[0]+60*6))
                        print(f" Earliest metro can be boarded from {station} towards {line[0]} at :")
                        time_printer(timeconvertor(time[1]+60*6))
                        print(f" Last metro can be boarded from {station} towards {line[-1]} at :")
                        time_printer(timeconvertor(time[0]+60*23))
                        print(f" Last metro can be boarded from {station} towards {line[0]} at :")
                        time_printer(timeconvertor(time[1]+60*23))
                    else:
                        if station == line[0]:
                            print(f" Earliest metro can be boarded from {station} towards {line[-1]} at :")
                            time_printer(timeconvertor(time[0]+60*6))
                            print(f" Last metro can be boarded from {station} towards {line[-1]} at :")
                            time_printer(timeconvertor(time[0]+60*23))
                        else:
                            print(f" Earliest metro can be boarded from {station} towards {line[0]} at :")
                            time_printer(timeconvertor(time[1]+60*6))
                            print(f" Earliest metro can be boarded from {station} towards {line[0]} at :")
                            time_printer(timeconvertor(time[1]+60*23))
                if prin[1]:
                    forward_freq = []
                    backward_freq = []
                    forward_freq = list(map(lambda x : x + time[0], frequency))
                    backward_freq = list(map(lambda x : x + time[1], frequency))

                    forward_timings_ = []
                    backward_timings_ = []

                    forward_timings = [x for x in forward_freq if x >= total_minutes]
                    backward_timings =[x for x in backward_freq if x >= total_minutes]
                    
                    if len(forward_timings)>3:
                        forward_timings_ = forward_timings[:3]
                    else:
                        forward_timings_ = forward_timings.copy()
                    if len(forward_timings) == 0:
                        forward_timings_.append(-1)
                    if len(backward_timings)>3:
                        backward_timings_ = backward_timings[:3]
                    else:
                        backward_timings_ = backward_timings.copy()
                    if len(backward_timings) == 0:
                        backward_timings_.append(-1)
                    if prin[2]:
                        if station == line[-1]:
                            forward_timings_ = [-1]
                        if station == line[0]:
                            backward_timings_ = [-1]
                        return forward_timings_,backward_timings_ 
                    if forward_timings_[0] != -1:
                        for f in range(len(forward_timings_)):
                            forward_timings_[f] = timeconvertor(forward_timings_[f])
                    if backward_timings_[0]!= -1:
                        for b in range(len(backward_timings_)):
                            backward_timings_[b] = timeconvertor(backward_timings_[b])

                    print("-------------------------------------------------------------------------------")
                    if station != line[0] and station != line[-1]:
                        if forward_timings_[0] != -1:
                            print(f"Future metro timings from {station} towards {line[-1]} are at:")
                            for f in forward_timings_:
                                time_printer(f)
                        else:
                            print(f"No train available from {station} towrds {line[-1]} ")
                        if backward_timings_[0]!= -1:
                            print(f"Future metro timings from {station} towards {line[0]} are at:")
                            for b in backward_timings_:
                                time_printer(b)
                        else:
                            print(f"No train available from {station} towrds {line[0]} ")

                    else:
                        if station == line[0]:
                            if forward_timings_[0] != -1:
                                print(f"Future metro timings from {station} towards {line[-1]} are at:")
                                for f in forward_timings_:
                                    time_printer(f)
                            else:
                                print(f"No train available from {station} towrds {line[-1]} ")
                            
                        else:
                            if backward_timings_[0]!= -1:

                                print(f"Future metro timings from {station} towards {line[0]} are at:")
                                for b in backward_timings_:
                                    time_printer(b)
                            else:
                                print(f"No train available from {station} towrds {line[0]} ")
       
def main(): 
    
    blueline, timelist_blueline ,magentaline , timelist_mahentaline , bluesideline , timelist_bluesideline, frequency= data_extraction(file_path)
    print("----------------------------------------------------------------------------------------------------")
    print("----------------------------------------------------------------------------------------------------")
    print("")
    print("                                                                        Blue main line -> line 3")
    print("                                                                        Blue side line -> line 4")
    print("                                                                        Magenta line -> line 8")
    print("WELCOME TO METRO HELPER")
    print("Menu:")
    print("enter 1 for metro line information:")
    print("enter 2 for finding best route:")
    print("enter 3 for metro station information and upcoming metro at the metro station:")
    print('')
    enter = input().strip()
    if not enter.isnumeric():
        print("inavlid input")
        exit()
    enter = int(enter)
    match enter:
        case 1:
            print("Blue main line [line 3] metro stations :")
            for indx,value in enumerate(blueline):
                print(f"{indx+1}. {value.title()}")
            print("Magenta line [line 8] metro stations :")
            for indx,value in enumerate(magentaline):
                print(f"{indx+1}. {value.title()}")
            print("Blue side line [line 4] metro stations :")
            for indx,value in enumerate(bluesideline):
                print(f"{indx+1}. {value.title()}")
        case 2: # activates main1()
            main1()
        case 3:# activates main2()
            main2()
        case _:
            print("invalid input")
    
    
main()