from Classes.Constant import *
from Classes.Utils import Utils
from Classes.Minutia import Minutia
from Classes.Template import Template
import numpy as np


class MinutiaCollection:
    def __init__(self):
        self.minutiae = []
        self.farthest_points = ()
        self.farthest_distance = 0
        self.layers_dis = []
        self.transformed_minutiae = []
        self.templates = [] # contains collection of templates for every minutia

    def _import_data(self, file_path) -> None:
        with open(file_path, 'r') as file:
            for line in file:
                # Split the line into its four parts
                parts = line.split()

                # Check if there are exactly four parts
                if len(parts) == 4:
                    # Parse and store the values
                    x = float(parts[0])
                    y = float(parts[1])
                    radian = float(parts[2])
                    type = parts[3]
                    minutia = Minutia(x, y, radian, type)
                    self.minutiae.append(minutia)

    def _point_selection(self, number_of_layer=LAYER) -> None:
        # getting the farthest 2 point
        for i in range(len(self.minutiae)):
            for j in range(i + 1, len(self.minutiae)):
                x1, y1 = self.minutiae[i].x, self.minutiae[i].y
                x2, y2 = self.minutiae[j].x, self.minutiae[j].y
                dis = Utils.calculate_distance(x1, y1, x2, y2)
                if dis > self.farthest_distance:
                    self.farthest_distance = dis
                    self.farthest_points = (self.minutiae[i], self.minutiae[j])

        # getting center point & radius
        center = (
            (self.farthest_points[0].x +
             self.farthest_points[1].x) / 2,
            (self.farthest_points[0].y +
             self.farthest_points[1].y) / 2
        )
        radius = self.farthest_distance / 2

        # selecting minutia (outside radius => not selected)
        for minutia in self.minutiae:
            xi, yi = minutia.x, minutia.y
            dis = Utils.calculate_distance(*center, xi, yi)
            if dis <= radius:
                minutia.is_selected = True

        # storring every layer's lenght
        for i in range(number_of_layer):
            self.layers_dis.append(
                self.farthest_distance * (i + 1) /
                number_of_layer / 2
            )

    # adding neighbor data for each minutia
    def _process_neighbor(self) -> None:
        neighbors = []
        for i in self.minutiae:
            neighbor = []
            for j in self.minutiae:
                if i == j:
                    continue

                x1, y1, a1 = i.x, i.y, i.rad
                x2, y2, a2 = j.x, j.y, j.rad

                # ? centralize the minutia i
                new_x2 = x2 - x1
                new_y2 = y2 - y1
                # ! a is already on radian, so no need to convert!
                new_x = new_x2 * np.cos(a1) + new_y2 * np.sin(a1)
                new_y = -new_x2 * np.sin(a1) + new_y2 * np.cos(a1)
                new_a = a2 - a1

                neighbor.append(Minutia(new_x, new_y, new_a, j.type))
            neighbors.append(neighbor)

        # adding the added neighbors data
        index = 0
        for minutia in self.minutiae:
            if minutia.is_selected == False:
                continue
            minutia.neighbors = neighbors[index]
            index += 1

    def _get_points_in_layer_sector(self, neighbors, layer, sector) -> list:
        points = []
        for neighbor in neighbors:
            distance = Utils.calculate_distance(0, 0, neighbor.x, neighbor.y)
            # if distance > self.layers_dis[layer - 1] and distance <= self.layers_dis[layer]:
            if layer == 0:
                low = 0
            else:
                low = self.layers_dis[layer - 1]
            high = self.layers_dis[layer]
            if low < distance <= high:
                # Calculate the angle theta
                theta = np.arctan2(neighbor.y, neighbor.x)
                # Normalize the angle to fall between 0 and 360 degrees
                theta_normalized = np.mod(theta, 2 * np.pi)
                # Determine the quadrant
                quadrant = np.floor(theta_normalized /
                                    (2 * np.pi / SECTOR))

                if quadrant == sector:
                    points.append(neighbor)

        return points

    def _transform(self, mykey) -> None:
        transformed_list = []
        for i in range(len(self.minutiae)):
            if self.minutiae[i].is_selected is False:
                continue
            center_i = Minutia(
                self.minutiae[i].x,
                self.minutiae[i].y,
                self.minutiae[i].rad,
                self.minutiae[i].type
            )

            # ? iterate every neighbor in layer - range order
            for layer in range(LAYER):  # i
                for sector in range(SECTOR):  # j

                    # ? getting minutia(e) in layer i and sector j
                    point_list = self._get_points_in_layer_sector(
                        self.minutiae[i].neighbors,
                        layer,
                        sector
                    )

                    # ? skip in no minutia
                    if len(point_list) == 0:
                        continue

                    # ? get key for layer i and sector j
                    key_rotate = mykey.key[layer][sector][0]
                    key_x = mykey.key[layer][sector][1]
                    key_y = mykey.key[layer][sector][2]

                    # ? transform every minutia(e) in layer i sector j
                    for minutia in point_list:
                        new_minutia = Minutia(
                            *Utils.rotate(minutia, key_rotate),
                            minutia.type
                        )
                        new_minutia = Minutia(
                            *Utils.mirror_vertical(new_minutia, key_x), minutia.type
                        )
                        new_minutia = Minutia(
                            *Utils.mirror_horizontal(new_minutia, key_y), minutia.type
                        )

                        center_i.neighbors.append(new_minutia)
            transformed_list.append(center_i)
        self.transformed_minutiae = transformed_list

    def print_data(self) -> None:
        n = 1
        for minutia in self.minutiae:
            print(f'MINUTIA #{n}')
            print('x\t:', minutia.x)
            print('y\t:', minutia.y)
            print('rad\t:', minutia.rad)
            print('type\t:', minutia.type)
            print('selected :', minutia.is_selected)
            count = 1
            print('neigbors :')
            for neighbor in minutia.neighbors:
                print(
                    f'{str(count).rjust(3)}. {str(neighbor.x).rjust(20)}, {str(neighbor.y).rjust(20)}, {str(neighbor.rad).rjust(20)}')
                count += 1
            print()
            n += 1

    def print_transformed(self) -> None:
        n = 1
        for minutia in self.transformed_minutiae:
            print(f'MINUTIA #{n}')
            print('x\t:', minutia.x)
            print('y\t:', minutia.y)
            print('rad\t:', minutia.rad)
            print('type\t:', minutia.type)
            print('selected :', minutia.is_selected)
            count = 1
            print('neigbors :')
            for neighbor in minutia.neighbors:
                print(
                    f'{str(count).rjust(3)}. {str(neighbor.x).rjust(20)}, {str(neighbor.y).rjust(20)}, {str(neighbor.rad).rjust(20)}')
                count += 1
            print()
            n += 1

    def print_template(self) -> None:
        n = 1
        for template in self.templates:
            print(f'TEMPLATE MINUTIA #{n}')
            print('type\t:', template.type)
            count = 1
            print('neigbors :')
            for neighbor in template.neighbors:
                print(
                    f'{str(count).rjust(3)}. {str(neighbor[0]).rjust(1)}, {str(neighbor[1]).rjust(20)}, {str(neighbor[2]).rjust(20)}, {str(neighbor[3]).rjust(20)}, {str(neighbor[4]).rjust(20)}')
                count += 1
            print()
            n += 1


    def _process_representation(self) -> None:
        features = []
        for minutia in self.transformed_minutiae:
            feature = Template(minutia.type)
            for neighbor in minutia.neighbors:
                x, y = neighbor.x, neighbor.y
                elucidian = Utils.calculate_distance(x, y, 0, 0)
                alpha = np.arctan2(y, x)
                quadrant = Utils.find_quadrant(x, y)
                if (quadrant == 1 or quadrant == 3):
                    beta = Utils.rad2deg(neighbor.rad) % 180 - \
                        Utils.rad2deg(alpha) % 180
                elif (quadrant == 1 or quadrant == 3):
                    beta = Utils.rad2deg(alpha) % 180 - \
                        Utils.rad2deg(neighbor.rad) % 180
                else:
                    beta = 0
                beta = Utils.deg2rad(beta)
                m = np.tan(neighbor.rad)
                b = neighbor.y - (m * neighbor.x)
                d = -b / np.sqrt(m**2 + 1)
                feature.neighbors.append((neighbor.type, elucidian, alpha, beta, d))
            features.append(feature)
        self.templates = features

    def make_template(self, file_path, mykey):
        self._import_data(file_path)
        self._point_selection()
        self._process_neighbor()
        self._transform(mykey)
        self._process_representation()
