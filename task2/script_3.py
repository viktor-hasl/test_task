import json
import os
import shutil

# Пути к файлам
coco_annotation_file = "annotations/updated_annotations.json"  # Файл COCO
yolo_output_dir = "yolo_dataset/"  # Каталог YOLO

# Создаем папку для YOLO
os.makedirs(yolo_output_dir, exist_ok=True)

shutil.copytree('images/', 'yolo_dataset/images' )


# Загружаем COCO аннотации
with open(coco_annotation_file, "r") as f:
    coco_data = json.load(f)

# Получаем категории (COCO ID → YOLO class)
category_map = {cat["id"]: idx for idx, cat in enumerate(coco_data["categories"])}

# Обрабатываем изображения
for image in coco_data["images"]:
    image_name = image["file_name"]
    image_width, image_height = image["width"], image["height"]
    class_folder = image["coco_url"].strip("/")  # Используем COCO URL как каталог

    # Создаем папку для класса
    image_output_folder = os.path.join(yolo_output_dir, class_folder)
    os.makedirs(image_output_folder, exist_ok=True)

    # Создаем файл аннотации YOLO
    yolo_annotation_file = os.path.join(image_output_folder, image_name.replace(".jpg", ".txt").replace(".png", ".txt"))

    with open(yolo_annotation_file, "w") as f:
        for annotation in coco_data["annotations"]:
            if annotation["image_id"] == image["id"]:
                category_id = category_map[annotation["category_id"]]
                bbox = annotation["bbox"]

                # Нормализуем координаты
                x_center = (bbox[0] + bbox[2] / 2) / image_width
                y_center = (bbox[1] + bbox[3] / 2) / image_height
                width = bbox[2] / image_width
                height = bbox[3] / image_height

                # Записываем в YOLO формат
                f.write(f"{category_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

print("Конвертация завершена! YOLO-аннотации сохранены в", yolo_output_dir)

