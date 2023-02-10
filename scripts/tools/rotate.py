import cv2
import math
import numpy as np
import os
import pdb
import xml.etree.ElementTree as ET


class ImgAugemention():
    def __init__(self):
        self.angle = 90

    # rotate_img
    def rotate_image(self, src, angle, scale=1.):
        w = src.shape[1]
        h = src.shape[0]
        # convet angle into rad
        rangle = np.deg2rad(angle)  # angle in radians
        # calculate new image width and height
        nw = (abs(np.sin(rangle) * h) + abs(np.cos(rangle) * w)) * scale
        nh = (abs(np.cos(rangle) * h) + abs(np.sin(rangle) * w)) * scale
        # ask OpenCV for the rotation matrix
        rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), angle, scale)
        # calculate the move from the old center to the new center combined
        # with the rotation
        rot_move = np.dot(rot_mat, np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0]))
        # the move only affects the translation, so update the translation
        # part of the transform
        rot_mat[0, 2] += rot_move[0]
        rot_mat[1, 2] += rot_move[1]
        # map
        return cv2.warpAffine(
            src, rot_mat, (int(math.floor(nw)), int(math.floor(nh))),  # ceil
            flags=cv2.INTER_LANCZOS4)

    def rotate_xml(self, src, xmin, ymin, xmax, ymax, angle, scale=1.):
        w = src.shape[1]
        h = src.shape[0]
        rangle = np.deg2rad(angle)  # angle in radians
        # now calculate new image width and height
        # get width and heigh of changed image
        nw = (abs(np.sin(rangle) * h) + abs(np.cos(rangle) * w)) * scale
        nh = (abs(np.cos(rangle) * h) + abs(np.sin(rangle) * w)) * scale
        # ask OpenCV for the rotation matrix
        rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), angle, scale)
        # calculate the move from the old center to the new center combined
        # with the rotation
        rot_move = np.dot(rot_mat, np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0]))
        # the move only affects the translation, so update the translation
        # part of the transform
        rot_mat[0, 2] += rot_move[0]
        rot_mat[1, 2] += rot_move[1]
        # rot_mat: the final rot matrix
        # get the four center of edges in the initial martix，and convert the coord
        point1 = np.dot(rot_mat, np.array([(xmin + xmax) / 2, ymin, 1]))
        point2 = np.dot(rot_mat, np.array([xmax, (ymin + ymax) / 2, 1]))
        point3 = np.dot(rot_mat, np.array([(xmin + xmax) / 2, ymax, 1]))
        point4 = np.dot(rot_mat, np.array([xmin, (ymin + ymax) / 2, 1]))
        # concat np.array
        concat = np.vstack((point1, point2, point3, point4))
        # change type
        concat = concat.astype(np.int32)
        # print(concat)
        rx, ry, rw, rh = cv2.boundingRect(concat)
        return rx, ry, rw, rh

    def process_img(self, imgs_path, xmls_path, img_save_path, xml_save_path, angle_list):
        # assign the rot angles
        for angle in angle_list:
            for img_name in os.listdir(imgs_path):
                # split filename and suffix
                n, s = os.path.splitext(img_name)
                # for the sake of use yolo model, only process '.jpg'
                if s == ".jpg":
                    img_path = os.path.join(imgs_path, img_name)
                    print(img_path)
                    img = cv2.imread(img_path)
                    if not img:
                        img = np.fromfile(img_path, dtype=np.uint8)
                        img = cv2.imdecode(img, -1)
                    rotated_img = self.rotate_image(img, angle)
                    save_name = n + "_" + str(angle) + "d.jpg"
                    # 写入图像
                    # cv2.imwrite(os.path.join(img_save_path, save_name), rotated_img)
                    cv2.imencode('.jpg', rotated_img)[1].tofile(os.path.join(img_save_path, save_name))
                    rotated_img = cv2.imread(os.path.join(img_save_path, save_name))
                    if not rotated_img:
                        rotated_img = np.fromfile(os.path.join(img_save_path, save_name), dtype=np.uint8)
                        rotated_img = cv2.imdecode(rotated_img, -1)
                    size = rotated_img.shape
                    w = size[1]  # 宽度
                    h = size[0]  # 高度
                    # print("log: [%sd] %s is processed." % (angle, img))
                    xml_url = img_name.split('.')[0] + '.xml'
                    xml_path = os.path.join(xmls_path, xml_url)
                    # print(xml_path)
                    # print(xml_url)
                    tree = ET.parse(xml_path)
                    file_name = tree.find('filename').text  # it is origin name
                    path = tree.find('path').text  # it is origin path
                    size = tree.find('size')
                    # w = size.find("width").text
                    # h = size.find("height").text
                    print(xml_path)
                    size.find("width").text = str(w)
                    size.find("height").text = str(h)
                    # change name and path
                    # tree.find('filename').text = save_name  # change file name to rot degree name
                    tree.find(
                        'filename').text = save_name  # change file path to rot degree name
                    root = tree.getroot()
                    for box in root.iter('bndbox'):
                        xmin = float(box.find('xmin').text)
                        ymin = float(box.find('ymin').text)
                        xmax = float(box.find('xmax').text)
                        ymax = float(box.find('ymax').text)
                        x, y, w, h = self.rotate_xml(img, xmin, ymin, xmax, ymax, angle)
                        # change the coord
                        box.find('xmin').text = str(x)
                        box.find('ymin').text = str(y)
                        box.find('xmax').text = str(x + w)
                        box.find('ymax').text = str(y + h)
                        box.set('updated', 'yes')
                    # write into new xml
                    tree.write(os.path.join(xml_save_path, n + "_" + str(angle) + "d.xml"), "utf-8")
                print("[%s] %s is processed." % (angle, img_name))


