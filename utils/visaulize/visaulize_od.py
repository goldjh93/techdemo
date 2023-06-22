import numpy as np
import matplotlib.pyplot as plt
import json
from typing import List
import PIL
from PIL import Image as PILImage
from PIL import ImageDraw as PILImageDraw

def data_parsing(json_path: str):
    """_summary_

    Args:
        json_path (str): _description_
    """
    js_file = open(json_path)
    js_data = json.load(js_file)

    # for key
    # pass



def draw_boundingbox(img_path: str, bbox: List[tuple])->PIL.Image.Image :
    """_summary_

    Args:
        img_path (str): _description_
        bbox (List[tuple]): _description_

    Returns:
        PIL.Image.Image: _description_
    """
    pass 