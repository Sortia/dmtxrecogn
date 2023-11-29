import cv2
from pylibdmtx.pylibdmtx import decode


class DatamatrixRecognizer:
    def __init__(self, path, segment):
        self.resized_height = 2400
        self.resized_width = None
        self.zone_scale_x = 2.5
        self.zone_scale_y = 2.5
        self.bordered = None

        self.timeout = 3
        self.path = path
        self.segment = segment
        self.count_x_segments = 3
        self.count_y_segments = 6

    @staticmethod
    def get_img(path):
        return cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    @staticmethod
    def process_img(img):
        img = cv2.convertScaleAbs(img, alpha=1.5, beta=30)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img = clahe.apply(img)

        _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        return img

    def resize_img(self, img):
        # Определение текущих размеров изображения
        height, width = img.shape[:2]

        # Расчет пропорциональной ширины на основе желаемой высоты
        aspect_ratio = width / height
        self.resized_width = int(self.resized_height * aspect_ratio)

        # Изменение размера изображения
        return cv2.resize(img, (self.resized_width, self.resized_height))

    def crop_img(self, img):
        segment_height = self.resized_height / self.count_y_segments
        segment_width = self.resized_width / self.count_x_segments

        search_area_height = int(segment_height * self.zone_scale_y)
        search_area_width = int(segment_width * self.zone_scale_x)

        y = max(0, int(((self.segment.y - 1) * segment_height) - ((search_area_height - segment_height) / self.zone_scale_y)))
        x = max(0, int(((self.segment.x - 1) * segment_width) - ((search_area_width - segment_width) / self.zone_scale_x)))

        crop_y = y + search_area_height
        crop_x = x + search_area_width

        return img[y:crop_y, x:crop_x]

    def get_dmtx_text(self, img):
        data = decode(img, timeout=self.timeout * 1000, max_count=1)

        if data:
            return data[0].data.decode('utf-8')
        else:
            return None

    def add_border(self, img):
        top, bottom, left, right = 0, 0, 0, 0
        border_width = 100

        if self.segment.y == 1:
            top = border_width

        if self.segment.y == self.count_y_segments:
            bottom = border_width

        if self.segment.x == 1:
            left = border_width

        if self.segment.x == self.count_x_segments:
            right = border_width

        self.resized_height += top + bottom
        self.resized_width += left + right

        return cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(255, 255, 255))

    def prepare_img(self, img):
        img = self.resize_img(img)
        # img = self.add_border(img)
        img = self.crop_img(img)
        img = self.process_img(img)

        return img

    def magick(self):
        img = self.get_img(self.path)
        img = self.prepare_img(img)
        cv2.imwrite("test.png", img)
        return self.get_dmtx_text(img)
