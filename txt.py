def add_record(lst: list):
    """Функция записывает list в txt файл, перед тим отсортировав их по алфавиту"""
    lst.sort()
    f = open("C:/python_test/result.txt", mode="a", encoding="utf-8")
    for i in lst:
        f.write(i+"\n")
    f.close()
