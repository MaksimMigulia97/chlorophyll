
data = {
    "August 2023": "final_data/autumn.csv",
    "June 2023": "final_data/summer.csv",
    "March 2023": "final_data/spring.csv",
    "January 2023": "final_data/winter.csv",
}


depth = [0, -50, -100, -150, -200, -250, -300, -350, -400, -450, -500]


options = [
    {'label': 'August 2023', 'value': data['August 2023']},
    {'label': 'June 2023', 'value': data['June 2023']},
    {'label': 'March 2023', 'value': data['March 2023']},
    {'label': 'January 2023', 'value': data['January 2023']},
]


chlorophyll_coefficients = {
    "depth": [-50, -100, -150, -200, -250, -300, -350, -400, -450, -500],
    "autumn": [1.2, 1.7, 0.9, 0.2, 0.1, 0.05, 0.04, 0.03, 0.02, 0.01],
    "winter": [1.1, 1.5, 0.9, 0.2, 0.1, 0.05, 0.04, 0.03, 0.02, 0.01],
    "spring": [1.2, 1.6, 0.9, 0.2, 0.1, 0.05, 0.04, 0.03, 0.02, 0.01],
    "summer": [1.2, 1.8, 0.9, 0.2, 0.1, 0.05, 0.04, 0.03, 0.02, 0.01],
}


seasons = [
    {'label': 'Spring', 'value': 'spring'},
    {'label': 'Summer', 'value': 'summer'},
    {'label': 'Autumn', 'value': 'autumn'},
    {'label': 'Winter', 'value': 'winter'},
]


MAX_POINTS = 2


columns=[
    {'name': 'Depth (m)', 'id': 'depth'},
    {'name': 'August 2023', 'id': 'August 2023'},
    {'name': 'January 2023', 'id': 'January 2023'},
    {'name': 'March 2023', 'id': 'March 2023'},
    {'name': 'June 2023', 'id': 'June 2023'},
]
