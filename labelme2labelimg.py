# -*- coding: utf-8 -*-
import os
import json
from PIL import Image
from xml.dom.minidom import Document
from apply_exif_orientation import apply_exif_orientation


source_path = r'C:\Users\smile\Desktop\毕业设计\需要标记的图片'            # Labelme的工作文件夹
target_path = r'C:\Users\smile\Desktop\毕业设计\需要标记的图片_LabelImg'   # 生成的新文件夹，不存在时会创建
source_img_suffixs = ['JPG', 'PNG']  # 在windows中，大小写不敏感，linux下需要额外添加小写扩展        # 支持的原始图片，可以多个
target_img_suffix = 'png'       # 生成的图片文件后缀，仅限一种，推荐png


# 以下是在labelImg的xml预定义的一些数据
m_database = 'Unknown'
m_segmented = 0
m_pose='Unspecified'
m_truncated = 1
m_difficult = 0
m_segmented = 0


def transformer(old_json_path, old_img_path, new_xml_path, new_img_path):
    ## 图片处理
    img = Image.open(old_img_path)
    img = apply_exif_orientation(img)
    m_depth = len(img.getbands()) 
    m_width, m_height = img.width, img.height
    img.save(new_img_path)

    ## 文件处理
    json_data = open(old_json_path, 'r').read()
    data = json.loads(json_data)
    new_img_dir, m_filename = os.path.split(new_img_path)
    m_folder = os.path.split(new_img_dir)[-1]
    m_path = new_img_path
    



    doc = Document()  #创建DOM文档对象
    DOCUMENT = doc.createElement('annotation') #创建根元素
    floder = doc.createElement('floder')         
    floder_text = doc.createTextNode(m_folder)
    floder.appendChild(floder_text)               
    DOCUMENT.appendChild(floder)                   
    doc.appendChild(DOCUMENT)
    #处理filename
    filename = doc.createElement('filename')           
    filename_text = doc.createTextNode(m_filename) 
    filename.appendChild(filename_text)               
    DOCUMENT.appendChild(filename)                   
    doc.appendChild(DOCUMENT)
    # 处理path
    path = doc.createElement('path')           
    path_text = doc.createTextNode(m_path) 
    path.appendChild(path_text)               
    DOCUMENT.appendChild(path)                   
    doc.appendChild(DOCUMENT)
    # 处理source
    source = doc.createElement('source') 
    database = doc.createElement('database')
    database_text = doc.createTextNode(m_database)
    database.appendChild(database_text)
    source.appendChild(database)                  
    DOCUMENT.appendChild(source)                   
    doc.appendChild(DOCUMENT)


    size = doc.createElement('size') 
    width = doc.createElement('width')
    width_text = doc.createTextNode(str(m_width))
    width.appendChild(width_text)
    size.appendChild(width) 
    height = doc.createElement('height')
    height_text = doc.createTextNode(str(m_height)) 
    height.appendChild(height_text)
    size.appendChild(height)   
    depth = doc.createElement('depth')
    depth_text = doc.createTextNode(str(m_depth)) 
    depth.appendChild(depth_text)
    size.appendChild(depth) 
    DOCUMENT.appendChild(size) 

    
    segmented = doc.createElement('segmented')           
    segmented_text = doc.createTextNode(str(m_segmented)) 
    segmented.appendChild(segmented_text)               
    DOCUMENT.appendChild(segmented)                   
    
    doc.appendChild(DOCUMENT)
    for i in range(len(data['shapes'])):  # 遍历每一个shape
        m_name = data['shapes'][i]['label']
        m_xmin, m_ymin = m_width, m_height
        m_xmax, m_ymax = 0, 0
        for j in range(0, len(data['shapes'][i]['points'])):
            m_xmin = min(m_xmin, int(data['shapes'][i]['points'][j][0]))
            m_xmax = max(m_xmax, int(data['shapes'][i]['points'][j][0]))
            m_ymin = min(m_ymin, int(data['shapes'][i]['points'][j][1]))
            m_ymax = max(m_ymax, int(data['shapes'][i]['points'][j][1]))
            
        object = doc.createElement('object') 
        name = doc.createElement('name')
        name_text = doc.createTextNode(m_name)
        name.appendChild(name_text)
        object.appendChild(name) 
        pose = doc.createElement('pose')
        pose_text = doc.createTextNode(m_pose) 
        pose.appendChild(pose_text)
        object.appendChild(pose)   
        truncated = doc.createElement('truncated')
        truncated_text = doc.createTextNode(str(m_truncated)) 
        truncated.appendChild(truncated_text)
        object.appendChild(truncated) 
        difficult = doc.createElement('difficult')
        difficult_text = doc.createTextNode(str(m_difficult)) 
        difficult.appendChild(difficult_text)
        object.appendChild(difficult) 

        bndbox  = doc.createElement('bndbox') 
        xmin = doc.createElement('xmin')
        xmin_text = doc.createTextNode(str(m_xmin))
        xmin.appendChild(xmin_text)
        bndbox.appendChild(xmin) 

        ymin = doc.createElement('ymin')
        ymin_text = doc.createTextNode(str(m_ymin)) 
        ymin.appendChild(ymin_text)
        bndbox.appendChild(ymin)   
    
        xmax = doc.createElement('xmax')
        xmax_text = doc.createTextNode(str(m_xmax))
        xmax.appendChild(xmax_text)
        bndbox.appendChild(xmax) 

        ymax = doc.createElement('ymax')
        ymax_text = doc.createTextNode(str(m_ymax)) 
        ymax.appendChild(ymax_text)
        bndbox.appendChild(ymax) 
        object.appendChild(bndbox)

        DOCUMENT.appendChild(object) 
        
    xml_file = open(new_xml_path, 'w',  encoding='utf-8')
    #writexml()第一个参数是目标文件对象，第二个参数是根节点的缩进格式，第三个参数是其他子节点的缩进格式，
    # 第四个参数制定了换行格式，第五个参数制定了xml内容的编码。
    doc.writexml(xml_file, indent = '', newl = '\n', addindent = '\t', encoding='utf-8')
    xml_file.close()



if __name__ == "__main__":
    # 遍历json文件并确保存在相应的图片文件，保持文件结构，并复制
    for root, dirs, files in os.walk(source_path):
        new_root = root.replace(source_path, target_path, 1)
        if not os.path.exists(new_root):
            os.makedirs(new_root)
        
        for dir in dirs:
            dir = os.path.join(new_root, dir)
            if not os.path.exists(dir):
                os.mkdir(dir)

        for file in files:
            shortname, extension = os.path.splitext(file)
            if extension != '.json':
                continue
            else:
                exist_same_name_img = False
                for img_suffix in source_img_suffixs:
                    if os.path.exists(os.path.join(root, shortname+'.'+img_suffix)):
                        exist_same_name_img = True
                        old_img_path = os.path.join(root, shortname+'.'+img_suffix)
                        new_img_path = os.path.join(new_root, shortname+'.'+target_img_suffix)
                if exist_same_name_img is False:
                    continue

            # 原json文件的路径
            old_json_path = os.path.join(root, file)
            # 原始img文件的路径 old_img_path
            # 新xml文件的路径
            new_xml_path = os.path.join(new_root, shortname+'.xml')
            # 新img文件的路径 new_img_path
            print(new_img_path)
            try:
                transformer(old_json_path, old_img_path, new_xml_path, new_img_path)
            except IOError as e:
                print(e)
