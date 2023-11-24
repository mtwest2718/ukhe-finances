#!/usr/bin/python3

import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import pdb
import argparse
import pathlib
import sys

def average_salary(tbl, ukprn=10007792, outdir=None, group='russell group filter'):
    print("\tAnnual average salary for staff in k£")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    name = uni['he provider'].unique()[0]

    avg_salary = sb.swarmplot(
        data=tbl,
        x='academic year', y='avg_salary', hue=group,
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=avg_salary,
        x='academic year', y='avg_salary',
        color='g', label=name, zorder=2, marker='o', markersize=10
    )
    avg_salary.set_ylim(25,65)
    avg_salary.set(
        xlabel='Academic Year', 
        ylabel='Annual Salary (k£)',
        title='Average UKHE staff salary per year'
    )
    plt.legend(loc='upper left', title=group.title())
    plt.savefig(outdir.joinpath('avg_salary.png'))
    plt.clf()

def staffcosts_income(tbl, ukprn=10007792, outdir=None, group='russell group filter'):
    print("\tProportion of Income spent on Staff Costs")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    name = uni['he provider'].unique()[0]

    staff_income = sb.swarmplot(
        data=tbl,
        x='academic year', y='staff_vs_income', hue=group,
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=staff_income,
        x='academic year', y='staff_vs_income',
        color='g', label=name, zorder=2, marker='o', markersize=10
    )
    staff_income.set_ylim(0.1,0.8)
    staff_income.set(
        xlabel='Academic Year', 
        ylabel='Proportion of Total Income',
        title='What proportion of income is spent on staff costs'
    )
    plt.legend(loc='lower left', title=group.title())
    plt.savefig(outdir.joinpath('staff_vs_income.png'))
    plt.clf()

def staffcosts_expenditure(tbl, ukprn=10007792, outdir=None, group='russell group filter'):
    print("\tWhat proportion of Total Expenditure is Staff Costs")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    name = uni['he provider'].unique()[0]

    staff_expend = sb.swarmplot(
        data=tbl,
        x='academic year', y='staff_vs_expend', hue=group,
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=staff_expend,
        x='academic year', y='staff_vs_expend',
        color='g', label=name, zorder=2, marker='o', markersize=10
    )
    staff_expend.set_ylim(0.1,0.8)
    staff_expend.set(
        xlabel='Academic Year', 
        ylabel='Proportion of Total Expenditure',
        title='What proportion of annual expenditure is staff costs'
    )
    plt.legend(loc='lower left', title=group.title())
    plt.savefig(outdir.joinpath('staff_vs_expend.png'))
    plt.clf()

def annual_surplus_income(tbl, ukprn=10007792, outdir=None, group='russell group filter'):
    print("\tHow big is the annual surplus, scaled by the total income")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    name = uni['he provider'].unique()[0]

    surplus_income = sb.swarmplot(
        data=tbl,
        x='academic year', y='surplus_vs_income', hue=group,
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=surplus_income,
        x='academic year', y='surplus_vs_income',
        color='g', label=name, zorder=2, marker='o', markersize=10
    )
    surplus_income.set_ylim(-0.2,0.25)
    surplus_income.set(
        xlabel='Academic Year', 
        ylabel='Proportion of Total Income',
        title='How big is the annual surplus relative to total income?'
    )
    plt.legend(loc='lower left', title=group.title())
    plt.savefig(outdir.joinpath('surplus_vs_income.png'))
    plt.clf()

def unrestricted_reserves(tbl, ukprn=10007792, outdir=None, group='russell group filter'):
    print("\tUnrestricted Reserves, scaled by the total income")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    name = uni['he provider'].unique()[0]

    ax = sb.swarmplot(
        data=tbl,
        x='academic year', y='unrestricted_vs_income', hue=group,
        dodge=True, zorder=2, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=ax,
        x='academic year', y='unrestricted_vs_income',
        color='g', label=name, zorder=3, marker='o', markersize=10
    )
    ax.axhline(0.5, label='"reasonable" lowerbound', color='black', linestyle='dashed', zorder=1)
    ax.set_ylim(-1,5.25)
    ax.set(
        xlabel='Academic Year', 
        ylabel='Proportion of Total Income',
        title='How big are the Unrestricted Reserves relative to total income?'
    )
    plt.legend(loc='upper left', title=group.title())
    plt.savefig(outdir.joinpath('reserves_vs_income.png'))
    plt.clf()

