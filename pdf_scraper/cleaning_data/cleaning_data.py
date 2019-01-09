class CleaningData:
    @staticmethod
    def __double_add(content: list, to_add: str, index: int) -> None:
        """
        Add to to_add the contents
        :param content:
        :param to_add:
        :param index:
        :return: None
        """
        content.append(to_add[:index])
        content.append(to_add[index:])

    @staticmethod
    def __long__line_case(content: list, line: str) -> bool:
        """
        Handles the case of a long line. When position 25 is a number
        :param content:
        :param line:
        :return: bool
        """
        if len(line) > 25:
            if line[25].isdigit():
                content.append(line[26:].strip())
                return True
        return False

    def __comma_case(self, content: list, line: str) -> bool:
        """
        Handles the case of a comma line. When position 25 is a number
        :param content:
        :param line:
        :return: bool
        """
        if line[12].isdigit():
            final_line = line[13:].strip()
            if 'Opening Remarks' in final_line:
                self.__double_add(content, final_line, 15)
            else:
                content.append(final_line)
            return True
        return False

    @staticmethod
    def __specific_string_case(content: list, line: str, strings: list) -> bool:
        """
        Adds specific data to the string
        :param content:
        :param line:
        :param strings:
        :return: bool
        """
        for string in strings:
            if line.strip() == string:
                content[-1] += f' {line.strip()}'
                return True
        return False

    def clean(self, contents: list) -> list:
        """
        Clears data and returns new data
        :param contents:
        :return: list
        """
        _new_content = []

        for line in contents:
            if line:
                try:
                    if self.__long__line_case(_new_content, line):
                        continue

                    if self.__comma_case(_new_content, line):
                        continue

                    if 'Professor Grace Wong' in line:
                        self.__double_add(_new_content, line, 33)
                        continue

                    if self.__specific_string_case(
                            _new_content,
                            line,
                            ['substitutions', 'the study of Liver Diseases']
                    ):
                        continue

                    if line.strip() == 'Professor Henry Chan':
                        line += ' (Hong Kong)'

                    _new_content.append(line.strip())
                except IndexError:
                    pass
        return _new_content
