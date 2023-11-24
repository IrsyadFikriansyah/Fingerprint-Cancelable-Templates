from Classes.KeyCollection import KeyCollection
from Classes.MinutiaCollection import MinutiaCollection
from Classes.Constant import PATH
from Classes.Utils import Utils

file_number = 1
file_name1 = f'{file_number}_1.tif.txt'
file_path1 = f'{PATH}{file_name1}'

mykeys = KeyCollection()

count_match = 0
count = 0
for j in range(1, 101):
    if j == file_number: continue
    file_name2 = f'{j}_2.tif.txt'
    file_path2 = f'{PATH}{file_name2}'

    minutiae1, minutiae2 = MinutiaCollection(), MinutiaCollection()

    minutiae1.make_template(file_path1, mykeys)
    minutiae2.make_template(file_path2, mykeys)
    is_match = Utils.compare(minutiae1.templates, minutiae2.templates)
    if is_match == True:
        count_match += 1
    count += 1
print(f'TESTING FPR for {file_name1}')
print(f'matched: {count_match}')
print(f'not matched: {count - count_match}')