import pandas as pd

from cleaning_data.cleaning_data import CleaningData
from data_to_excel.data_to_excel import DataToExcel
from config.get_config import get_config
from parse_pdf.parse_pdf import ParsePdf


config = get_config()

contents = ParsePdf(
    config['to_delete']
).get_pdf_data(
    config['pdf_filename'], config['page']
)

new_content = CleaningData().clean(contents)

data_to_excel = DataToExcel(new_content)
data_to_excel.to_excel()

final_result = data_to_excel.final_data

df = pd.DataFrame(final_result)
df.to_csv(
    config['output_filename'],
    index=False,
    columns=
    [
        'Session Title', 'Title', 'Position', 'First Name',
        'Middle Name', 'Last Name', 'Workplace'
    ]
)
