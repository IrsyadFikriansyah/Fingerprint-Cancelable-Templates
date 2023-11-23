from Classes.KeyCollection import KeyCollection
from Classes.MinutiaCollection import MinutiaCollection
from Classes.Constant import PATH
from Classes.Utils import Utils

# file_name1 = '1_1.tif.txt'
# file_path1 = f'{PATH}{file_name1}'

# file_name2 = '1_2.tif.txt'
# file_path2 = f'{PATH}{file_name2}'

mykeys = KeyCollection()
# minutiae1, minutiae2 = MinutiaCollection(), MinutiaCollection()

# minutiae1.make_template(file_path1, mykeys)
# minutiae2.make_template(file_path2, mykeys)

# print(Utils.compare(minutiae1.templates, minutiae2.templates))

count_match = 0
count = 0
# for i in range(1, 101):
for j in range(1, 101):
    file_name1 = f'1_1.tif.txt'
    file_path1 = f'{PATH}{file_name1}'

    file_name2 = f'{j}_1.tif.txt'
    file_path2 = f'{PATH}{file_name2}'

    minutiae1, minutiae2 = MinutiaCollection(), MinutiaCollection()

    minutiae1.make_template(file_path1, mykeys)
    minutiae2.make_template(file_path2, mykeys)
    is_match = Utils.compare(minutiae1.templates, minutiae2.templates)
    if is_match == True:
        count_match += 1
    # print(f'{file_name1}')
    # print(f'{file_name2}')
    # print(f'{is_match}')
    # print()
    count += 1
print(f'jumlah match: {count_match}')
print(f'jumlah not match: {count - count_match}')


