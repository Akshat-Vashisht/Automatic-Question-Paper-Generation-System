import openpyxl

marks5 = set()

wb = openpyxl.load_workbook("TestQuestionBank.xlsx")
ws = wb["Sheet1"]
lastRow = ws.max_row
print(lastRow)