def external_borrowing(tbl, ukprn=10007792, outdir=None, group='russell group filter'):
    print("\tThe scale of external borrowing by year")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    name = uni['he provider'].unique()[0]

    ax = sb.swarmplot(
        data=tbl,
        x='academic year', y='ext_borrow_vs_income', hue=group,
        dodge=True, zorder=2, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=ax,
        x='academic year', y='ext_borrow_vs_income',
        color='g', label=name, zorder=3, marker='o', markersize=10
    )
    ax.axhline(0.5, label='"normal" range', color='black', linestyle='dashed', zorder=1)
    ax.set_ylim(-0.1,2.5)
    ax.set(
        xlabel='Academic Year', 
        ylabel='Proportion of Total Income',
        title='How much external borrowing does each institution do?'
    )
    plt.legend(loc='upper left', title=group.title())
    plt.savefig(outdir.joinpath('extborrow_vs_income.png'))
    plt.clf()

def asset_liability_ratio(tbl, ukprn=10007792, outdir=None, group='russell group filter'):
    print("\tThe ratio of currenet assets to liabilities")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    name = uni['he provider'].unique()[0]

    ax = sb.swarmplot(
        data=tbl,
        x='academic year', y='current_assets_vs_liability', hue=group,
        dodge=True, zorder=2, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=ax,
        x='academic year', y='current_assets_vs_liability',
        color='g', label=name, zorder=3, marker='o', markersize=10
    )
    ax.axhline(1, label='"good" lowerbound', color='black', linestyle='dashed', zorder=1)
    ax.set_ylim(-0.1,10)
    ax.set(
        xlabel='Academic Year', 
        ylabel='Ratio of assets to liabilities',
        title='Measure of ability to pay near future debts from "liquid" assets.'
    )
    plt.legend(loc='upper left', title=group.title())
    plt.savefig(outdir.joinpath('asset_vs_liabilities.png'))
    plt.clf()

def change_tuition_fees(tbl, ukprn=10007792, outdir=None, group='russell group filter'):
    # Get details for single uni
    uni_name = tbl.loc[tbl['ukprn']==ukprn, 'he provider'].unique()[0]

    # rescale tuition fees from 2016/17 value to compare growth levels
    w = pd.pivot_table(tbl, values=['tuition_fees'], columns=['academic year'], index=['ukprn','russell group filter'])
    norm = w.div(w[('tuition_fees','2016/17')], axis=0, level=1)
    L = norm.stack()
    L.reset_index()
    pct = L.add({'tuition_fees': -1})
    pct = pct.mul({'tuition_fees': 100})

    print("\tGauging how tuition fees changes over time for each institution")
    tuition_fees = sb.lineplot(
        data=pct,
        x='academic year', y='tuition_fees', hue=group,
        alpha=0.6, estimator=None, units='ukprn', lw=3, zorder=1
    )
    sb.scatterplot(
        data=pct.loc[ukprn], ax=tuition_fees,
        x='academic year', y='tuition_fees',
        color='g', s=200, label=uni_name, zorder=2
    )
    tuition_fees.set_ylim(-25,150)
    tuition_fees.set(
        xlabel='Academic Year', 
        ylabel='Percent change in tuition fee income',
        title='How has UKHE income from tuition fees changed over time?'
    )
    plt.legend(loc='upper left', title=group.title())
    plt.savefig(outdir.joinpath('total_tuition_fees.png'))
    plt.clf()

def tuition_vs_surplus(tbl, ukprn=10007792, outdir=None, group='russell group filter', year='2020/21'):
    print("\tThe relationship between tuition fee income and annual surplus")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    name = uni['he provider'].unique()[0]

    fee_income = sb.scatterplot(
        data=tbl[ tbl['academic year']==year ], 
        x='surplus_vs_income', y='total_fees_vs_income', hue=group,
        zorder=1, legend=True
    )
    sb.scatterplot(
        data=uni[ uni['academic year']==year ], ax=fee_income,
        x='surplus_vs_income', y='total_fees_vs_income',
        color='g', s=200, label=name, zorder=2
    )
    fee_income.set_xlim(-0.2,0.25)
    fee_income.set_ylim(0,1)
    fee_income.set(
        xlabel='Total annual surplus relative to Total income', 
        ylabel='Proportion of income from student fees', 
        title=f'Relationship beween fee income and annual surplus in {year}'
    )
    plt.legend(loc='lower left', title=group.title())
    plt.savefig(outdir.joinpath('fees_vs_surplus.png'))
    plt.clf()

