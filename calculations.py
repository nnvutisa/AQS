from math import floor
import numpy as np

def get_breakpoint(pollutant,value):
    breakpoint_table = {
        'Ozone':[[0.,0.054],[0.055,0.070],[0.071,0.085],[0.086,0.105],[0.106,0.2],[0.405,0.504],[0.505,0.604]],
        'PM 2.5':[[0.,12.],[12.1,35.4],[35.5,55.4],[55.5,150.4],[150.5,250.4],[250.5,350.4],[350.5,500.4]],
        'PM 10':[[0.,54.],[55.,154.],[155.,254.],[255.,354.],[355.,424.],[425.,504.],[505.,604.]],
        'Carbon monoxide':[[0.,4.4],[4.5,9.4],[9.5,12.4],[12.5,15.4],[15.5,30.4],[30.5,40.4],[40.5,50.4]],
        'Sulfur dioxide':[[0.,35.],[36.,75.],[76.,185.],[186.,304.],[305.,604.],[605.,804.],[805.,1004.]],
        'Nitrogen dioxide':[[0.,53.],[54.,100.],[101.,360.],[361.,649.],[650.,1249.],[1250.,1649.],[1650.,2049.]]
    }
    aqi = [[0.,50.],[51.,100.],[101.,150.],[151.,200.],[201.,300.],[301.,400.],[401.,500.]]
    breakpoint = {}
    for i in range(7):
        BP_low = breakpoint_table[pollutant][i][0]
        BP_high = breakpoint_table[pollutant][i][1]
        if (BP_low <= value)and(value <= BP_high):
            breakpoint['BP_low'] = BP_low
            breakpoint['BP_high'] = BP_high
            breakpoint['I_low'] = aqi[i][0]
            breakpoint['I_high'] = aqi[i][1]
    if not breakpoint:
        raise Exception('Value of the pollutant does not correspond to any level')
    return breakpoint

def calculate_aqi(pollutants):
    #pollutants should be a list in this order: Ozone, PM2.5, PM10, CO, SO2, NO2
    #missing polutants should have values as NaN
    pollutant_name = ['Ozone','PM 2.5','PM 10','Carbon monoxide','Sulfur dioxide','Nitrogen dioxide']
    aqi_list = []
    
    #truncate the values
    if not np.isnan(pollutants[0]): pollutants[0] = int(pollutants[0]*1000)/1000.
    if not np.isnan(pollutants[1]): pollutants[1] = int(pollutants[1]*10)/10.
    if not np.isnan(pollutants[2]): pollutants[2] = floor(pollutants[2])
    if not np.isnan(pollutants[3]): pollutants[3] = int(pollutants[3]*10)/10.
    if not np.isnan(pollutants[4]): pollutants[4] = floor(pollutants[4])
    if not np.isnan(pollutants[5]): pollutants[5] = floor(pollutants[5])
    
    #calculate aqi for each pollutant
    for i,pollutant in enumerate(pollutants):
        if not np.isnan(pollutant):
            breakpoint = get_breakpoint(pollutant_name[i],pollutant)
            aqi = int(((breakpoint['I_high']-breakpoint['I_low'])/(breakpoint['BP_high']-breakpoint['BP_low'])* 
                   (float(pollutant)-breakpoint['BP_low'])+breakpoint['I_low']))
        else:
            aqi = np.NAN
        aqi_list.append(aqi)
    return aqi_list
