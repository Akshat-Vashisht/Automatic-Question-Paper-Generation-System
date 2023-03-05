import pandas as pd

df = pd.read_excel('TestQuestionBank.xlsx')

df = df[(df['Marks'] == 5) & (df['Difficulty'] == "Easy")]

listOf5 = df['Question'].to_list()

for i in listOf5:
    print(i)
