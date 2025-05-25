from lxml import etree
import glob

all_file = glob.glob("data/*.xml")

unique = {}
for xml_file in all_file:
    tree = etree.parse(xml_file)

    labels = tree.xpath(f"//@label")

    for label in labels:
        if label in unique:
            unique[label] += 1
        else:
            unique[label] = 1

for (key, value) in unique.items():
    print(f'{key}: {value}')
