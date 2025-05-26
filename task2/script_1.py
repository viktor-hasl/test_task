import json
import os
import shutil


with open('annotations/instances_train.json', 'r') as f:
    annotations = json.load(f)


imgs = {}
# Перебираем аннотации
for annot in annotations['annotations']:
    # Добавляем id картинки в словарь, если его нет, со значением категории
    if not annot['image_id'] in imgs.keys():
        category_name = next(
            (category["name"] for category in annotations['categories'] if category['id'] == annot['category_id']),
            None
        )
        imgs[annot['image_id']] = [category_name]
    else:
        category_name = next(
            (category["name"] for category in annotations['categories'] if category['id'] == annot['category_id']),
            None
        )
        if not category_name in imgs[annot['image_id']]:
            imgs[annot['image_id']] = imgs[annot['image_id']] + [category_name]



for img_annotation in annotations['images']:
    if img_annotation['id'] in imgs.keys():
        name_folder = '_'.join(sorted(imgs[img_annotation['id']]))
        name_file = img_annotation['file_name']
        img_annotation['file_name'] = 'images/' + name_folder + '/'
        if not os.path.exists(img_annotation['file_name']):
            os.makedirs(img_annotation['file_name'])
        try:
            shutil.move('images/train/' + name_file, img_annotation['file_name'])
        except shutil.Error:
            print(f"Файл {img_annotation['file_name']} уже есть")
        img_annotation['file_name'] += name_file
    else:
        name_file = img_annotation['file_name']
        img_annotation['file_name'] = 'images/'
        try:
            shutil.move('images/train/' + name_file, img_annotation['file_name'])
        except shutil.Error:
            print(f"Файл {img_annotation['file_name']} уже есть")
        img_annotation['file_name'] += name_file


with open('annotations/updated_annotations.json', 'w', encoding='utf-8') as file:
    json.dump(annotations, file,  ensure_ascii=False, indent=4)