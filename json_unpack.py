# import codecs

def jsonunpack(f_name: str) -> list:
    """Функция находит в файле json номера ишью и упаковывает их в list"""
    f = open(f"C:/python_test/{f_name}", encoding="utf-8", errors="ignore")
    # f = open("C:/python_test/api_result.json", encoding="utf-8, errors="ignore")

    flag = 0
    lst = list()
    for line in f:
        if line.find("jira-key") != (-1):
            flag = 1
            continue
        if flag == 1:
            x = line.find('"')
            y = line.find('"', x+1)
            issue_n = line[x+1:y]
            lst.append(issue_n)
            flag = 0
    lst = list(set(lst))
    f.close()
    return lst
