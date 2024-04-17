import pandas as pd

d = {'col1': [600, 601, 630, 930, 980], 
     'col2': [230, 260, 285, 295, 298]}
df = pd.DataFrame(data=d)

print("original:")
print(df)

def delta_encode(df, columns, ref = None):
    no_ref = False
    if ref is None:  # If reference not set, first row is the reference
        ref = df.iloc[0, :]
        no_ref = True

    encoded_df = None
    first_col = True
    for i in range(df.shape[1]):
        current_col = df.iloc[:, i]
        current_col = current_col.sub(ref.iloc[i])

        if not no_ref:
            current_col[0] = ref.iloc[i] 
        
        if first_col:
            encoded_df = pd.DataFrame(data=current_col.values, columns=[(columns[i])], dtype='Float32')
            first_col = False
        else:
            encoded_df[(columns[i])] = current_col

    return encoded_df

col_list = ["col1", "col2"]
test_df = delta_encode(df, col_list, pd.Series([600, 200]))

print("\ndelta:")
print(test_df)