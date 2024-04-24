import pandas as pd


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