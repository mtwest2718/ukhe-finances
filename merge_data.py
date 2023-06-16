#!/usr/bin/python3

import pandas as pd
import numpy as np
from zipfile import ZipFile as zf
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
    elif tbl_id==11:
        long = long[long['head of provider marker']=='Total']
        drop_cols = list(long.columns[[3,5]])
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
            'Staff costs',
            'Surplus/(deficit) before other gains/losses and share of surplus/(deficit) in joint ventures and associates',
            'Depreciation and amortisation',
            'Interest and other finance costs'],
        3: ['Total net assets/(liabilities)',
            'Total current assets',
            'Bank overdrafts ',
            'Investments ',                 # Current assets 
            'Total creditors (amounts falling due within one year)',
            'Cash and cash equivalents ',
            'Deferred course fees',
            'Other (including grant claw back)',        # < 1 year
            'Tax and social security costs',
            'Total creditors (amounts falling due after more than one year)',
            'Other (including grant claw back) ',       # > 1 year
            'Income and expenditure reserve - unrestricted ',
            'Revaluation reserve'],
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
            'Internal funds',
            'Other external sources'],
        11: ['Performance related pay and other bonuses',
            'Total remuneration (before salary sacrifice)',
            'Basic salary paid before salary sacrifice arrangements',
            'Basic salary'],
        12: ['Average staff numbers (FTE) as disclosed in accounts',
            'Total staff numbers (FTE) as disclosed in accounts',
            'Total changes to pension provisions/ pension adjustments',
            'Changes to pension provisions',
            'Total salaries and wages',
            'Salaries and wages academic staff',
            'Salaries and wages non-academic staff',
            'Average academic staff numbers (FTE)',
            'Average non-academic staff numbers (FTE)']
    }

    categories = cats[tbl_id]
    return unfiltered[ unfiltered['category'].isin(categories) ]

def parse_zip(tbl_id):
    zip_file = f"table-{tbl_id}.zip"

    tbls = []
    # open zip file
    with zf(zip_file, 'r') as z:
        for fname in z.namelist():
            z.extractall('.',members=[fname])
            tbl = parse_table(tbl_id, csv_file=fname)
            tbls.append(tbl)            
    # concat tables together
    return pd.concat(tbls, ignore_index=True)

def parse_table(tbl_id, csv_file=None):
    if not csv_file:
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

    # drop excess category metadata
    narrowed = rename_category_col(tbl_id, df)
    # select only the desired categories from each file
    long = filter_categories(tbl_id, narrowed)

    return long

