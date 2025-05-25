import json
import os
import shutil


with open('annotations/instances_train.json', 'r') as f:
    annotations = json.load(f)


imgs = {}
for annot in annotations['annotations']:
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
        img_annotation['coco_url'] = 'images/' + name_folder + '/'
        if not os.path.exists(img_annotation['coco_url']):
            os.makedirs(img_annotation['coco_url'])
        try:
            shutil.move('images/train/' + img_annotation['file_name'], img_annotation['coco_url'])
        except shutil.Error:
            print(f"Файл {img_annotation['file_name']} уже есть")
    else:
        img_annotation['coco_url'] = 'images/'
        try:
            shutil.move('images/train/' + img_annotation['file_name'], img_annotation['coco_url'])
        except shutil.Error:
            print(f"Файл {img_annotation['file_name']} уже есть")


with open('annotations/updated_annotations.json', 'w', encoding='utf-8') as file:
    json.dump(annotations, file,  ensure_ascii=False, indent=4)