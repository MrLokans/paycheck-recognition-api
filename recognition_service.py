import logging
import sys

from PIL import Image
import pyocr
import pyocr.builders

import constants
import exceptions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)


class RecognizerService(object):

    def __init__(self, logger=logger):
        self.logger = logger
        self.ocr_tool = self.get_ocr_tool()
        self.lang = self.get_recognition_language()

    def get_ocr_tool(self):
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            error_message = "No OCR is present in the system."
            logging.error(error_message)
            raise exceptions.NoOCRToolPresent(error_message)
        ocr_tool = tools[0]
        logger.info("Using {} as OCR tool. ".format(ocr_tool.get_name()))
        return ocr_tool

    def get_recognition_language(self):
        available_languages = self.ocr_tool.get_available_languages()
        lang = constants.DEFAULT_RECOGNITION_LANGUAGE
        if lang not in available_languages:
            raise exceptions.LanguageIsNotSupported("Unknown language: {}"
                                                    .format(lang))
        return lang

    def recognize_image(self, path: str) -> str:
        image = Image.open(path)
        txt = self.ocr_tool.image_to_string(
            image,
            lang=self.lang,
            builder=pyocr.builders.TextBuilder()
        )
        return txt


def main():
    recognizer = RecognizerService()
    print(recognizer.recognize_image('example.jpg'))


if __name__ == '__main__':
    main()
