from Classes.Constant import *
import numpy as np


class Helper:
    def get_delta_r(ri, rj) -> float:
        result = abs(rj - ri) / ri * 100
        return result

    def get_delta_a(ai, aj) -> float:
        ai = Utils.rad2deg(ai)
        aj = Utils.rad2deg(aj)
        result = min(abs(ai - aj), 360 - abs(ai - aj)) / 360 * 100
        return result

    def get_delta_b(bi, bj) -> float:
        bi = Utils.rad2deg(bi)
        bj = Utils.rad2deg(bj)
        result = min(abs(bi - bj), 360 - abs(bi - bj)) / 360 * 100
        return result

    def get_delta_d(di, dj) -> float:
        result = abs(dj - di) / di * 100
        return result

    def get_delta_f(r, a, b, d = 0) -> float:
        result = r * WHG_R + a * WHG_A + b * WHG_B
        return result


class Utils:
    def calculate_distance(x1, y1, x2, y2) -> float:
        distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return distance

    def rad2deg(rad) -> float:
        deg = rad * 180 / np.pi
        if deg < 0:
            return 360 + deg
        return deg

    def deg2rad(deg) -> float:
        if deg < 0:
            deg = 360 + deg
        deg = deg % 360
        rad = deg * np.pi / 180
        return rad

    def rotate(point, by, degree=DEGREE) -> tuple:
        x, y, angle = point.x, point.y, point.rad
        # Convert the rotation angle from degrees to radians
        radian = np.deg2rad(by * degree)
        new_x = x * np.cos(radian) - y * np.sin(radian)
        new_y = x * np.sin(radian) + y * np.cos(radian)
        # Update the angle by adding the rotation in radians
        new_angle = angle + radian
        return (new_x, new_y, new_angle)

    def mirror_vertical(point, y) -> tuple:
        return (2 * y - point.x, point.y, np.pi - point.rad)

    def mirror_horizontal(point, x) -> tuple:
        return (point.x, 2 * x - point.y, np.pi - point.rad)

    # alert: this def might be wrong, that's why it's not used
    def find_perpendicular_point(x, y, direction_angle) -> tuple:
        # Calculate the magnitude of the vector
        magnitude = np.sqrt(x**2 + y**2)

        if np.isclose(magnitude, 0):
            raise ValueError("Vector has zero magnitude.")

        # Calculate the coordinates of the point on the line
        px = magnitude * np.cos(direction_angle)
        py = magnitude * np.sin(direction_angle)

        # Verify that the dot product is zero (perpendicular to the vector)
        dot_product = x * px + y * py

        # if np.isclose(dot_product, 0):
        #     return (px, py)
        # else:
        #     raise ValueError("The calculated point is not perpendicular to the vector.")
        return (px, py)

    def find_quadrant(x, y) -> int:
        if x > 0 and y > 0:
            return 1
        elif x < 0 and y > 0:
            return 2
        elif x < 0 and y < 0:
            return 3
        elif x > 0 and y < 0:
            return 3
        else:
            return 0

    def get_z(element):
        return element[2]


    def compare(templates1, templates2) -> bool:
        minutia_value = [] # contains what idx of minutia and number of neighbors are matched if both minutiae matched
        # ? comparing minutia
        for minutia1_index, minutia1 in enumerate(templates1):
            center_value = []
            for minutia2_index, minutia2 in enumerate(templates2):
                if minutia1.type != minutia2.type:
                    continue

                # ? comparing neighbor seeing if minutia1 and minutia2 are the same center
                for neighbor1_index, neighbor1 in enumerate(minutia1.neighbors):
                    neighbor_value = []
                    for neighbor2_index, neighbor2 in enumerate(minutia2.neighbors):
                        if neighbor1[0] != neighbor2[0]:
                            continue

                        delta_r = Helper.get_delta_r(neighbor1[1], neighbor2[1])
                        delta_a = Helper.get_delta_a(neighbor1[2], neighbor2[2])
                        delta_b = Helper.get_delta_b(neighbor1[3], neighbor2[3])
                        if delta_r > T_R or delta_a > T_A or delta_b > T_B:
                            continue
                        delta_f = Helper.get_delta_f(delta_a, delta_r, delta_b)
                        if delta_f > T_DIS:
                            continue
                        
                        # getting every neighbor's Δf for neighbor1 as center
                        neighbor_value.append([neighbor1_index, neighbor2_index, delta_f]) 

                    center_value.append(neighbor_value)
                
                temp = []
                for i in center_value:
                    for j in i:
                        temp.append([j[0], j[1], j[2]])

                # ? Sort based on the third element (Δf) of each sublist
                sorted_data = sorted(temp, key=lambda x: x[2])  

                selected1 = []
                selected2 = []
                number_of_neighbor_matched = 0
                for i in sorted_data:
                    if i[0] not in selected1 and i[1] not in selected2:
                        selected1.append(i[0])
                        selected2.append(i[1])
                        number_of_neighbor_matched += 1
                    elif i[0] in selected1 or i[1] in selected2:
                        continue

                if number_of_neighbor_matched < T_LAMBDA:
                    continue
                
                print(f'MINUTIA {minutia1_index} X MINUTIA {minutia2_index}')
                for i in sorted_data:
                    print(f'index_i:{i[0]}, index_j:{i[1]}, Δf:{i[2]}')
                print(selected1, len(selected1))
                print(selected2, len(selected2))
                print(f'number match:{number_of_neighbor_matched}')
                print()

                minutia_value.append([minutia1_index, minutia2_index, number_of_neighbor_matched])

        for i in minutia_value:
            print(i)
        pass
