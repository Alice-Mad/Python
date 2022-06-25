import modules
import unpack_tarxz
import bbapi
import json_unpack
import txt
import getpass
import sys


# zip1_dir = input("Введите директорию размещения первого файла для сравнения: ")
# zip1_name = input("Введите название первого файла (название должно заканчиваться на '.tar.xz'): ")
zip1_dir = "C:/python_test/22.09.2022/"
zip1_name = "tas-027-02578.tar.xz"

# распаковываем первый архив и получаем адрес для файла sources.txt первой версии ПО
source1_way = unpack_tarxz.tarunpack(zip1_dir, zip1_name)

# zip2_dir = input("Введите директорию размещения второго файла для сравнения: ")
# zip2_name = input("Введите название второго файла (название должно заканчиваться на '.tar.xz'): ")
zip2_dir = "C:/python_test/02.06.2022/"
zip2_name = "tas-027-03238.tar.xz"

# распаковываем второй архив и получаем адрес для файла sources.txt второй версии ПО
source2_way = unpack_tarxz.tarunpack(zip2_dir, zip2_name)

modules_list1 = modules.modules_list(source1_way)
modules_list2 = modules.modules_list(source2_way)

m = modules.modules_difflist(modules_list1, modules_list2)

dlst_f1 = m[0]
dlst_f2 = m[1]

# создадим пустой файл
f = open("C:/python_test/result.txt", mode="w", encoding="utf-8")
f.close()

# просим залогиниться
username = input("Введите login: ")
password = getpass.getpass(prompt="Введите password: ", stream=sys.stderr)

# дадим запросы и получим файлы json - в том количество, количество модулей которых имело изменения
our_list = list()
i = 0
for lst in dlst_f1:
    if dlst_f1[i] > dlst_f2[i]:
        c1 = dlst_f2[i][3]
        c2 = dlst_f1[i][3]
    else:
        c1 = dlst_f1[i][3]
        c2 = dlst_f2[i][3]
    # запустим функцию запроса в API BB данных и получим обратно помимо файла JSON название новорожденнгоо файла JSON
    file_name = bbapi.bbapi_getjson(lst[2], lst[1], c1, c2, str(i), username, password)
    # теперь вычленим номера ишью из файла, название которого получено выше (уже без повторов)
    our_listpart = json_unpack.jsonunpack(file_name)
    our_list = our_list + our_listpart
    i += 1
# запишем полученный лист в файл
txt.add_record(our_list)