def key_financial_indicators(wide):
    # start with institutional & year indetifiers
    kfi = wide.loc[:,['ukprn', 'he provider', 'academic year']]

    ## KFIs from Table-14
    # annual surplus as % of income
    income = wide['Total income']
    pension_adjust = wide['Changes to pension provisions'] + \
        wide['Total changes to pension provisions/ pension adjustments']
    expenditure = wide['Total expenditure'] - pension_adjust
    
    surplus = wide['Surplus/(deficit) before other gains/losses and share of surplus/(deficit) in joint ventures and associates']
    kfi['surplus_vs_income'] = (surplus + pension_adjust) / income 

    # staff costs as % of income
    kfi['staff_vs_income'] = (wide['Staff costs'] - pension_adjust) / income

    # unrestricted reserves as % of income
    unreserves = wide['Income and expenditure reserve - unrestricted '] + wide['Revaluation reserve']
    kfi['unrestricted_vs_income'] = unreserves / income

    # external borrowing as % of income
    borrow = wide['Total creditors (amounts falling due within one year)'] - \
        (wide['Bank overdrafts '] + wide['Deferred course fees'] + wide['Other (including grant claw back)']) + \
        wide['Total creditors (amounts falling due after more than one year)'] - \
        wide['Other (including grant claw back) ']
    kfi['ext_borrow_vs_income'] = borrow / income

    # Days ratio of Total net assets to total expenditure
    kfi['net_assets_vs_expend'] = 365*wide['Total net assets/(liabilities)'] / expenditure

    # Ratio of current assets to current liabilities
    kfi['current_assets_vs_liability'] = wide['Total current assets'] / \
        wide['Total creditors (amounts falling due within one year)']

    # Net cash inflow from operating activities as a % of income
    kfi['ops_cash_vs_income'] = wide['Net cash inflow from operating activities'] / income

    # Net liquidity days
    liquidity = wide['Investments '] + wide['Cash and cash equivalents '] - wide['Bank overdrafts ']
    kfi['net_liquidity_days'] = 365*liquidity/(expenditure - wide['Depreciation'])

    # Debt service ratio
    financing = wide['Interest paid'] + wide['Repayments of amounts borrowed'] + \
        wide['Interest element of finance lease and service concession payments'] + \
        wide['Capital element of finance lease and service concession payments']
    kfi['debt_service_ratio'] = wide['Net cash inflow from operating activities'] / np.abs(financing)

    ## Other KFIs (of potential interest to staff)
    # Pay per FTE in k£
    total_staff_num = wide['Average staff numbers (FTE) as disclosed in accounts'] + \
        wide['Total staff numbers (FTE) as disclosed in accounts']
    kfi['avg_salary'] = wide['Total salaries and wages'] / total_staff_num
    kfi['avg_remuneration'] = (wide['Staff costs'] - pension_adjust) / total_staff_num
    kfi['academic_salary'] = wide['Salaries and wages academic staff'] / wide['Average academic staff numbers (FTE)']
    kfi['ps_staff_salary'] = wide['Salaries and wages non-academic staff'] / wide['Average non-academic staff numbers (FTE)']

    # Other sources as % of total income
    kfi['uk_vs_total_fees'] = wide['Total HE course fees'] / wide['Total UK fees']
    kfi['fbg_vs_income'] = wide['Funding body grants'] / income
    kfi['research_vs_income'] = wide['Total research grants and contracts'] / income
    kfi['donate_vs_income'] = wide['Total donations and endowments'] / income
    kfi['reside_cater_vs_income'] = wide['Total residences and catering operations (including conferences)'] / income
    kfi['total_income'] = income

    # Other expenditures
    kfi['finance_vs_expend'] = wide['Interest and other finance costs'] / expenditure
    kfi['depreciate_amort_vs_expend'] = wide['Depreciation and amortisation'] / expenditure
    kfi['staff_vs_expend'] = (wide['Staff costs'] - pension_adjust) / expenditure
    kfi['capital_vs_expend'] = wide['Total actual spend'] / expenditure
    kfi['total_expenditure'] = expenditure

    # Head of provider remuneration
    basic = wide['Basic salary paid before salary sacrifice arrangements'] + wide['Basic salary']
    remuneration = wide['Total remuneration (before salary sacrifice)']
    kfi['vc_bonus_vs_salary'] = wide['Performance related pay and other bonuses'] / basic
    kfi['galt_index_salary'] = basic / kfi['avg_salary']
    kfi['galt_index_total'] = remuneration / kfi['avg_remuneration']

    return kfi


def main():
    tbls = [parse_table(T) for T in [1,3,4,6,7,9,12]]
    tbls.append(parse_zip(11))

    # merge tables vertically
    long_tbl = pd.concat(tbls, ignore_index=True)
    LT = long_tbl.astype({'value':'float64'})

    # pivot table long to wide
    wide = pd.pivot_table(
        LT, values=["value"], columns=['category'], 
        index=["ukprn","he provider","academic year"], fill_value=0)
    WV = wide['value'].reset_index()

    WV.to_csv('wide.csv')

    # Table of Key Financial Indicators
    kfi = key_financial_indicators(WV)
    kfi = kfi.round(3)
    kfi.to_csv('kfi.csv')

    return kfi

if __name__ == "__main__":
    main()


