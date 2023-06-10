#!/usr/bin/python3

import pandas as pd
import pdb

tbls = [1,3,4,6,7,9,10,12,14]

def make_negative(x):
    if isinstance(x,str):
        return '-' + x[1:-1] if x.startswith('(') else x
    else:
        return x

def read_table(tbl_id):
    # name of the CSV file 
    csv_file = f"table-{tbl_id}.csv"

    full_tbl = pd.read_csv(csv_file, skiprows=12)
    # make all column names lower case for easier filtering
    full_tbl.columns = full_tbl.columns.str.lower()
    # drop unneed columns
    tbl = full_tbl.drop(columns=['country of he provider','region of he provider'])
    if 'financial year end' in tbl.columns:
        tbl.drop(columns=['financial year end'], inplace=True) 
    # filter out sector totals
    tbl.dropna(subset=["ukprn"], inplace=True)

    # remove 2015/16
    df = tbl[ tbl['academic year']!='2015/16' ]
    # keep only rows for end-of-year report
    if 'year end month' in df.columns:
        df = df[ df['year end month']=='All' ]
        df.drop(columns=['year end month'], inplace=True) 
    
    # rename value column
    val_col = [c for c in df.columns if 'value' in c][0]
    df = df.rename(columns={val_col:'value'})
    # remove NaN values from "value" column
    df = df.dropna(subset=["value"])

    # convert values in parenthese into negative numbers
    numbers = df['value'].apply(make_negative)
    df.update(numbers)
    df.convert_dtypes()

    return df

long = read_table(tbls[0]) 



