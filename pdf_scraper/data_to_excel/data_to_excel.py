class DataToExcel:
    def __init__(self, content) -> None:
        self.result = {line: [] for line in content if 'Symposium' in line}
        self.result['unsigned'] = []
        self.content = content

        self._final_data = []

        self.__add_lines_to_result()

    def __add_lines_to_result(self) -> None:
        """
        Adds lines for the result dict
        Example: adds "Fibrosis regression after HBeAg seroconversion" to
        "Symposium I: Chronic Hepatitis B" key

        :return: dict
        """
        symposium = None

        for ind, line in enumerate(self.content):
            if line == '':
                continue

            if 'Symposium' in line:
                symposium = line

            self.result[symposium if symposium else 'unsigned'].append(line)

    def __add_unsigned_data(self) -> None:
        """
        Adds unsigned data to the "_final_data" from the file top
        :return: None
        """
        deleted_comma = self.result['unsigned'][1].split(',')
        place = deleted_comma[-1]
        name = deleted_comma[0].split()[1:]

        self._final_data.append({
            'Title': self.result['unsigned'][0],
            'Position': 'Speaker',
            'First Name': name[0],
            'Last Name': name[1],
            'Workplace': place
        })

    def __add_index_0(self, last: str, data_plus_one: str) -> None:
        """
        Handles case with index == 0 and 'Symposium' in data.
        Parses data and adds to "_final_data"
        :param last:
        :param data_plus_one:
        :return: None
        """
        names = (data_plus_one
                    .replace('(Chairpersons: ', '')
                    .replace(')', '')
                    .split('and ')
                 )

        for name in names:
            name_parts = name.split()[1:]

            data_to_add = {
                'Session title': last,
                'Title': '',
                'Position': 'Chairperson',
                'First Name': name_parts[0],
            }

            if len(name_parts) == 2:
                data_to_add['Last Name'] = name_parts[1]

            elif len(name_parts) == 3:
                data_to_add['Middle name'] = name_parts[1]
                data_to_add['Last Name'] = name_parts[2]

            self._final_data.append(data_to_add)

    def __add_index_not_0(
            self,
            data: str,
            last: str,
            data_plus_one: str
    ) -> None:
        """
        Handles case with index != 0 and 'Symposium' in data.
        Parses data and adds to "_final_data"
        :param data:
        :param last:
        :param data_plus_one:
        :return:
        """
        name, country = data_plus_one.split('(')
        name_parts = name.split()[1:]
        country = country.replace(')', '')

        data_to_add = {
            'Session title': last,
            'Title': data,
            'Position': 'Speaker',
            'Middle Name': '',
            'Workplace': country
        }

        if len(name_parts) == 2:
            data_to_add['First Name'] = name_parts[0]
            data_to_add['Last Name'] = name_parts[1]

            self._final_data.append(data_to_add)

        elif len(name_parts) == 3:
            data_to_add['First Name'] = ' '.join(
                name_parts[:2]
            ) if name_parts[1].strip() != 'de' else name_parts[0]

            data_to_add['Last Name'] = (name_parts[2]
                                        if name_parts[1].strip() != 'de'
                                        else ' '.join(name_parts[1:])
                                        )

            self._final_data.append(data_to_add)

    def to_excel(self) -> None:
        """
        Prepares data for conversion to excel
        :return: None
        """
        self.__add_unsigned_data()

        last = None

        for key, value in self.result.items():
            if last != key:
                last = key

            for ind, data in enumerate(value[::2]):
                data_plus_one = value[ind * 2 + 1]

                if ind == 0 and 'Symposium' in data:
                    self.__add_index_0(last, data_plus_one)

                elif 'Opening Remarks' not in data:
                    self.__add_index_not_0(data, last, data_plus_one)

    @property
    def final_data(self) -> list:
        """
        Returns "_final_data"
        :return: list
        """
        return self._final_data
