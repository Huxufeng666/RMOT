# """
# Created on Tue Jun 12 10:24:36 2018
# 将voc格式转json格式用于caffe2的detectron的训练
# 在detectron中voc_2007_train.json和voc_2007_val.json中categories的顺序必须保持一致
# 因此最好事先确定category的顺序,书写在category_set中
# @author: yantianwang
# """
 
# import xml.etree.ElementTree as ET
# import os
# import json
# import collections
 
# coco = dict()
# coco['images'] = []
# coco['type'] = 'instances'
# coco['annotations'] = []
# coco['categories'] = []
 
# #category_set = dict()
# image_set = set()
# image_id = 2019000001  #train:2018xxx; val:2019xxx; test:2020xxx
# category_item_id = 1
# annotation_id = 1
# category_set = ['small-vehicle', 'large-vehicle', 'plane','harbor', 'ship', 
#              'tennis-court', 'soccer-ball-field', 'ground-track-field',
#              'baseball-diamond', 'swimming-pool', 'roundabout', 'basketball-court', 
#              'storage-tank', 'bridge', 'helicopter']
# '''
# def addCatItem(name):
#     global category_item_id
#     category_item = dict()
#     category_item['supercategory'] = 'none'
#     category_item_id += 1
#     category_item['id'] = category_item_id
#     category_item['name'] = name
#     coco['categories'].append(category_item)
#     category_set[name] = category_item_id
#     return category_item_id
# '''
 
# def addCatItem(name):
#     '''
#     增加json格式中的categories部分
#     '''
#     global category_item_id
#     category_item = collections.OrderedDict()
#     category_item['supercategory'] = 'none'
#     category_item['id'] = category_item_id
#     category_item['name'] = name
#     coco['categories'].append(category_item)
#     category_item_id += 1
 
# def addImgItem(file_name, size):
#     global image_id
#     if file_name is None:
#         raise Exception('Could not find filename tag in xml file.')
#     if size['width'] is None:
#         raise Exception('Could not find width tag in xml file.')
#     if size['height'] is None:
#         raise Exception('Could not find height tag in xml file.')
#     #image_item = dict()    #按照一定的顺序，这里采用collections.OrderedDict()
#     image_item = collections.OrderedDict()
#     jpg_name = os.path.splitext(file_name)[0]+'.png'
#     image_item['file_name'] = jpg_name  
#     image_item['width'] = size['width']   
#     image_item['height'] = size['height']
#     image_item['id'] = image_id
#     coco['images'].append(image_item)
#     image_set.add(jpg_name)    
#     image_id = image_id+1
#     return image_id
 
 
# def addAnnoItem(object_name, image_id, category_id, bbox):
#     global annotation_id
#     #annotation_item = dict()
#     annotation_item = collections.OrderedDict()
#     annotation_item['segmentation'] = []
#     seg = []
#     # bbox[] is x,y,w,h
#     # left_top
#     seg.append(bbox[0])
#     seg.append(bbox[1])
#     # left_bottom
#     seg.append(bbox[0])
#     seg.append(bbox[1] + bbox[3])
#     # right_bottom
#     seg.append(bbox[0] + bbox[2])
#     seg.append(bbox[1] + bbox[3])
#     # right_top
#     seg.append(bbox[0] + bbox[2])
#     seg.append(bbox[1])
#     annotation_item['segmentation'].append(seg)
#     annotation_item['area'] = bbox[2] * bbox[3]
#     annotation_item['iscrowd'] = 0
#     annotation_item['image_id'] = image_id
#     annotation_item['bbox'] = bbox
#     annotation_item['category_id'] = category_id
#     annotation_item['id'] = annotation_id
#     annotation_item['ignore'] = 0 
#     annotation_id += 1 
#     coco['annotations'].append(annotation_item)
 
 
# def parseXmlFiles(xml_path):
#     xmllist = os.listdir(xml_path)
#     xmllist.sort()
#     for f in xmllist:
#         if not f.endswith('.xml'):
#             continue
 
#         bndbox = dict()
#         size = dict()
#         current_image_id = None
#         current_category_id = None
#         file_name = None
#         size['width'] = None
#         size['height'] = None
#         size['depth'] = None
 
#         xml_file = os.path.join(xml_path, f)
#         print(xml_file)
 
#         tree = ET.parse(xml_file)
#         root = tree.getroot() #抓根结点元素
 
#         if root.tag != 'annotation': #根节点标签
#             raise Exception('pascal voc xml root element should be annotation, rather than {}'.format(root.tag))
 
#         # elem is <folder>, <filename>, <size>, <object>
#         for elem in root:
#             current_parent = elem.tag
#             current_sub = None
#             object_name = None
  

#             #elem.tag, elem.attrib，elem.text
#             if elem.tag == 'folder':
#                 continue
 
#             if elem.tag == 'filename':
#                 file_name = elem.text
#                 if file_name in category_set:
#                     raise Exception('file_name duplicated')
 
