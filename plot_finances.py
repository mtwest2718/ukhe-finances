#!/usr/bin/python3

import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import pdb


def average_salary(tbl, ukprn=10007792):
    print("\tAnnual average salary for staff in k£")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    avg_salary = sb.swarmplot(
        data=tbl,
        x='academic year', y='avg_salary', hue='russell group filter',
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=avg_salary,
        x='academic year', y='avg_salary',
        color='g', label='Exeter', zorder=2, marker='o', markersize=10
    )
    avg_salary.set_ylim(25,60)
    avg_salary.set(
        xlabel='Academic Year', 
        ylabel='Annual Salary (k£)',
        title='Average UKHE staff salary per year'
    )
    plt.legend(loc='lower right', title='Russell Group')
    plt.savefig('./figures/avg_salary.png')
    plt.clf()

def staffcosts_income(tbl, ukprn=10007792):
    print("\tProportion of Income spent on Staff Costs")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    staff_income = sb.swarmplot(
        data=tbl,
        x='academic year', y='staff_vs_income', hue='russell group filter',
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=staff_income,
        x='academic year', y='staff_vs_income',
        color='g', label='Exeter', zorder=2, marker='o', markersize=10
    )
    staff_income.set_ylim(0.1,0.8)
    staff_income.set(
        xlabel='Academic Year', 
        ylabel='Proportion of Total Income',
        title='What proportion of income is spent on staff costs'
    )
    plt.legend(loc='lower right', title='Russell Group')
    plt.savefig('./figures/staff_vs_income.png')
    plt.clf()

def staffcosts_expenditure(tbl, ukprn=10007792):
    print("\tWhat proportion of Total Expenditure is Staff Costs")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    staff_expend = sb.swarmplot(
        data=tbl,
        x='academic year', y='staff_vs_expend', hue='russell group filter',
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=staff_expend,
        x='academic year', y='staff_vs_expend',
        color='g', label='Exeter', zorder=2, marker='o', markersize=10
    )
    staff_expend.set_ylim(0.1,0.8)
    staff_expend.set(
        xlabel='Academic Year', 
        ylabel='Proportion of Total Expenditure',
        title='What proportion of annual expenditure is staff costs'
    )
    plt.legend(loc='lower right', title='Russell Group')
    plt.savefig('./figures/staff_vs_expend.png')
    plt.clf()

def annual_surplus_income(tbl, ukprn=10007792):
    print("\tHow big is the annual surplus, scaled by the total income")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    surplus_income = sb.swarmplot(
        data=tbl,
        x='academic year', y='surplus_vs_income', hue='russell group filter',
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=surplus_income,
        x='academic year', y='surplus_vs_income',
        color='g', label='Exeter', zorder=2, marker='o', markersize=10
    )
    surplus_income.set_ylim(-0.2,0.25)
    surplus_income.set(
        xlabel='Academic Year', 
        ylabel='Proportion of Total Income',
        title='How big is the annual surplus relative to total income?'
    )
    plt.legend(loc='lower left', title='Russell Group')
    plt.savefig('./figures/surplus_vs_income.png')
    plt.clf()

def change_tuition_fees(tbl, ukprn=10007792):
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
        x='academic year', y='tuition_fees', hue='russell group filter',
        alpha=0.6, estimator=None, units='ukprn', lw=3, zorder=1
    )
    sb.scatterplot(
        data=pct.loc[ukprn], ax=tuition_fees,
        x='academic year', y='tuition_fees',
        color='g', s=200, label='Exeter', zorder=2
    )
    tuition_fees.set_ylim(-25,150)
    tuition_fees.set(
        xlabel='Academic Year', 
        ylabel='Percent change in tuition fee income',
        title='How has UKHE income from tuition fees changed over time?'
    )
    plt.legend(loc='upper left', title='Russell Group')
    plt.savefig('./figures/total_tuition_fees.png')
    plt.clf()

