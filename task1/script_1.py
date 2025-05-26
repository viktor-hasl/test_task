from lxml import etree
import glob
# Получвем все xml файлы
all_file = glob.glob("data/*.xml")


count_all_img = 0
count_marked_img = 0
count_nomarked_img = 0
count_all_figures = 0
max_s = 0
min_s = 0

# Проходим по каждому файлу и получаем нужные нам значения
for file in all_file:
    xml_file = file
    tree = etree.parse(xml_file)
    root = tree.getroot()

    for elem in root.findall('image'):
        count_all_img += 1

        if len(elem) > 0:
            count_all_figures += len(elem)
            count_marked_img += 1
        else:
            count_nomarked_img += 1
        # Ищим самое боьлше и маленькое изображение
        width = int(elem.attrib['width'])
        height = int(elem.attrib['height'])
        if width * height >= max_s:

            max_img = elem
            max_s = width * height
        if width * height <= min_s or min_s == 0:

            min_img = elem
            min_s = width * height



count_max_img = 0
count_min_img = 0
# Проходим по всем файлам и считаем сколько самых больших и маленьких картинок
for file in all_file:
    xml_file = file
    tree = etree.parse(xml_file)
    root = tree.getroot()
    count_max_img += len(tree.xpath(f"//image[@width={max_img.attrib['width']} and @height={max_img.attrib['height']}"
                                    f" or @width={max_img.attrib['height']} and @height={max_img.attrib['width']} ]"))
    count_min_img += len(tree.xpath(f"//image[@width={min_img.attrib['width']} and @height={min_img.attrib['height']}"
                                    f" or @width={min_img.attrib['height']} and @height={min_img.attrib['width']} ]"))


print('Общее количество изображений: ' + str(count_all_img))
print('Количество размеченных изображений: ' + str(count_marked_img))
print('Количество неразмеченных изображений: ' + str(count_nomarked_img))
print('Количество всех фигур: ' + str(count_all_figures))

print(f'\nСамое большое изображения: {max_img.attrib["width"]}x{max_img.attrib["height"]}\nИмя: {max_img.attrib["name"]}\n({count_max_img} шт.)')
print(f'\nСамое маленькое изображения: {min_img.attrib["width"]}x{min_img.attrib["height"]}\nИмя: {min_img.attrib["name"]}\n({count_min_img} шт.)')






