#!/usr/bin/python3

import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import pdb

# Figure settings
sb.set_theme()
sb.set_context("talk")
sb.set(rc={"figure.figsize":(16, 9)})

# Key Financial Indicators CSV file
csv_file = 'kfi.csv'
tbl = pd.read_csv(csv_file)
# Also pulling out just the data for the University of Exeter
uoe = 10007792
exeter = tbl[tbl['ukprn']==uoe]

# Annual average salary for staff in k£
avg_salary = sb.boxenplot(
    data=tbl,
    x='academic year', y='avg_salary', hue='russell group filter',
    k_depth="trustworthy", scale='exponential', saturation=1
)
sb.scatterplot(
    data=exeter, ax=avg_salary,
    x='academic year', y='avg_salary',
    color='g', s=200, label='Exeter'
)
avg_salary.set_ylim(25,60)
avg_salary.set(
    xlabel='Academic Year', 
    ylabel='Annual Salary (k£)',
    title='Average UKHE staff salary per year'
)
plt.legend(loc='lower right', title='Russell Group')
plt.savefig('avg_salary.png', dpi=600)
plt.clf()

# Proportion of Income spent on Staff Costs
staff_income = sb.boxenplot(
    data=tbl,
    x='academic year', y='staff_vs_income', hue='russell group filter',
    k_depth="trustworthy", scale='exponential', saturation=1
)
sb.scatterplot(
    data=exeter, ax=staff_income,
    x='academic year', y='staff_vs_income',
    color='g', s=200, label='Exeter'
)
staff_income.set_ylim(0.1,0.8)
staff_income.set(
    xlabel='Academic Year', 
    ylabel='Proportion of Total Income',
    title='What proportion of income is spent on staff costs'
)
plt.legend(loc='lower right', title='Russell Group')
plt.savefig('staff_vs_income.png', dpi=600)
plt.clf()

# Proportion of Total Expenditure that is Staff Costs
staff_expend = sb.boxenplot(
    data=tbl,
    x='academic year', y='staff_vs_expend', hue='russell group filter',
    k_depth="trustworthy", scale='exponential', saturation=1
)
sb.scatterplot(
    data=exeter, ax=staff_expend,
    x='academic year', y='staff_vs_expend',
    color='g', s=200, label='Exeter'
)
staff_expend.set_ylim(0.1,0.8)
staff_expend.set(
    xlabel='Academic Year', 
    ylabel='Proportion of Total Expenditure',
    title='What proportion of annual expenditure is staff costs'
)
plt.legend(loc='lower right', title='Russell Group')
plt.savefig('staff_vs_expend.png', dpi=600)
plt.clf()

# Proportion of Income spent on Staff Costs
surplus_income = sb.boxenplot(
    data=tbl,
    x='academic year', y='surplus_vs_income', hue='russell group filter',
    k_depth="trustworthy", scale='exponential', saturation=1
)
sb.scatterplot(
    data=exeter, ax=surplus_income,
    x='academic year', y='surplus_vs_income',
    color='g', s=200, label='Exeter'
)
surplus_income.set_ylim(-0.3,0.3)
surplus_income.set(
    xlabel='Academic Year', 
    ylabel='Proportion of Total Income',
    title='How big is the annual surplus relative to total income?'
)
plt.legend(loc='lower right', title='Russell Group')
plt.savefig('surplus_vs_income.png', dpi=600)
plt.clf()

# Gauging change in tuition fee income over time
tuition_fees = sb.lineplot(
    data=tbl,
    x='academic year', y='tuition_fees', hue='russell group filter',
    alpha=0.6, estimator=None, units='ukprn', lw=2
)
sb.scatterplot(
    data=exeter, ax=tuition_fees,
    x='academic year', y='tuition_fees',
    color='g', s=200, label='Exeter'
)
tuition_fees.set_ylim(1e3,1e6)
tuition_fees.set(
    xlabel='Academic Year', 
    ylabel='Income from Tuition Fees (k£)',
    title='How has UKHE income from tuition fees changed over time?',
    yscale='log'
)
plt.legend(loc='lower right', title='Russell Group')
plt.savefig('total_tuition_fees.png', dpi=600)
plt.clf()


