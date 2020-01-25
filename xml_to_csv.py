import xml.etree.ElementTree as ET
import os
import numpy as np
import csv

DATASET_DIR = 'all_data/'

WHITELIST = ["man", "woman", "table", "side_table", "chair", "towel",
		"bottle", "picture", "painting", "plant", "mirror"]

mypath = os.path.dirname(os.path.abspath(__file__))
print(mypath)
annotations = []
classes = set([])

# coe = [f for f in os.listdir(DATASET_DIR) if f.endswith(".xml")]
# print(coe)

print("[INFO] Pegando annotations...")
for xml_file in [f for f in os.listdir(DATASET_DIR) if f.endswith(".xml")]:
	coe = os.path.join(DATASET_DIR, xml_file)
	tree = ET.parse(os.path.join(DATASET_DIR, xml_file))
	root = tree.getroot()

	file_name = None

	for elem in root:
		if elem.tag == 'filename':
			file_name = os.path.join(DATASET_DIR, elem.text)

		if elem.tag == 'object':
			obj_name = None
			coords = []
			for subelem in elem:
				if subelem.tag == 'name':
					obj_name = subelem.text
				if subelem.tag == 'bndbox':
					for subsubelem in subelem:
						coords.append(subsubelem.text)
			item = [file_name] + coords + [obj_name]
			if len(WHITELIST) == 0 or obj_name in WHITELIST:
				annotations.append(item)
				classes.add(obj_name)

ANNOTATIONS_FILE = mypath + "/annonations_file.csv"
CLASSES_FILE = mypath + "/classes_file.csv"

print("[INFO] Escrevendo annotations_file.csv...")
with open(ANNOTATIONS_FILE, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(annotations)

print("[INFO] Escrevendo classes_file.csv...")
with open(CLASSES_FILE, 'w') as f:
    for i, line in enumerate(classes):
        f.write('{},{}\n'.format(line, i))

print("[INFO] Done!")


# keras_retinanet/bin/train.py csv ../Documentos/@home_dataset/CALTECH101/annonations_file.csv  ../Documentos/@home_dataset/CALTECH101/classes_file.csv