def clear_path(imgs_path, xmls_path):
    from shutil import rmtree
    if os.path.exists(imgs_path):
        rmtree(imgs_path)
    if os.path.exists(xmls_path):
        rmtree(xmls_path)
    # rmtree("/home/thor/data/sfz-gh/tmp")
    os.makedirs(imgs_path)
    os.makedirs(xmls_path)


def copysrcfile(files_path, imgs_path, xmls_path):
    from shutil import copyfile
    files = os.listdir(files_path)
    images = []
    for f in files:
        print(f)
        if "xml" in f:
            copyfile(os.path.join(files_path, f), os.path.join(xmls_path, f))
            images.append(f)
        else:
            copyfile(os.path.join(files_path, f), os.path.join(imgs_path, f))


if __name__ == '__main__':
    import random

    img_aug = ImgAugemention()
    imgs_path = r'C:\Users\9000\Desktop\标注\resize_rx\sfz_rx\images'
    xmls_path = r'C:\Users\9000\Desktop\标注\resize_rx\sfz_rx\annotations'
    img_save_path = r'C:\Users\9000\Desktop\标注\resize_rx\rotate'
    xml_save_path = r'C:\Users\9000\Desktop\标注\resize_rx\xml_rot'
    files_path = r'C:\Users\9000\Desktop\标注\resize_rx\all'
    clear_path(imgs_path, xmls_path)
    copysrcfile(files_path, imgs_path, xmls_path)

    angle_list = [90, -90]
    img_aug.process_img(imgs_path, xmls_path, img_save_path, xml_save_path, angle_list)
    from shutil import copyfile

    files = os.listdir(img_save_path)
    for f in files:
        copyfile(f"{img_save_path}/{f}", f"{imgs_path}/{f}")
    files = os.listdir(xml_save_path)
    for f in files:
        copyfile(f"{xml_save_path}/{f}", f"{xmls_path}/{f}")
    files = os.listdir(xmls_path)
    images = []
    for f in files:
        print(f)
        if "xml" in f:
            images.append(f)

    val_len = int(len(images) * 0.2)
    print(val_len)

    val_list = random.sample(images, val_len)

    vals = []
    trains = []
    for f in images:
        n = f.split(".")[0]
        img = None
        for i in ["jpg", "jpeg"]:
            if os.path.exists(rf"C:\Users\9000\Desktop\标注\resize_rx\sfz_rx\images/{n}.{i}"):
                img = rf"./images/{n}.{i}"
                break
        if not img: continue
        if f in val_list:
            vals.append(f"{img} ./annotations/{f}")
        else:
            trains.append(f"{img} ./annotations/{f}")

    with open(r"C:\Users\9000\Desktop\标注\resize_rx\sfz_rx/train.txt", "w") as w:
        w.write("\n".join(trains))

    with open(r"C:\Users\9000\Desktop\标注\resize_rx\sfz_rx/valid.txt", "w") as w:
        w.write("\n".join(vals))