def tuition_fee_proportion(tbl, ukprn=10007792):
    print("\tUnderstand what portion of income comes from Student Fees")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    fee_income = sb.scatterplot(
        data=tbl[ tbl['academic year']=='2021/22' ], 
        x='total_fees_vs_income', y='uk_vs_total_fees', hue='russell group filter',
        zorder=1, legend=True
    )
    sb.scatterplot(
        data=uni[ uni['academic year']=='2021/22' ], ax=fee_income,
        x='total_fees_vs_income', y='uk_vs_total_fees',
        color='g', s=200, label='Exeter', zorder=2
    )
    fee_income.set(
        xlabel='Proportion of income from student fees', 
        ylabel='Proportion of fee income from UK students',
        title='Contribution of student fees to UKHE income in 2021/22'
    )
    plt.legend(loc='lower right', title='Russell Group')
    plt.savefig('./figures/fees_vs_income.png')
    plt.clf()

def capital_projects(tbl, ukprn=10007792):
    print("\tHow of total expenditures is spent on capital projects")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    capital_expend = sb.swarmplot(
        data=tbl,
        x='academic year', y='capital_vs_expend', hue='russell group filter',
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=capital_expend,
        x='academic year', y='capital_vs_expend',
        color='g', label='Exeter', zorder=2, marker='o', markersize=10
    )
    capital_expend.set_ylim(0,0.8)
    capital_expend.set(
        xlabel='Academic Year', 
        ylabel='Proportion of annual Total Expenditure',
        title='What proportion of annual expenditure is on Capital Costs?'
    )
    plt.legend(loc='upper right', title='Russell Group')
    plt.savefig('./figures/capital_expenditure.png')
    plt.clf()

def galt_index(tbl, ukprn=10007792):
    print("\tRatio of VC remuneration to that average remuneration of staff.")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    vc = sb.swarmplot(
        data=tbl,
        x='academic year', y='vc_avg_remunerate', hue='russell group filter',
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=vc,
        x='academic year', y='vc_avg_remunerate',
        color='g', label='Exeter', zorder=2, marker='o', markersize=10
    )
    vc.set_ylim(0,12)
    vc.set(
        xlabel='Academic Year', 
        ylabel='Ratio of VC to staff average',
        title="How does the VC's remuneration compare to the rest of staff?"
    )
    plt.legend(loc='lower right', title='Russell Group')
    plt.savefig('./figures/vc_compensation.png')
    plt.clf()


def compare_staff_salary(tbl, acyear='2021/22', ukprn=10007792):
    print("\tComparing average salaries for academics and ps-staff")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    ax = sb.scatterplot(
        data=tbl[tbl['academic year']==acyear], 
        x='academic_salary', y='ps_staff_salary', hue='russell group filter',
        zorder=1, legend=True
    )
    sb.scatterplot(
        data=uni[ uni['academic year']==acyear ], ax=ax,
        x='academic_salary', y='ps_staff_salary',
        color='g', s=200, label='Exeter', zorder=2
    )
    ax.set_ylim(20,80)
    ax.set_xlim(20,80)
    ax.set(
        xlabel='Average Salary (k£) for Academic Staff', 
        ylabel='Average Salary (k£) for Professional Services',
        title='Comparing Salaries between Academic and PS Staff for '+acyear
    )
    plt.plot(
        [20, 80], [20, 80], 
        color='black', linestyle='dashed', linewidth=2, label='Equality'
    )
    plt.legend(loc='upper right', title='Russell Group')
    plt.savefig('./figures/compare_salaries.png')
    plt.clf()

def net_liquidity_days(tbl, ukprn=10007792):
    print("\tNet Liquidity Days")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    surplus_income = sb.swarmplot(
        data=tbl,
        x='academic year', y='net_liquidity_days', hue='russell group filter',
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=surplus_income,
        x='academic year', y='net_liquidity_days',
        color='g', label='Exeter', zorder=2, marker='o', markersize=10
    )
    surplus_income.axhline(60, label='Lower Bound', color='black', linestyle='dashed')
    surplus_income.set_ylim(-10,600)
    surplus_income.set(
        xlabel='Academic Year', 
        ylabel='Days of Operating Cost Coverage',
        title='A measure of institutions abilitity to costs from liquid assets'
    )
    plt.legend(loc='upper left', title='Russell Group')
    plt.savefig('./figures/net_liquidity_days.png')
    plt.clf()

