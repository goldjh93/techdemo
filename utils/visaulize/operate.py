import visaulize_od as vs


image_id = 61471
jsonurl = "/home/goldjh93/dataset/coco/annotations-4/instances_val2017.json"
imgurl = "/home/goldjh93/dataset/coco/val2017"
svurl = "/home/goldjh93/img/coco"
data_dic = vs.data_parsing(jsonurl, image_id)
# print(data_dic)

bboxlist = vs.make_bboxlist(data_dic)
namelist = vs.make_namelist(data_dic)
imgpath = vs.make_imgpath(imgurl, image_id)
color_dict = vs.set_color(jsonurl)

# print(bboxlist)
# print(namelist)
# print(imgpath)
# print(color_dict)

vs.draw_boundingbox(imgpath, bboxlist, namelist, image_id, svurl, color_dict, 4, 2)
# '/home/goldjh93/img/coco'
# "/home/goldjh93/img/lvis"
# '/home/goldjh93/dataset/coco/annotations-4/instances_val2017.json'
# "/home/goldjh93/dataset/LVIS/lvis_v1_val.json"
