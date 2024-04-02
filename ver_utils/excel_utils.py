import pandas as pd
import openpyxl

def sample():
    df = pd.DataFrame([[11, 21, 31], [12, 22, 32], [31, 32, 33]],
                     columns=['a', 'b', 'c'])

    print(df)
    df.to_excel(r"C:\Users\yusufz1\Downloads\trial.xlsx", sheet_name="try1", index=False)

if __name__ == "__main__":
    print("start")
    sample()
    print("done")