def tuition_fee_proportion(tbl, ukprn=10007792, outdir=None, group='russell group filter'):
    print("\tUnderstand what portion of income comes from Student Fees")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    name = uni['he provider'].unique()[0]

    fee_income = sb.scatterplot(
        data=tbl[ tbl['academic year']=='2021/22' ], 
        x='total_fees_vs_income', y='uk_vs_total_fees', hue=group,
        zorder=1, legend=True
    )
    sb.scatterplot(
        data=uni[ uni['academic year']=='2021/22' ], ax=fee_income,
        x='total_fees_vs_income', y='uk_vs_total_fees',
        color='g', s=200, label=name, zorder=2
    )
    fee_income.set_xlim(0,1)
    fee_income.set_ylim(0,1)
    fee_income.set(
        xlabel='Proportion of income from student fees', 
        ylabel='Proportion of fee income from UK students',
        title='Contribution of student fees to UKHE income in 2021/22'
    )
    plt.legend(loc='lower right', title=group.title())
    plt.savefig(outdir.joinpath('fees_vs_income.png'))
    plt.clf()

def capital_projects(tbl, ukprn=10007792, outdir=None, group='russell group filter'):
    print("\tHow of total expenditures is spent on capital projects")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    name = uni['he provider'].unique()[0]

    capital_expend = sb.swarmplot(
        data=tbl,
        x='academic year', y='capital_vs_expend', hue=group,
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=capital_expend,
        x='academic year', y='capital_vs_expend',
        color='g', label=name, zorder=2, marker='o', markersize=10
    )
    capital_expend.set_ylim(0,0.8)
    capital_expend.set(
        xlabel='Academic Year', 
        ylabel='Proportion of annual Total Expenditure',
        title='What proportion of annual expenditure is on Capital Costs?'
    )
    plt.legend(loc='upper center', title=group.title())
    plt.savefig(outdir.joinpath('capital_expenditure.png'))
    plt.clf()

def galt_index(tbl, ukprn=10007792, outdir=None, group='russell group filter'):
    print("\tRatio of VC remuneration to that average remuneration of staff.")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    name = uni['he provider'].unique()[0]

    vc = sb.swarmplot(
        data=tbl,
        x='academic year', y='vc_avg_remunerate', hue=group,
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=vc,
        x='academic year', y='vc_avg_remunerate',
        color='g', label=name, zorder=2, marker='o', markersize=10
    )
    vc.set_ylim(0,14)
    vc.set(
        xlabel='Academic Year', 
        ylabel='Ratio of VC to staff average',
        title="How does the VC's remuneration compare to the rest of staff?"
    )
    plt.legend(loc='lower left', title=group.title())
    plt.savefig(outdir.joinpath('vc_compensation.png'))
    plt.clf()


def compare_staff_salary(tbl, acyear='2021/22', ukprn=10007792, outdir=None, group='russell group filter'):
    print("\tComparing average salaries for academics and ps-staff")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    name = uni['he provider'].unique()[0]

    ax = sb.scatterplot(
        data=tbl[tbl['academic year']==acyear], 
        x='academic_salary', y='ps_staff_salary', hue=group,
        zorder=2, legend=True
    )
    sb.scatterplot(
        data=uni[ uni['academic year']==acyear ], ax=ax,
        x='academic_salary', y='ps_staff_salary',
        color='g', s=200, label=name, zorder=3
    )
    ax.set_ylim(20,80)
    ax.set_xlim(20,80)
    ax.set(
        xlabel='Average Salary (k£) for Academic Staff', 
        ylabel='Average Salary (k£) for Professional Services',
        title='Comparing Salaries between Academic and PS Staff for '+acyear
    )
    plt.plot(
        [20, 80], [20, 80], zorder=1,
        color='black', linestyle='dashed', linewidth=2, label='Equality'
    )
    plt.legend(loc='upper right', title=group.title())
    plt.savefig(outdir.joinpath('compare_salaries.png'))
    plt.clf()

def net_liquidity_days(tbl, ukprn=10007792, outdir=None, group='russell group filter'):
    print("\tNet Liquidity Days")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    name = uni['he provider'].unique()[0]

    surplus_income = sb.swarmplot(
        data=tbl,
        x='academic year', y='net_liquidity_days', hue=group,
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=surplus_income,
        x='academic year', y='net_liquidity_days',
        color='g', label=name, zorder=2, marker='o', markersize=10
    )
    surplus_income.axhline(60, label='Lower Bound', color='black', linestyle='dashed')
    surplus_income.set_ylim(-10,600)
    surplus_income.set(
        xlabel='Academic Year', 
        ylabel='Days of Operating Cost Coverage',
        title='A measure of institutions abilitity to costs from liquid assets'
    )
    plt.legend(loc='upper left', title=group.title())
    plt.savefig(outdir.joinpath('net_liquidity_days.png'))
    plt.clf()

