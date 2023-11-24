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
            return 4
        else:
            return 0

    def get_z(element):
        return element[2]


    def compare(templates1, templates2) -> bool:
        # ? comparing minutia globally
        global_matched = []
        for minutia1_index, minutia1 in enumerate(templates1):
            for minutia2_index, minutia2 in enumerate(templates2):
                if minutia1.type != minutia2.type:
                    continue
                # ? comparing minutia locally
                local_matched = []
                for neighbor1_index, neighbor1 in enumerate(minutia1.neighbors):
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
                        local_matched.append(
                            [neighbor1_index, neighbor2_index, delta_f]
                        )
                
                # ? sort by Δf (ASC)
                local_matched = sorted(local_matched, key=lambda x: x[2])
                # ? matching one to one neighbor
                selected_neighbor1, selected_neighbor2 = [], []
                for i in local_matched:
                    if i[0] not in selected_neighbor1 and i[1] not in selected_neighbor2:
                        selected_neighbor1.append(i[0])
                        selected_neighbor2.append(i[1])
                    else:
                        continue

                if len(selected_neighbor1) < T_LAMBDA: continue
                # print(f'CENTER {minutia1_index} X CENTER {minutia2_index}')
                # print(len(selected_neighbor1))
                # for i in local_matched:
                #     print(i)
                # print(selected_neighbor1)
                # print(selected_neighbor2)
                # print()
                global_matched.append([minutia1_index, minutia2_index, len(selected_neighbor1)])

        # ? sort by number of matched locals (DESC)
        global_matched = sorted(global_matched, key=lambda x: -x[2])
        # ? matching one to one minutia
        selected_minutia1, selected_minutia2 = [], []
        for i in global_matched:
            if i[0] not in selected_minutia1 and i[1] not in selected_minutia2:
                selected_minutia1.append(i[0])
                selected_minutia2.append(i[1])
            else:
                continue
        if len(selected_minutia1) < T_N: 
            return False
        return True

        print(len(selected_minutia1))
        print(selected_minutia1)
        print(selected_minutia2)
        # for i in global_matched:
        #     print(i)
            #     break
            # break
        pass
