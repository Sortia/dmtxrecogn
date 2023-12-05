import asyncio

import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode
import os
from pdf2image import convert_from_path


class DatamatrixRecognizer:
    def __init__(self):
        self.resized_height = 2400
        self.resized_width = None
        self.zone_scale_x = 2
        self.zone_scale_y = 2
        self.bordered = None

        self.timeout = 2
        self.count_x_segments = 3
        self.count_y_segments = 6

    @staticmethod
    def get_img_list(path):
        file_extension = os.path.splitext(path)[1]

        if file_extension == '.pdf':
            pages = convert_from_path(path)
            img_list = [np.array(page) for page in pages]
        else:
            img_list = [cv2.imread(path, cv2.COLOR_BGR2GRAY)]

        return [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in img_list]

    @staticmethod
    def img_preprocessing(img):
        img = cv2.convertScaleAbs(img, alpha=1.5, beta=30)

        _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        kernel = np.ones((50, 50), np.uint8)
        closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        img[closed == 0] = 255

        return img

    def resize_img(self, img):
        height, width = img.shape[:2]
        aspect_ratio = width / height
        self.resized_width = int(self.resized_height * aspect_ratio)

        return cv2.resize(img, (self.resized_width, self.resized_height))

    def crop_img(self, img, params):
        segment_height = self.resized_height / self.count_y_segments
        segment_width = self.resized_width / self.count_x_segments

        search_area_height = int(segment_height * self.zone_scale_y)
        search_area_width = int(segment_width * self.zone_scale_x)

        y = max(0, int(((params["segment"]["y"] - 1) * segment_height) - (
                    (search_area_height - segment_height) / self.zone_scale_y)))
        x = max(0,
                int(((params["segment"]["x"] - 1) * segment_width) - ((search_area_width - segment_width) / self.zone_scale_x)))

        crop_y = y + search_area_height
        crop_x = x + search_area_width

        return img[y:crop_y, x:crop_x]

    def get_dmtx_text(self, img):
        data = decode(img, timeout=self.timeout * 1000, max_count=1, corrections=10)

        if data:
            return [data[0].data.decode('utf-8')]
        else:
            return []

    @staticmethod
    def add_borders(img):
        return cv2.copyMakeBorder(img, 150, 150, 150, 150, cv2.BORDER_CONSTANT, value=(255, 255, 255))

    def prepare_img(self, img, params):
        img = self.resize_img(img)
        img = self.crop_img(img, params)
        img = self.img_preprocessing(img)
        img = self.add_borders(img)
        # cv2.imwrite('output_image.png', img)  # Сохранить в формате PNG
        return img

    async def process_img(self, img, params):
        prepared_img = self.prepare_img(img, params)
        return self.get_dmtx_text(prepared_img)

    async def magick(self, path, params):
        img_list = self.get_img_list(path)
        tasks = [self.process_img(img, params) for img in img_list]
        return await asyncio.gather(*tasks)
