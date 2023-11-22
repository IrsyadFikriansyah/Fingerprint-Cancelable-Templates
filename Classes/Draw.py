from Classes.Constant import *
import matplotlib.pyplot as plt
import numpy as np


class Draw:
    def compare(filename1, minutiae1, filename2, minutiae2) -> None:
        plt.figure(figsize=(6, 6))
        x1, y1 = [], []
        x2, y2 = [], []

        for minutia1 in minutiae1.minutiae:
            x1.append(minutia1.x)
            y1.append(minutia1.y)

        for minutia2 in minutiae2.minutiae:
            x2.append(minutia2.x)
            y2.append(minutia2.y)

        plt.scatter(x1, y1, color='blue', marker='.')
        plt.scatter(x2, y2, color='red', marker='.')

        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.legend([f'{filename1}', f'{filename2}'], loc="upper right")
        plt.show()

    def point_selection(filename, minutiae) -> None:
        plt.figure(figsize=(6, 6))
        x1, y1 = [], []  # selected
        x2, y2 = [], []  # not selected

        for minutia in minutiae.minutiae:
            if minutia.is_selected:
                x1.append(minutia.x)
                y1.append(minutia.y)
            else:
                x2.append(minutia.x)
                y2.append(minutia.y)

        # ? Draw minutia points
        #  draw farthest point
        plt.scatter(
            minutiae.farthest_points[0].x,
            minutiae.farthest_points[0].y,
            color='red', marker='.'
        )
        plt.scatter(
            minutiae.farthest_points[1].x,
            minutiae.farthest_points[1].y,
            color='red', marker='.'
        )
        # draw selected point
        plt.scatter(
            x1, y1, color='orange', marker='.', label='selected'
        )
        plt.scatter(
            x2, y2, color='purple', marker='.', label='not selected'
        )

        plt.legend(loc="upper right")

        # ? Draw circle
        # Calculate center and radius of the circle
        center = (
            (
                minutiae.farthest_points[0].x +
                minutiae.farthest_points[1].x
            ) / 2,
            (
                minutiae.farthest_points[0].y +
                minutiae.farthest_points[1].y
            ) / 2
        )
        radius = minutiae.farthest_distance / 2

        # Plot the circle
        circle = plt.Circle(center, radius, color='red', fill=False)
        plt.gca().add_patch(circle)
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('point selection')
        plt.show()

    def minutia_center_n(filename, minutiae, index) -> None:
        plt.figure(figsize=(6, 6))
        x1, y1 = [], []

        for minutia in minutiae.minutiae[index].neighbors:
            x1.append(minutia.x)
            y1.append(minutia.y)

        # ? Draw minutia points
        plt.scatter(x1, y1, color='blue', marker='.')
        plt.scatter(0, 0, color='red', marker='.')

        # ? Draw sectors
        for sector in range(SECTOR):
            deg = sector * 360 / SECTOR
            # print(deg)
            angle_radians = np.deg2rad(deg)

            x = minutiae.farthest_distance / 2 * np.cos(angle_radians)
            y = minutiae.farthest_distance / 2 * np.sin(angle_radians)

            # Plot the line from (0,0) to the endpoint (x,y)
            plt.plot([0, x], [0, y], color='red',
                     linestyle='dashed', linewidth=1)

        # ? Draw circle
        # Calculate center and radius of the circle
        center = (0, 0)
        radius = minutiae.farthest_distance / 2

        # Plot the circle
        for i in range(LAYER):
            circle = plt.Circle(
                center, minutiae.layers_dis[i], color='red', fill=False)
            plt.gca().add_patch(circle)

        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title(
            f'{filename}\nindex:{index}; x:{minutiae.minutiae[index].x}, y:{minutiae.minutiae[index].y}')
        plt.show()
