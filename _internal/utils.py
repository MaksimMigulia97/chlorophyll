import pandas as pd
from constants import chlorophyll_coefficients


def get_info_and_table_data(selected_info_text):
    text = selected_info_text.split(',')
    info_dict = {
        'Latitude (°)': text[0].split(':')[-1].strip(),
        'Longitude (°)': text[1].split(':')[-1].strip(),
        'Depth max (m)': text[2].split(':')[-1].strip(),
        'Surface chlorophyll concentration (mg/m³)': text[3].split(':')[-1].strip(),
        'Surface temperature (°C)': text[4].split(':')[-1].strip(),
    }

    table_data = pd.DataFrame(list(info_dict.items()), columns=['Data', 'Value'])
    return table_data


def calculate_chlorophyll(depth, chlorophyll, season):
    if depth > 0:
        return "Depth must be negative and between -500 and -50 with 50m intervals" 
    depth_index = chlorophyll_coefficients["depth"].index(depth)
    
    new_chlorophyll = chlorophyll * chlorophyll_coefficients[season][depth_index]

    return round(new_chlorophyll, 4)
