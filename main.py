import csv
import os
import time
from collections import defaultdict

import cv2
import numpy as np
from ops import OPS
from pie_chart import create_pie_chart, draw_legend

# localize for less typing
FONT = cv2.FONT_HERSHEY_SIMPLEX

# seed for static colors
np.random.seed(2)
# generated a rendom color for each operation
COLORS = [np.random.randint(0, 255, size=(3,)).tolist() for _ in OPS]


def from_iso_date(date):
    """
    returns unix epoch given YYYY-MM-DD
    """
    return int(time.mktime(time.strptime(str(date), "%Y-%m-%d")))


def group_into_other(sizes, labels, threshold=1):
    """
    given the sizes and labels of a pie chart, groups all slices under 
    "threshold" percent into one "Other" category
    """
    # Normalize the sizes to percentages
    total = sum(sizes)
    percentages = [size / total * 100 for size in sizes]

    new_labels = []
    new_values = []
    other_value = 0

    for label, percentage, size in zip(labels, percentages, sizes):
        if percentage < threshold:
            # Keep the raw size for the 'Other' slice
            other_value += size
        else:
            new_labels.append(label)
            new_values.append(size)

    # If there were any small slices, add the 'Other' label
    if other_value > 0:
        new_labels.append("Other")
        new_values.append(other_value)

    return (
        new_values,
        new_labels,
        # get the color for each label, grey if Other
        [COLORS[OPS.index(i)] if i != "Other" else (50, 50, 50) for i in new_labels],
    )


def build_header(date):
    """
    make a header image (to be vstacked onto the pie charts)
    composed roughly as thus:

                            Bitshares Operations as of 2025-02-03

                    This Week                              Cumulative to Now

    """
    # make a black image
    header = np.zeros((200, 400 * 4, 3)).astype(np.uint8)
    
    # add some text
    cv2.putText(
        header,
        f"BitShares Operations as of {date}",
        (800-(cv2.getTextSize(f"BitShares Operations as of {date}", FONT, 0.7, 2)[0][0]//2), 50),
        FONT,
        0.7,
        (255, 255, 255),
        2,
    )
    cv2.putText(
        header,
        "This Week",
        (400-(cv2.getTextSize("This Week", FONT, 0.7, 2)[0][0]//2), 100),
        FONT,
        0.7,
        (255, 255, 255),
        2,
    )
    cv2.putText(
        header,
        "Cumulative to Now",
        (1200-(cv2.getTextSize("Cumulative to Now", FONT, 0.7, 2)[0][0]//2), 100),
        FONT,
        0.7,
        (255, 255, 255),
        2,
    )
    return header


def main():
    # clear terminal
    print("\033c")

    # grab the csv from kibana and format it into a list of lists
    data = []
    with open("weekly bitshares ops count.csv") as handle:
        reader = csv.reader(handle)
        for row in reader:
            data.append(row)
            
    # remove the column names
    data = data[1:]

    # all we really need is the date and count, they are already in order by op id
    data = [
        [
            i[1],
            int(i[2].replace(",", "")) if i[2] != "-" else 0,
        ]
        for i in data
    ]

    # put each count into a dictionary keyed by date
    dated_data = defaultdict(list)
    for i in data:
        dated_data[i[0]].append(i[1])

    # make a numpy array out of each key
    # (by far faster that using np.append in the previous step)
    dated_data = {k: np.array(v) for k, v in dated_data.items()}

    # cumulative sizes
    c_sizes = None

    # mp4 video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    # yes, i'm aware 1600x600 is a non-standard resolution, but it grids out nicely
    out = cv2.VideoWriter("out.mp4", fourcc, 30, (1600, 600))

    for date, sizes in dated_data.items():
        # print progess
        print("\033[A", date)

        # if there is no data (i.e. before anything happened)
        if not np.sum(sizes):
            # skip this frame
            continue

        if c_sizes is None:
            # initialize the cumulative pie chart
            c_sizes = sizes
        else:
            # or add the current slices to them
            c_sizes += sizes

        # group any small slices in the cumulative and weekly sections into "Other"
        grouped_c_sizes, grouped_c_labels, c_colors = group_into_other(
            c_sizes, OPS, 0.5
        )
        grouped_sizes, grouped_labels, colors = group_into_other(sizes, OPS, 0.5)

        # make two pie charts and legends
        c1 = create_pie_chart(grouped_sizes, colors)
        l1 = draw_legend(colors, grouped_labels, width=400, font_size=0.7)

        c2 = create_pie_chart(grouped_c_sizes, c_colors)
        l2 = draw_legend(c_colors, grouped_c_labels, width=400, font_size=0.7)

        # and the header
        header = build_header(date)

        # stack the pie charts with their legends, and stack the header on that
        frame = np.vstack((header, np.hstack((l1, c1, c2, l2))))

        # write the frame to the video writer
        out.write(frame)

    # close the pipe
    out.release()


if __name__ == "__main__":
    main()
