
import csv
from bokeh.plotting import figure, output_file, show

blood_pressure_file = 'blood-pressure.csv'

avgs = []

def get_avgs(array):
    systole, diastole, hr = 0, 0 , 0
    for i in array:
        s, d, h = i.split('/')
        systole += int(s)
        diastole += int(d)
        hr += int(h)
    systole = int(systole/3)
    diastole = int(diastole/3)
    hr = int(hr/3)
    return systole, diastole, hr


with open(blood_pressure_file, newline='') as f:
    reader = csv.reader(f, delimiter=' ', quotechar='|')
    next(reader)
    for row in reader:
        row = row[0]
        row = row.split(',')
        wrists = row[1:4]
        wrist_avg = get_avgs(wrists)
        hands = row[4:]
        hand_avg = get_avgs(hands)
        data = [row[0], list(wrist_avg), list(hand_avg)]
        avgs.append(data)

for line in avgs:
    print(line)

avgs.pop(0)
avgs.pop(0)


x_line = list(range(len(avgs)))
wrist_sys = [i[1][0] for i in avgs]
wrist_dia = [i[1][1] for i in avgs]
wrist_hr = [i[1][2] for i in avgs]

hand_sys = [i[2][0] for i in avgs]
hand_dia = [i[2][1] for i in avgs]


output_file("patch.html")

p = figure(plot_width=400, plot_height=400)

p.multi_line([x_line, x_line, x_line, x_line, x_line], [wrist_sys, wrist_dia, wrist_hr, hand_sys, hand_dia],
             color=["firebrick", "navy", 'black', 'orange', 'green'], alpha=[0.8, 0.3, 1, 0.8, 0.3], line_width=4)

show(p)
