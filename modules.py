import datetime


def modules_list(file_withway: str) -> list:
    """Функция получает файл sources.txt и парсит его данные, выдавая лист,
    наполненный сетами - для удобства дальнейшей обработки"""
    f = open(file_withway)
    lst = list()
    modules = set()
    flag = 0
    flag_main = 0
    for line in f:
        if line[:4] == "Name" and flag_main == 0:
            modules.add(line[:(len(line) - 1)])
            flag_main = 1
        if line[:4] == "Date" and flag_main == 1:
            modules.add(line[:(len(line) - 1)])
            flag_main = 2
        if line[:3] == "VCS" and flag_main == 2:
            modules.add(line[:(len(line) - 1)])
            flag_main = 3
        if line[:6] == "Commit" and flag_main == 3:
            modules.add(line[:(len(line)-1)])
            lst.append(modules)
            flag_main = 4
            modules = set()
        if line[:3] == "Dep" and flag == 0:
            modules.add(line[:(len(line)-1)])
            flag = 1
        if line[:3] == "VCS" and flag == 1:
            modules.add(line[:(len(line)-1)])
            flag = 2
        if line[:6] == "Commit" and flag == 2:
            modules.add(line[:(len(line)-1)])
            lst.append(modules)
            modules = set()
            flag = 0
    f.close()
    return lst


def modules_difflist(m_list1: list, m_list2: list) -> tuple:
    """Функция позволяет обработать данные для двух файлов ПО, выявив различия в них и отбросив совпадения,
    в результате выдаёт итоговые данные в tuple, содержащем два элемента - с данными для первого файла
    и с данными для второго файла - толкьо отличные. Дата приведена к формату datetime для возможности её сравнения"""
    # формируем два листа - первый с данными модулей, имеющих отличия от тех же модулей второго, и наоборот
    # листы теперь будут содержать не сеты, а листы данных, а дата будет переведена из типа str в datetime
    diff_file1 = list()
    diff_file2 = list()
    i = 0
    while True:
        symm_diff = m_list1[i].symmetric_difference(m_list2[i])
        if symm_diff != set():
            diff_file1.append(m_list1[i])
            diff_file2.append(m_list2[i])
        i += 1
        if i >= len(m_list1):
            break

    # сформируем дату типа datetime для каждого из файла
    for line in diff_file1[0]:
        if line[:4] == "Date":
            dt_file1 = datetime.date(int(line[12:16]), int(line[9:11]), int(line[6:8]))
    for line in diff_file2[0]:
        if line[:4] == "Date":
            dt_file2 = datetime.date(int(line[12:16]), int(line[9:11]), int(line[6:8]))

# переложим данные в листы: в нужном порядке и с датой типа datetime
    difflist_file1 = list()
    i = 0
    while True:
        lst = list()
        lst.append(dt_file1)
        for line in diff_file1[i]:
            if line[:3] == "Nam":
                lst.append(line[6:])
            if line[:3] == "Dep":
                lst.append(line[5:])
        for line in diff_file1[i]:
            if line[:3] == "VCS":
                x = line.rfind(lst[1])-1
                ll = line[:x]
                y = ll.rfind("/")+1
                lll = ll[y:]
                lst.append(lll)
        for line in diff_file1[i]:
            if line[:6] == "Commit":
                lst.append(line[13:])
        difflist_file1.append(lst)
        i += 1
        if i >= len(diff_file1):
            break

# сделаем то же самое для набора данных второго файла
    difflist_file2 = list()
    i = 0
    while True:
        lst = list()
        lst.append(dt_file2)
        for line in diff_file2[i]:
            if line[:3] == "Nam":
                lst.append(line[6:])
            if line[:3] == "Dep":
                lst.append(line[5:])
        for line in diff_file2[i]:
            if line[:3] == "VCS":
                x = line.rfind(lst[1])-1
                ll = line[:x]
                y = ll.rfind("/")+1
                lll = ll[y:]
                lst.append(lll)
        for line in diff_file2[i]:
            if line[:6] == "Commit":
                lst.append(line[13:])
        difflist_file2.append(lst)
        i += 1
        if i >= len(diff_file2):
            break

    return difflist_file1, difflist_file2