def operating_cash_flow(tbl, ukprn=10007792):
    print("\tNet cash flow")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    surplus_income = sb.swarmplot(
        data=tbl,
        x='academic year', y='ops_cash_vs_income', hue='russell group filter',
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=surplus_income,
        x='academic year', y='ops_cash_vs_income',
        color='g', label='Exeter', zorder=2, marker='o', markersize=10
    )
    surplus_income.set_ylim(-0.2,0.4)
    surplus_income.set(
        xlabel='Academic Year', 
        ylabel='Proportion of Total Income',
        title='What is the net cash flow from Operating Actives relative to income?'
    )
    plt.legend(loc='upper left', title='Russell Group')
    plt.savefig('./figures/opscash_vs_income.png')
    plt.clf()

def eoy_cash_equivalents(tbl, ukprn=10007792):
    print("\tEnd of year cash equivalents")

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    ax = sb.swarmplot(
        data=tbl,
        x='academic year', y='ops_cash_vs_income', hue='russell group filter',
        dodge=True, zorder=1, warn_thresh=0.2
    )
    sb.lineplot(
        data=uni, ax=ax,
        x='academic year', y='ops_cash_vs_income',
        color='g', label='Exeter', zorder=2, marker='o', markersize=10
    )
    ax.set(
        xlabel='Academic Year', 
        ylabel='Proportion of Total Income',
        title='What is the net cash flow from Operating Actives relative to income?'
    )
    plt.legend(loc='upper left', title='Russell Group')
    plt.savefig('./figures/opscash_vs_income.png')
    plt.clf()

def comparing_surplus_measures(tbl, acyear='2021/22', ukprn=10007792):
    print("\tAnnual surplus measures for "+acyear)

    # Get details for single uni
    uni = tbl[tbl['ukprn']==ukprn]
    ax = sb.scatterplot(
        data=tbl[tbl['academic year']==acyear], 
        x='ops_cash_vs_income', y='surplus_vs_income', hue='russell group filter',
        zorder=1, legend=True
    )
    sb.scatterplot(
        data=uni[ uni['academic year']==acyear ], ax=ax,
        x='ops_cash_vs_income', y='surplus_vs_income',
        color='g', s=200, label='Exeter', zorder=2
    )
    ax.set_ylim(-0.2,0.25)
    ax.set(
        xlabel='Net cash flow from operating activities', 
        ylabel='Total annual surplus',
        title='Financial surplus measures relative to total income in '+acyear,
    )
    plt.legend(loc='upper left', title='Russell Group')
    plt.savefig('./figures/compare_surplus.png')
    plt.clf()


def main():
    # Figure settings
    sb.set_theme(
        context="talk",
        style="whitegrid",
        rc={"figure.figsize":(16, 9), "figure.dpi":300, "savefig.dpi":300}
    )

    # Key Financial Indicators CSV file
    csv_file = 'kfi.csv'
    tbl = pd.read_csv(csv_file)
    # Also pulling out just the data for the University of Exeter
    uoe = 10007792

    print('Swarm Plots')
    net_liquidity_days(tbl)
    operating_cash_flow(tbl)
    eoy_cash_equivalents(tbl)
    galt_index(tbl)
    capital_projects(tbl)
    staffcosts_income(tbl)
    staffcosts_expenditure(tbl)
    average_salary(tbl)

    print('Scatter Plots')
    compare_staff_salary(tbl)
    comparing_surplus_measures(tbl)
    tuition_fee_proportion(tbl)

    print('Line Plots') 
    change_tuition_fees(tbl)

if __name__ == "__main__":
    main()



