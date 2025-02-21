"""
GPT generated - Pie charts without Matplotlib

Using only OpenCV and NumPy
"""
import cv2
import numpy as np


def draw_legend(
    colors,
    labels,
    width=150,
    height=400,
    font_size=0.8,
    text_color=(255, 255, 255),
    padding=40,
    rect_width=20,
    rect_height=20,
    line_height=40,
    thickness=2,
):
    """
    Create a separate legend image that can be hstacked onto the pie chart.

    Parameters:
    - colors: List of colors for each legend entry.
    - labels: List of labels for each legend entry.
    - width: Width of the legend image.
    - font_size: Font size for the text labels in the legend.
    - text_color: Color of the text labels in the legend.

    Returns:
    - The legend image.
    """

    # Create a blank image for the legend
    legend_img = np.zeros((height, width, 3), dtype=np.uint8)

    # Draw each legend entry (colored rectangle and label)
    for i, (label, color) in enumerate(zip(labels, colors)):
        # Draw colored rectangle for each legend entry
        cv2.rectangle(
            legend_img,
            (30, i * line_height + padding),
            (30 + rect_width, i * line_height + rect_height),
            color,
            -1,
        )

        # Draw the text next to the rectangle
        cv2.putText(
            legend_img,
            label,
            (30 + rect_width + 10, i * line_height + 15 + (padding // 2)),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_size,
            text_color,
            thickness,
        )

    return legend_img


def create_pie_chart(
    sizes,
    colors,
    labels=None,
    width=400,
    height=400,
    radius=150,
    text_color=(255, 255, 255),
    font_size=0.8,
    thickness=2,
):
    """
    Create a pie chart (without legend) that can be hstacked with a separate legend image.

    Parameters:
    - labels: List of labels for each slice.
    - sizes: List of values for each slice.
    - colors: List of colors for each slice.
    - width: Width of the output image.
    - height: Height of the output image.
    - radius: Radius of the pie chart slices.
    - text_color: Color of the text labels on the pie chart.
    - font_size: Font size for the labels on the pie chart.

    Returns:
    - The pie chart image (without the legend).
    """
    # Canvas size
    center = (width // 2, height // 2)

    # Create a blank image (dark background for better visibility of pie)
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Calculate the start angle and sweep angle for each slice
    total = sum(sizes)
    angles = np.cumsum([0] + [(size / total) * 360 for size in sizes])
    start_angle = 0

    # Draw each slice
    for i, angle in enumerate(angles[:-1]):
        end_angle = angles[i + 1]
        color = colors[i]
        # Use OpenCV to draw an arc (slice)
        cv2.ellipse(img, center, (radius, radius), 0, start_angle, end_angle, color, -1)

        # Update the start angle for the next slice
        start_angle = end_angle

    if labels is not None:
        # Add text labels to the pie chart
        for i, label in enumerate(labels):
            angle = (
                angles[i] + angles[i + 1]
            ) / 2  # Position in the middle of each slice
            x = int(center[0] + (radius + 20) * np.cos(np.deg2rad(angle)))
            y = int(center[1] + (radius + 20) * np.sin(np.deg2rad(angle)))

            # Draw the label
            cv2.putText(
                img,
                label,
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_size,
                text_color,
                thickness,
            )

    return img


def main():
    # Sample data (you can change this to your data)
    labels = ["A", "B", "C", "D"]
    sizes = [15, 30, 45, 10]  # Corresponding values for each label
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # BGR colors

    # Create the pie chart and legend as separate images
    pie_chart_img = create_pie_chart(labels, sizes, colors)
    legend_img = draw_legend(colors, labels, font_size=0.3)

    # Stack them horizontally
    final_img = np.hstack((pie_chart_img, legend_img))

    # Show the final image
    cv2.imshow("Pie Chart with Legend", final_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
