import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import json
from typing import List, Tuple
import PIL
from PIL import Image
from PIL import ImageDraw as PILImageDraw
from easydict import EasyDict as edict


def data_parsing(json_path: str, id:int):
    """_summary_

    Args:
        json_path (str): json path must be string
    annotation에서 bbox, file_name, supercategory 값을 추출
    bbox는 list -> List[tuple]
    example [(x,y,h,w)]

    Return: List= [(file_name, bbox, supercategory) ]


    """
    with open(json_path) as f:
        _anno_dict = json.load(f)
        anno_dict = edict(_anno_dict)

    file_name = anno_dict.images[n].file_name


def make_imgpath(image_root: str, image_id):
    """_summary_

    Args:
        image_root (_type_): image file root path must be string
        image_id (_type_): annotation의 image_id
    """
    pass


def draw_boundingbox(
    img_path: str, bbox: List[tuple], supercategory: List
) -> PIL.Image.Image:
    img = Image.open(img_path)
    font1 = {"color": "blue", "weight": "bold", "size": 12}
    plt.imshow(img)
    ax = plt.gca()

    for n in range(0, len(bbox)):
        x = bbox[n][0]
        y = bbox[n][1]
        width = bbox[n][2]
        height = bbox[n][3]
        rect = patches.Rectangle((x, y), width, height, edgecolor="blue", fill=False)
        ax.add_patch(rect)
        ax.text(x, y + 10, supercategory[n], fontdict=font1)
    plt.show()

    """_summary_

    Args:
        img_path (str): img_path must be string
        bbox (List[tuple]): [(x,y,h,w), ...] 1개 이상의 튜플
        supercategory: List ["Dog", "Cat", ...] 1개 이상의 string, len(bbox) = len(supercategory) 일치하지 않을 시 null 값.

    bbox가 갖고 있는 튜플의 개수 만큼 반복문을 통해 사각형을 이미지에 생성
    튜플안 값들은 0번째부터 3번째까지 각각 x,y,width, height 값을 나타냄. 
    ax.text()를 통해 각 사각형의 카테고리 부여 
    Returns:
        PIL.Image.Image: _description_
        임의로 plt.show()로 리턴, -> 이미지 저장 후추 구현?
    """
    pass