def operating_cash_flow(tbl, ukprn=10007792, outdir=None, group='russell group filter'):
    print("\tNet cash flow")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    name = uni['he provider'].unique()[0]

    ax = sb.swarmplot(
        data=tbl,
        x='academic year', y='ops_cash_vs_income', hue=group,
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=ax,
        x='academic year', y='ops_cash_vs_income',
        color='g', label=name, zorder=2, marker='o', markersize=10
    )
    ax.axhline(0.05, label='"alright" lowerbound', color='black', linestyle='dashed', zorder=1)
    ax.set_ylim(-0.2,0.425)
    ax.set(
        xlabel='Academic Year', 
        ylabel='Proportion of Total Income',
        title='What is the net cash flow from Operating Actives relative to income?'
    )
    plt.legend(loc='upper left', title=group.title())
    plt.savefig(outdir.joinpath('opscash_vs_income.png'))
    plt.clf()

def comparing_surplus_measures(tbl, acyear='2021/22', ukprn=10007792, outdir=None, group='russell group filter'):
    print("\tAnnual surplus measures for "+acyear)

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    name = uni['he provider'].unique()[0]

    ax = sb.scatterplot(
        data=tbl[tbl['academic year']==acyear], 
        x='ops_cash_vs_income', y='surplus_vs_income', hue=group,
        zorder=3, legend=True
    )
    sb.scatterplot(
        data=uni[ uni['academic year']==acyear ], ax=ax,
        x='ops_cash_vs_income', y='surplus_vs_income',
        color='g', s=200, label=name, zorder=4
    )
    ax.axhline(0, color='black', linestyle='dashed', zorder=1)
    ax.axvline(0.05, color='black', linestyle='dotted', zorder=2)
    ax.set_xlim(-0.2,0.425)
    ax.set_ylim(-0.2,0.25)
    ax.set(
        xlabel='Net cash flow from operating activities', 
        ylabel='Total annual surplus',
        title='Financial surplus measures relative to total income in '+acyear,
    )
    plt.legend(loc='lower right', title=group.title())
    plt.savefig(outdir.joinpath('compare_surplus.png'))
    plt.clf()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-csv', type=argparse.FileType('r'), 
        help="Path to CSV data that the plots are generated from")
    parser.add_argument('-f', '--figure-dir', type=pathlib.Path,
        help="The directory path where the figures should be saved")
    parser.add_argument('-u', '--ukprn', type=int, default=10007792,
        help="The UK PRovider Number for the institution of interest")
    args = parser.parse_args() 

    # Key Financial Indicators CSV file
    tbl = pd.read_csv(args.input_csv)

    # Checking input arguments
    if not args.figure_dir.exists():
        sys.exit(f"The dir <{args.figure_dir}> does not exist.")
    if args.ukprn not in tbl['ukprn'].values:
        sys.exit(f"{args.ukprn} is not a valid UK Provider Number.")
    else:
        uni = tbl.loc[tbl['ukprn']==args.ukprn, 'he provider'].unique()[0]
        print(f"{args.ukprn} corresponds to {uni}")

    # Figure settings
    sb.set_theme(
        context="talk",
        style="whitegrid",
        rc={"figure.figsize":(16, 9), "figure.dpi":300, "savefig.dpi":300}
    )

    print('Swarm Plots')
    net_liquidity_days(tbl, ukprn=args.ukprn, outdir=args.figure_dir)
    operating_cash_flow(tbl, ukprn=args.ukprn, outdir=args.figure_dir)
    galt_index(tbl, ukprn=args.ukprn, outdir=args.figure_dir)
    capital_projects(tbl, ukprn=args.ukprn, outdir=args.figure_dir)
    staffcosts_income(tbl, ukprn=args.ukprn, outdir=args.figure_dir)
    staffcosts_expenditure(tbl, ukprn=args.ukprn, outdir=args.figure_dir)
    average_salary(tbl, ukprn=args.ukprn, outdir=args.figure_dir)
    annual_surplus_income(tbl, ukprn=args.ukprn, outdir=args.figure_dir)
    unrestricted_reserves(tbl, ukprn=args.ukprn, outdir=args.figure_dir)
    external_borrowing(tbl, ukprn=args.ukprn, outdir=args.figure_dir)
    asset_liability_ratio(tbl, ukprn=args.ukprn, outdir=args.figure_dir)

    print('Scatter Plots')
    compare_staff_salary(tbl, ukprn=args.ukprn, outdir=args.figure_dir)
    comparing_surplus_measures(tbl, ukprn=args.ukprn, outdir=args.figure_dir)
    tuition_fee_proportion(tbl, ukprn=args.ukprn, outdir=args.figure_dir)
    tuition_vs_surplus(tbl, ukprn=args.ukprn, outdir=args.figure_dir)

    print('Line Plots') 
    change_tuition_fees(tbl, ukprn=args.ukprn, outdir=args.figure_dir)

if __name__ == "__main__":
    main()



