#!/usr/bin/python3

import pandas as pd
import pdb

def make_negative(x):
    if isinstance(x,str):
        return '-' + x[1:-1] if x.startswith('(') else x
    else:
        return x

def rename_category_col(tbl_id, long):
    if tbl_id==12:
        drop_cols = long.columns[4]
    elif tbl_id==6:
        long = long[long['source of fees']=='Total']
        drop_cols = list(long.columns[[2,4]])
    else:
        if tbl_id==9:
            long = long[long['type of asset']=='Total capital expenditure']
        drop_cols = list(long.columns[3:-2])
    # dropping category metadata columns
    if drop_cols:
        long = long.drop(columns=drop_cols)

    return long.rename(columns={long.columns[-2]: 'category'})

def filter_categories(tbl_id, unfiltered):
    cats = {
        1: ['Total income',
            'Total expenditure',
            'Staff costs'],
        3: ['Total net assets/(liabilities)',
            'Total current assets',
            'Bank overdrafts ',
            'Investments ',                 # Current assets 
            'Total creditors (amounts falling due within one year)',
            'Cash and cash equivalents ',
            'Deferred course fees',
            'Other (including grant claw back)',
            'Tax and social security costs',
            'Total creditors (amounts falling due after more than one year)',
            'Other (including grant claw back) '],
        4: ['Net cash inflow from operating activities',
            'Depreciation',
            'Interest paid',
            'Repayments of amounts borrowed',
            'Interest element of finance lease and service concession payments',
            'Capital element of finance lease and service concession payments'],
        6: ['Total tuition fees and education contracts',
            'Total HE course fees',
            'Total UK fees'],
        7: ['Total research grants and contracts',
            'Total other income',
            'Total donations and endowments',
            'Total residences and catering operations (including conferences)',
            'Funding body grants'],         # income from
        9: ['Total actual spend',
            'Funding body grants',          # money from. used for capital expenditures
            'Internal funds',
            'Other external sources'],
        12: ['Average staff numbers (FTE) as disclosed in accounts',
            'Total staff numbers (FTE) as disclosed in accounts',
            'Total changes to pension provisions/ pension adjustments',
            'Changes to pension provisions',
            'Total salaries and wages','Salaries and wages academic staff',
            'Salaries and wages non-academic staff',
            'Average academic staff numbers (FTE)',
            'Average non-academic staff numbers (FTE)']
    }

    categories = cats[tbl_id]
    df = unfiltered[ unfiltered['category'].isin(categories) ]
    # double use of "Funding body grants"
    if tbl_id==7:
        df['category'].mask(
            df['category']=='Funding body grants','Total funding body grant income')
    return df


def parse_table(tbl_id):
    # name of the CSV file 
    csv_file = f"table-{tbl_id}.csv"
    print(csv_file)

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
    df = df.convert_dtypes()

    # drop excess category metadata
    narrowed = rename_category_col(tbl_id, df)
    # select only the desired categories from each file
    long = filter_categories(tbl_id, narrowed)

    print(long.columns)

    return long

def main():
    tbls = [parse_table(T) for T in [1,3,4,6,7,9,12]]
    # merge tables vertically
    long_tbl = pd.concat(tbls, ignore_index=True)

    print(long_tbl)

if __name__ == "__main__":
    main()


