import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json
from typing import List, Tuple
import PIL
from PIL import Image
from PIL import ImageDraw as PILImageDraw
from easydict import EasyDict as edict


def data_parsing(json_path: str, image_id: int):
    """Parse data from a JSON file and retrieve bounding box and category information for a specific image ID.

    Args:
        json_path (str): The path to the JSON file.
        image_id (int): The ID of the image to retrieve data for.

    Returns:
        dict: A dictionary containing bounding box and category information for the specified image ID.
            The dictionary has the following structure:
            {
                image_id (int): [
                    bbox_data (list of lists): A list of bounding box coordinates for the image,
                        where each inner list represents a bounding box as [x, y, width, height].
                    name_data (list of str): A list of category names corresponding to each bounding box.
                ]
            }

    Raises:
        FileNotFoundError: If the JSON file specified by `json_path` does not exist.

    Example:
        json_path = 'data.json'
        image_id = 123
        result = data_parsing(json_path, image_id)
        print(result)
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


# bboxlist변환 함수
def make_bboxlist(data_dic: dict) -> List[List]:
    bboxlist = list(data_dic.values())[0][0]

    return bboxlist


# namelist변환 함수
def make_namelist(data_dic: dict) -> List[str]:
    namelist = list(data_dic.values())[0][1]

    return namelist


# draw_bounding 함수에 넣을 이미지 경로 생성 함수
def make_imgpath(image_root: str, image_id):
    """Creates a file path for an image based on the image root and image ID.

    Args:
        image_root (str): The root directory where the image files are located.
        image_id: The ID of the image.

    Returns:
        str: The file path for the image.

    Example:
        image_root = "path/to/images"
        image_id = 12345
        result = make_imgpath(image_root, image_id)
        print(result)
        # Output: "path/to/images/0000012345.jpg"
    """
    # image_id의 길이가 6이하일 때 '0'의 걔수는 7개
    if len(str(image_id)) < 6:
        image_path = image_root + "/" + "0000000" + str(image_id) + ".jpg"
    # image_id의 길이가 6보다 클 때 '0'의 걔수는 6개
    else:
        image_path = image_root + "/" + "0000000" + str(image_id) + ".jpg"

    return image_path


# 지정된 이미지파일경로에 있는 이미지에 바운딩 박스를 그리고 박스에 라벨을 표시하는 함수
def draw_boundingbox(
    img_path: str, bbox: List[List], supercategory: List
) -> PIL.Image.Image:
    """Draws bounding boxes on an image and labels them with their respective supercategories.

    Args:
        img_path (str): The path to the image file.
        bbox (List[List[int]]): A list of lists representing the bounding boxes. Each inner list contains four integers:
                                the x and y coordinates of the top-left corner, followed by the width and height of the bounding box.
        supercategory (List[str]): A list of strings representing the supercategory labels for each bounding box.

    Returns:
        PIL.Image.Image: The image with bounding boxes and labels.

    Example:
        img_path = "path/to/image.jpg"
        bbox = [[10, 20, 50, 70], [60, 80, 30, 40]]
        supercategory = ["Category 1", "Category 2"]
        result = draw_boundingbox(img_path, bbox, supercategory)
        result.show()
    """
    # 이미지 로드
    img = Image.open(img_path)
    plt.imshow(img)
    ax = plt.gca()

    # 바운딩 박스 그리기 박스의 색과 라벨에 랜덤 컬러 설정
    for n in range(0, len(bbox)):
        x = bbox[n][0]
        y = bbox[n][1]
        width = bbox[n][2]
        height = bbox[n][3]
        colors = "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
        font1 = {"color": colors, "weight": "bold", "size": 11}
        rect = patches.Rectangle((x, y), width, height, edgecolor=colors, fill=False)
        ax.add_patch(rect)
        ax.text(x, y + 10, supercategory[n], fontdict=font1)
    plt.show()
