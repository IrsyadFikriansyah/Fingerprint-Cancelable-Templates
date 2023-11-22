from Classes.KeyCollection import KeyCollection
from Classes.MinutiaCollection import MinutiaCollection
from Classes.Constant import PATH
from Classes.Utils import Utils

file_name1 = '1_1.tif.txt'
file_path1 = f'{PATH}{file_name1}'

file_name2 = '1_2.tif.txt'
file_path2 = f'{PATH}{file_name2}'

mykeys = KeyCollection()
minutiae1, minutiae2 = MinutiaCollection(), MinutiaCollection()

minutiae1.make_template(file_path1, mykeys)
minutiae2.make_template(file_path2, mykeys)

# print(minutiae1.templates.__dict__)
Utils.compare(minutiae1.templates, minutiae2.templates)




# minutiae1.print_data()
# minutiae1.print_transformed()
# minutiae1.print_template()