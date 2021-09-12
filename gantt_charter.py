from calendar import monthrange, month_name
from datetime import date
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TKAgg')
fig, ax = plt.subplots(figsize=(8, 8))

box_height, box_spacing = 10, 5
def rgb_squasher(fst, snd, trd): return (fst / 255.0, snd / 255.0, trd / 255.0)

events = [
    (
        "Non-Overlap (O0)", 
        [((2020, 10, 1), (2021, 1, 1)), ((2021, 4, 5), (2021, 4, 11)), ((2021, 5, 31), (2021, 8, 31))], 
        "red"
    ),
    
    (
        "Drift Correction (O0)",
        [((2021, 1, 1), (2021, 4, 3)), ((2021, 9, 1), (2021, 10, 31))],
        "orange"
    ),
    
    (
        "Simulation Experiments (O1)",
        [((2021, 4, 11), (2021, 5, 30)), ((2021, 11, 1), (2022, 7, 31))],
        rgb_squasher(255, 255, 0)
    ),
    
        (
            "Noise Experiments (O1.1)",
            [((2021, 4, 11), (2021, 5, 30)), ((2021, 11, 1), (2022, 1, 31))],
            rgb_squasher(255, 230, 0)
        ),
        
        (
            "Extend Benchmarking (O1.2)",
            [((2022, 2, 1), (2022, 2, 28))],
            rgb_squasher(255, 230, 0)
        ),
        
        (
            "Urgency Experiments (O1.3)",
            [((2022, 3, 1), (2022, 5, 31))],
            rgb_squasher(255, 230, 0)
        ),
        
        (
            "Simple Implementation (O1.4)",
            [((2022, 6, 1), (2022, 7, 31))],
            rgb_squasher(255, 230, 0)
        ),
    
    (
        "Peak-Picking (O2)",
        [((2022, 8, 1), (2023, 3, 31))],
        rgb_squasher(0, 196, 0)
    ),
    
        (
            "Build Classifer (O2.1)",
            [((2022, 8, 1), (2022, 9, 30))],
            rgb_squasher(0, 128, 0)
        ),
    
        (
            "Extend Classifier (O2.2)",
            [((2022, 10, 1), (2023, 1, 31))],
            rgb_squasher(0, 128, 0)
        ),
    
        (
            "Validate Classifer (O2.3)",
            [((2023, 2, 1), (2023, 3, 31))],
            rgb_squasher(0, 128, 0)
        ),
    
    (
        "Further Peak-Picking (O3)",
        [((2023, 4, 1), (2023, 9, 30))],
        "blue"
    ),
    
    (
        "PhD Thesis",
        [((2023, 10, 1), (2024, 3, 31))],
        "purple"
    ),
]

events = [(name, [(date(*start), date(*end)) for start, end in dates], colour) for name, dates, colour in events]
min_date = min(date for e in events for datelist in e[1] for date in datelist)
max_date = max(date for e in events for datelist in e[1] for date in datelist)
def dist(date): return (date - min_date).days
events = [(name, [(dist(start), dist(end) - dist(start)) for start, end in dates], colour) for name, dates, colour in events]

for i, (name, dates, colour) in enumerate(events):
    ax.broken_barh(dates, ((len(events) - i) * (box_spacing + box_height), box_height), facecolors=colour)

for i, year in enumerate(range(min_date.year + 1, max_date.year)): 
    x = dist(date(year, 6, 30))
    ax.plot([x, x], [0, (len(events) + 2) * (box_spacing + box_height)], color="black")
    ax.text(x + 5, (len(events) + 1.5) * (box_spacing + box_height), f"End of Year {i+1}", color="black")
    
no_days, month_names = [0], []
for year in range(min_date.year, max_date.year + 1):
    min_month = min_date.month if year == min_date.year else 1
    max_month = max_date.month if year == max_date.year else 12
    for month in range(min_month, max_month + 1): 
        no_days.append(monthrange(year, month)[1])
        month_names.append(month_name[month][:3])
month_names.append(month_name[max_date.month % 12 + 1][:3])

ax.set_xticks(np.cumsum([no_days]))
ax.set_xticklabels(month_names)
ax.set_yticks([(len(events) - i) * (box_spacing + box_height) + box_height / 2.0 for i in range(len(events))])
ax.set_yticklabels([name for name, _, __ in events])
ax.set_title("Planned Timeline")
ax.set_ylim(ymin=0, ymax=(len(events) + 2) * (box_spacing + box_height))
ax.set_xlim(xmin=0, xmax=sum(no_days))
 
plt.show()
#plt.savefig(os.path.join(os.getcwd(), "apr_gantt.png"))