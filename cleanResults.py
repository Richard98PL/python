import os
import openpyxl

def cleanResults():
    file_path = os.path.abspath("Results/results.xlsx")
    workbook = openpyxl.load_workbook(file_path)
    print(file_path)

    # Select the active worksheet
    worksheet = workbook.active
    worksheet.delete_rows(1, worksheet.max_row)

    rows = [['SCENARIO', 'API', 'DATA_SIZE', 'TIME']]
    for row in rows:
        worksheet.append(row)

    # Save the workbook
    workbook.save(file_path)