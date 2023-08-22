import sys
from pathlib import Path

JPEG_IMAGES = []
JPG_IMAGES = []
SVG_IMAGES = []
PNG_IMAGES = []
MP3_AUDIO = []
MY_OTHER = []
ARCHIVES = []

REGISTER_EXTENSIONS = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'SVG': SVG_IMAGES,
    'PNG': PNG_IMAGES,
    'MP3': MP3_AUDIO,
    'ZIP': ARCHIVES,
}

FOLDERS = []
EXTENSION = set()
UNKNOWN = set()

def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()

def scan(folder: Path) -> None:
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item) #Сканируем вложенную папку. Рекурсия
            continue #переходим к следующему элементу в папке
    #работа с файлом 
        ext = get_extension(item.name) #получаем расширение файла
        fullname = folder / item.name #получаем путь к файлу
        if not ext: #если расширение не определенно
            MY_OTHER.append(fullname)
        else:
            try:            
                container = REGISTER_EXTENSIONS[ext] #получаем конетейнер для расширения
                EXTENSION.add(ext)
                container.append(fullname)
            except KeyError:
                #если расширение не зарегистрировано в REGISTER_EXTENSIONS - добавляем в неизвестное
                UNKNOWN.add(ext)
                MY_OTHER.append(fullname)

    if __name__ == '__main__':
        folder_to_scan = sys.argv[1]
        print(f'Start in folder: {folder_to_scan}')
        scan(Path(folder_to_scan))
        print(f'Images: {JPEG_IMAGES}')
        print(f'Archives: {ARCHIVES}')
        print(f'Audio: {MP3_AUDIO}')
        print(f'Documents: {ARCHIVES}')
        print(f'Other: {MY_OTHER}')
        print(f'Unknown: {UNKNOWN}')
        print(f'Images SVG: {SVG_IMAGES}')
        print(f'Images PNG: {PNG_IMAGES}')
        print(f'Images JPG: {JPG_IMAGES}')

        print(f'Types of files in folder: {EXTENSION}')
        print(FOLDERS [::-1])