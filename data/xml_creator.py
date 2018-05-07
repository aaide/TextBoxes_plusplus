"""
Based on @MhLiao's post here: https://github.com/MhLiao/TextBoxes_plusplus/issues/17
"""

import xml.dom.minidom as dom
import os


class XMLFacade:
    def __init__(self, img_name, sub_dir, dim, objects):
        self.img_name = img_name
        self.sub_dir = sub_dir
        self.dim = dim
        self.objects = objects
        self.doc = None

    def create(self):
        doc = dom.Document()
        root_node = doc.createElement('annotation')
        doc.appendChild(root_node)
        folder_node = doc.createElement('folder')
        folder_node_value = doc.createTextNode(self.sub_dir)
        folder_node.appendChild(folder_node_value)
        filename_node = doc.createElement('filename')
        filename_value = doc.createTextNode(self.img_name)
        filename_node.appendChild(filename_value)
        size_node = doc.createElement('size')
        root_node.appendChild(size_node)
        width_node = doc.createElement('width')
        width_value = doc.createTextNode(self.dim[0])
        width_node.appendChild(width_value)
        height_node = doc.createElement('height')
        height_value = doc.createTextNode(self.dim[1])
        height_node.appendChild(height_value)
        depth_node = doc.createElement('depth')
        depth_value = doc.createTextNode('3')
        depth_node.appendChild(depth_value)
        size_node.appendChild(width_node)
        size_node.appendChild(height_node)
        size_node.appendChild(depth_node)

        for difficult, label, (x1, y1, x2, y2, x3, y3, x4, y4) in self.objects:
            x = list(map(int, (x1, x2, x3, x4)))
            xmin = str(min(x))
            xmax = str(max(x))
            y = list(map(int, (y1, y2, y3, y4)))
            ymin = str(min(y))
            ymax = str(max(y))
            object_node = doc.createElement('object')
            root_node.appendChild(object_node)
            name_node = doc.createElement('name')
            name_value = doc.createTextNode('text')
            name_node.appendChild(name_value)
            label_node = doc.createElement('content')
            label_value = doc.createTextNode(label)
            label_node.appendChild(label_value)
            difficult_node = doc.createElement('difficult')
            difficult_value = doc.createTextNode(difficult)
            difficult_node.appendChild(difficult_value)
            bndbox_node = doc.createElement('bndbox')
            object_node.appendChild(bndbox_node)
            x1_node = doc.createElement('x1')
            x1_value = doc.createTextNode(x1)
            x1_node.appendChild(x1_value)
            y1_node = doc.createElement('y1')
            y1_value = doc.createTextNode(y1)
            y1_node.appendChild(y1_value)
            x2_node = doc.createElement('x2')
            x2_value = doc.createTextNode(x2)
            x2_node.appendChild(x2_value)
            y2_node = doc.createElement('y2')
            y2_value = doc.createTextNode(y2)
            y2_node.appendChild(y2_value)
            x3_node = doc.createElement('x3')
            x3_value = doc.createTextNode(x3)
            x3_node.appendChild(x3_value)
            y3_node = doc.createElement('y3')
            y3_value = doc.createTextNode(y3)
            y3_node.appendChild(y3_value)
            x4_node = doc.createElement('x4')
            x4_value = doc.createTextNode(x4)
            x4_node.appendChild(x4_value)
            y4_node = doc.createElement('y4')
            y4_value = doc.createTextNode(y4)
            y4_node.appendChild(y4_value)
            xmin_node = doc.createElement('xmin')
            xmin_value = doc.createTextNode(xmin)
            xmin_node.appendChild(xmin_value)
            ymin_node = doc.createElement('ymin')
            ymin_value = doc.createTextNode(ymin)
            ymin_node.appendChild(ymin_value)
            xmax_node = doc.createElement('xmax')
            xmax_value = doc.createTextNode(xmax)
            xmax_node.appendChild(xmax_value)
            ymax_node = doc.createElement('ymax')
            ymax_value = doc.createTextNode(ymax)
            ymax_node.appendChild(ymax_value)
            bndbox_node.appendChild(x1_node)
            bndbox_node.appendChild(y1_node)
            bndbox_node.appendChild(x2_node)
            bndbox_node.appendChild(y2_node)
            bndbox_node.appendChild(x3_node)
            bndbox_node.appendChild(y3_node)
            bndbox_node.appendChild(x4_node)
            bndbox_node.appendChild(y4_node)
            bndbox_node.appendChild(xmin_node)
            bndbox_node.appendChild(ymin_node)
            bndbox_node.appendChild(xmax_node)
            bndbox_node.appendChild(ymax_node)
            object_node.appendChild(difficult_node)
            object_node.appendChild(label_node)
            object_node.appendChild(name_node)
            object_node.appendChild(bndbox_node)
            root_node.appendChild(object_node)
        root_node.appendChild(folder_node)
        root_node.appendChild(filename_node)
        root_node.appendChild(size_node)
        self.doc = doc

    def write(self, xml_file_path=None):
        if not xml_file_path:
            xml_file_path = self.img_name.split('.')[0] + '.xml'
        f = open(xml_file_path, 'wb')
        f.write(self.doc.toprettyxml(indent="\t", newl="\n", encoding="utf-8"))
        f.close()


def txt_to_xml(base_file):
    with open(base_file, 'r') as bf:
        line = bf.readline().strip()
        while line:
            img_name = line
            sub_dir = bf.readline().strip()
            dim = bf.readline().split()
            line = bf.readline().strip()
            objects = []
            while line in ['0', '1']:
                difficult = line
                label = bf.readline().strip()
                bounding_limits = bf.readline().split()
                objects.append((difficult, label, bounding_limits))
                line = bf.readline().strip()
            x = XMLFacade(img_name, sub_dir, dim, objects)
            x.create()
            x.write()


if __name__ == '__main__':
    base_file = os.path.join("text", "example.txt")
    txt_to_xml(base_file)
