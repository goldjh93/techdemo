import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json
from typing import List
import PIL
from PIL import Image
from PIL import ImageDraw as PILImageDraw
from easydict import EasyDict as edict


def data_parsing(json_path: str, image_id: int):
    """Parse JSON data and extract bounding box and category information for a specific image.

    Args:
        json_path (str): Path to the JSON file containing the data.
        image_id (int): ID of the image to retrieve information for.

    Returns:
        dict: A dictionary containing the bounding box and category information for the specified image.
              The dictionary structure is {image_id: [[bbox_list], [name_list]]}.
    """

    # json_path를 통해 json파일 로드하여 json_dict에 저장
    with open(json_path) as f:
        _json_dict = json.load(f)
        json_dict = edict(_json_dict)

    # 각 필드를 조인하기 위해 categories, annotations, images로 분리
    _cate = pd.DataFrame(json_dict.categories)
    _anno = pd.DataFrame(json_dict.annotations)
    _img = pd.DataFrame(json_dict.images)
    # annotations와 images image_id로 left join 후 새 필드 생성
    join_df = pd.merge(
        left=_img, right=_anno, how="left", left_on=["id"], right_on=["image_id"]
    )
    data_tb1 = join_df[["image_id", "bbox", "category_id"]]
    # data_tb1과 categories category_id로 left join  후 새 필드 생성
    data_tb2 = pd.merge(
        left=data_tb1, right=_cate, how="left", left_on=["category_id"], right_on=["id"]
    )
    final_tb = data_tb2[["image_id", "bbox", "name"]]
    final_tb = final_tb.dropna()
    final_tb = final_tb.astype({"image_id": "int32", "name": "category"})

    # image_id를 통해 테이블 검색 후 bbox, name 리스트 추출
    temp_dic = {}
    temp_dic[image_id] = []
    for key in temp_dic:
        fd = final_tb[final_tb["image_id"] == key]
        bbox_data = fd.bbox.to_list()
        name_data = fd.name.to_list()
        temp_dic[key].append(bbox_data)
        temp_dic[key].append(name_data)

    return temp_dic


def make_bboxlist(data_dic: dict) -> List[List]:
    # bboxlist변환
    bboxlist = list(data_dic.values())[0][0]

    return bboxlist


def make_namelist(data_dic: dict) -> List[str]:
    # namelist변환
    namelist = list(data_dic.values())[0][1]

    return namelist


def set_color(json_path: str) -> dict:
    """Assign colors to category names.

    Assigns a random color to each unique category name in the JSON data.

    Args:
        json_path (str): Path to the JSON file containing the data.

    Returns:
        dict: A dictionary mapping category names to their assigned colors.
    """
    # 카테고리 name 색 할당
    with open(json_path) as f:
        _json_dict = json.load(f)
        json_dict = edict(_json_dict)
    _cate = pd.DataFrame(json_dict.categories)

    temp_color = {}
    name_array = _cate["name"].unique()
    for name in name_array:
        color = "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
        temp_color[name] = color

    return temp_color


def make_imgpath(image_root: str, image_id: int):
    # draw_bounding 함수에 넣을 이미지 경로 생성

    # image_id의 길이가 6이하일 때 '0'의 걔수는 7개
    if len(str(image_id)) < 6:
        image_path = image_root + "/" + "0000000" + str(image_id) + ".jpg"
    # image_id의 길이가 6보다 클 때 '0'의 걔수는 6개
    else:
        image_path = image_root + "/" + "000000" + str(image_id) + ".jpg"

    return image_path


def draw_boundingbox(
    img_path: str,
    bbox: List[List],
    supercategory: List,
    image_id: int,
    sv_path: str,
    color_dic: dict,
    fontsize: int = 10,
    boxwidth: int = 3,
) -> PIL.Image.Image:
    """Draw bounding boxes on an image and label each box.

    Args:
        img_path (str): Path to the image file.
        bbox (List[List]): List of bounding boxes. Each bounding box should be a list [x, y, width, height].
        supercategory (List): List of supercategories corresponding to each bounding box.
        image_id (int): ID of the image.
        sv_path (str): Path to save the resulting image file.
        color_dic (dict): Dictionary mapping supercategories to assigned colors.
        fontsize (int, optional): Font size for the labels. Defaults to 10.
        boxwidth (int, optional): Width of the bounding box lines. Defaults to 3.

    Returns:
        PIL.Image.Image: The resulting image with bounding boxes and labels.
    """
    # 지정된 이미지파일경로에 있는 이미지에 바운딩 박스를 그리고 박스에 라벨을 표시

    # 이미지 로드
    img = Image.open(img_path)
    plt.imshow(img)
    ax = plt.gca()
    font1 = {"color": "black", "weight": "normal", "fontsize": fontsize}
    # 바운딩 박스 그리기 박스의 색과 라벨에 컬러 매칭
    for n in range(0, len(bbox)):
        x = bbox[n][0]
        y = bbox[n][1]
        width = bbox[n][2]
        height = bbox[n][3]
        color = color_dic[supercategory[n]]
        box1 = {"facecolor": color, "edgecolor": color}
        rect = patches.Rectangle(
            (x, y), width, height, edgecolor=color, linewidth=boxwidth, fill=False
        )
        ax.add_patch(rect)
        ax.text(
            x,
            y + 10,
            supercategory[n],
            fontdict=font1,
            bbox=box1,
            verticalalignment="top",
            horizontalalignment="left",
        )
    # plt.show()
    plt.savefig(sv_path + "/" + str(image_id) + ".png")