#             # add img item only after parse <size> tag
#             elif current_image_id is None and file_name is not None and size['width'] is not None:
#                 if file_name not in image_set:
#                     current_image_id = addImgItem(file_name, size)#图片信息
#                     print('add image with {} and {}'.format(file_name, size))
#                 else:
#                     raise Exception('duplicated image: {}'.format(file_name))
#                     # subelem is <width>, <height>, <depth>, <name>, <bndbox>
#             for subelem in elem:
#                 bndbox['xmin'] = None
#                 bndbox['xmax'] = None
#                 bndbox['ymin'] = None
#                 bndbox['ymax'] = None
 
#                 current_sub = subelem.tag
#                 if current_parent == 'object' and subelem.tag == 'name':
#                     object_name = subelem.text
#                     #if object_name not in category_set:
#                     #    current_category_id = addCatItem(object_name)
#                     #else:
#                     #current_category_id = category_set[object_name]
#                     current_category_id = category_set.index(object_name)+1 #index默认从0开始,但是json文件是从1开始，所以+1
#                 elif current_parent == 'size':
#                     if size[subelem.tag] is not None:
#                         raise Exception('xml structure broken at size tag.')
#                     size[subelem.tag] = int(subelem.text)
 
#                 # option is <xmin>, <ymin>, <xmax>, <ymax>, when subelem is <bndbox>
#                 for option in subelem:
#                     if current_sub == 'bndbox':
#                         if bndbox[option.tag] is not None:
#                             raise Exception('xml structure corrupted at bndbox tag.')
#                         bndbox[option.tag] = int(option.text)
 
#                 # only after parse the <object> tag
#                 if bndbox['xmin'] is not None:
#                     if object_name is None:
#                         raise Exception('xml structure broken at bndbox tag')
#                     if current_image_id is None:
#                         raise Exception('xml structure broken at bndbox tag')
#                     if current_category_id is None:
#                         raise Exception('xml structure broken at bndbox tag')
#                     bbox = []
#                     # x
#                     bbox.append(bndbox['xmin'])
#                     # y
#                     bbox.append(bndbox['ymin'])
#                     # w
#                     bbox.append(bndbox['xmax'] - bndbox['xmin'])
#                     # h
#                     bbox.append(bndbox['ymax'] - bndbox['ymin'])
#                     print(
#                     'add annotation with {},{},{},{}'.format(object_name, current_image_id-1, current_category_id, bbox))
#                     addAnnoItem(object_name, current_image_id-1, current_category_id, bbox)
#     #categories部分
#     for categoryname in category_set:
#         addCatItem(categoryname) 
 
 
# if __name__ == '__main__':
#     xml_path = '/workspace/dataset/MaskPascalVOC/Annotations'
#     json_file = '/workspace/dataset/MaskPascalVOC/Annotations/voc_val.json'
#     parseXmlFiles(xml_path)
# json.dump(coco, open(json_file, 'w'))


#  import os
# import imageio

# if __name__ == '__main__':
#     ims_folder = '/workspace/demos/demo_vis'
#     gif_path = './pedestrian_2.gif'
#     ims_path_list = os.listdir(ims_folder)
#     ims_path_list.sort()
#     ims_list = []

#     for i, im_path in enumerate(ims_path_list):
#         im = imageio.imread(os.path.join(ims_folder, im_path))
#         ims_list.append(im)
#     imageio.mimsave(gif_path, ims_list, duration=0.1, loop=1)


# ffmpeg -f image2 -framerate 25 -i "/workspace/demos/demo_vis/%6d.jpg" -s 960*540 -y ./test1.mp4

import time
import cv2
 
def nothing(emp):
    pass
#设置窗口名称
cv2.namedWindow('frame')
cap = cv2.VideoCapture("/RMOT/exps/e2e_motr_r50_joint/results/demo/demo.avi")  # 读取文件
start_time = time.time()
#用于记录帧数
counter = 0
# 获取视频宽度
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# 获取视频高度
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#视频平均帧率
fps = cap.get(cv2.CAP_PROP_FPS)
# 获取视频帧数
frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
loop_flag = 0
pos = 0
# 新建一个滑动条
cv2.createTrackbar('time', 'frame', 0, frames, nothing)
while (True):
    if loop_flag == pos:
        loop_flag = loop_flag + 1
        cv2.setTrackbarPos('time', 'frame', loop_flag)
    else:
        pos = cv2.getTrackbarPos('time', 'frame')
        loop_flag = pos
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
    ret, frame = cap.read()
    # 键盘输入空格暂停，输入q退出
    key = cv2.waitKey(1) & 0xff
    if key == ord(" "):
        cv2.waitKey(0)
    if key == ord("q"):
        break
    counter += 1  # 计算帧数
    if (time.time() - start_time) != 0:  # 实时显示帧数
        cv2.putText(frame, "FPS {0}".format(float('%.1f' % (counter / (time.time() - start_time)))), (500, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),
                    3)
        src = cv2.resize(frame, (frame_width // 2, frame_height // 2), interpolation=cv2.INTER_CUBIC)  # 窗口大小
        cv2.imshow('frame', src)
        print("FPS: ", counter / (time.time() - start_time))
        counter = 0
        start_time = time.time()
    time.sleep(1 / fps)  # 按原帧率播放
cap.release()
cv2.destroyAllWindows()


