from lxml import etree
import glob


all_file = glob.glob('data/*.xml')
unique_figure = {}

for xml_file in all_file:
    tree = etree.parse(xml_file)

    all_figure = tree.xpath(f"//image/*")
    for figure in all_figure:
        if figure.tag in unique_figure:
            unique_figure[figure.tag] += 1
        else:
            unique_figure[figure.tag] = 1

for key, value in unique_figure.items():
    print(f'{key}: {value}')
