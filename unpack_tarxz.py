import tarfile
import glob


def tarunpack(main_dir: str, tar_name: str):
    """Функция разархивировывает (ну и слово!) архивы
    и выявляет в созданной папке файл sources.txt с установлением его пути наохждения"""
    # распакуем архив
    tf = tarfile.open(main_dir+tar_name)
    tf.extractall(main_dir+"/unpacked")
    tf.close()

    # найдём в нём пусть к файлу sources.txt
    file = glob.glob(f'{main_dir}/**/sources.txt', recursive=True)
    return file[0]
