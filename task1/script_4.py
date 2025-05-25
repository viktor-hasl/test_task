import xml.etree.ElementTree as ET
import glob
from pathlib import Path


all_file = glob.glob('data/*.xml')


for xml_file in all_file:
    tree = ET.parse(xml_file)
    root = tree.getroot()

    all_image = root.findall('image')
    # Проходим по каждому элементу и меняем нужные данные
    for elem in root.iter('image'):
        name_img = elem.attrib['name'].split('/')[-1]
        new_extension = name_img.split('.')[0] + '.png'
        elem.set('name', new_extension)

        id_image = elem.attrib['id']

        elem.set('id', str(len(all_image) - int(id_image) -1))

    # Сохранение в файл в выбраный путь
    if not Path("data_modified").exists():
        Path("data_modified").mkdir(exist_ok=True)

    name_file = xml_file.split('\\')[1][:-4] + '_modified.xml'
    tree.write('data_modified/' + name_file)




