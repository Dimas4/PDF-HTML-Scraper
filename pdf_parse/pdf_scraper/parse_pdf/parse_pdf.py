from PyPDF2 import PdfFileReader


class ParsePdf:
    def __init__(self, to_delete: list) -> None:
        assert isinstance(to_delete, list)
        self.to_delete = to_delete

    def __clear_data(self, contents: str) -> str:
        """
        Remove extra lines from the contents
        :param contents:
        :return: updated contents
        """
        for line in self.to_delete:
            contents = contents.replace(line, '')
        return contents

    def get_pdf_data(self, filename: str, page: int) -> list:
        """
        Get text from PDF via '\n'
        :param filename:
        :param page:
        :return: text
        """
        with open(filename, 'rb') as f:
            reader = PdfFileReader(f)
            contents = reader.getPage(page).extractText()
        return self.__clear_data(contents).split('\n')
