#!/usr/bin/python3

import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import pdb

# Figure settings
sb.set_theme()
sb.set_context("talk")
sb.set(rc={
    "figure.figsize":(16, 9), "figure.dpi":300, 
    "savefig.dpi":300
})

# Key Financial Indicators CSV file
csv_file = 'kfi.csv'
tbl = pd.read_csv(csv_file)
# Also pulling out just the data for the University of Exeter
uoe = 10007792
exeter = tbl[tbl['ukprn']==uoe]


print("\tAnnual average salary for staff in k£")
avg_salary = sb.swarmplot(
    data=tbl,
    x='academic year', y='avg_salary', hue='russell group filter',
    dodge=True, zorder=1, warn_thresh=0.2
)
sb.lineplot(
    data=exeter, ax=avg_salary,
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


print("\tProportion of Income spent on Staff Costs")
staff_income = sb.swarmplot(
    data=tbl,
    x='academic year', y='staff_vs_income', hue='russell group filter',
    dodge=True, zorder=1, warn_thresh=0.2
)
sb.lineplot(
    data=exeter, ax=staff_income,
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


print("\tWhat proportion of Total Expenditure is Staff Costs")
staff_expend = sb.swarmplot(
    data=tbl,
    x='academic year', y='staff_vs_expend', hue='russell group filter',
    dodge=True, zorder=1, warn_thresh=0.2
)
sb.lineplot(
    data=exeter, ax=staff_expend,
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


print("\tWhat proportion of total income is spent on Staff Costs")
surplus_income = sb.swarmplot(
    data=tbl,
    x='academic year', y='surplus_vs_income', hue='russell group filter',
    dodge=True, zorder=1, warn_thresh=0.2
)
sb.lineplot(
    data=exeter, ax=surplus_income,
    x='academic year', y='surplus_vs_income',
    color='g', label='Exeter', zorder=2, marker='o', markersize=10
)
surplus_income.set_ylim(-0.3,0.3)
surplus_income.set(
    xlabel='Academic Year', 
    ylabel='Proportion of Total Income',
    title='How big is the annual surplus relative to total income?'
)
plt.legend(loc='lower right', title='Russell Group')
plt.savefig('./figures/surplus_vs_income.png')
plt.clf()


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
    data=pct.loc[uoe], ax=tuition_fees,
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


print("\tUnderstand what portion of income comes from Student Fees")
fee_income = sb.lineplot(
    data=tbl, 
    x='total_fees_vs_income', y='uk_vs_total_fees', hue='russell group filter',
    zorder=1, legend=True, marker='o', units='ukprn', estimator=None
)
sb.scatterplot(
    data=exeter, ax=fee_income,
    x='total_fees_vs_income', y='uk_vs_total_fees',
    color='g', s=200, label='Exeter', zorder=2
)
fee_income.set(
    xlabel='Proportion of income from student fees', 
    ylabel='Proportion of fee income from UK students',
    title='Contribution of student fees to UKHE income'
)
plt.legend(loc='lower right', title='Russell Group')
plt.savefig('./figures/fees_vs_income.png')
plt.clf()


print("\tHow of total expenditures is spent on capital projects")
capital_expend = sb.swarmplot(
    data=tbl,
    x='academic year', y='capital_vs_expend', hue='russell group filter',
    dodge=True, zorder=1, warn_thresh=0.2
)
sb.lineplot(
    data=exeter, ax=capital_expend,
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


print("\tRatio of VC remuneration to that average remuneration of staff.")
vc = sb.swarmplot(
    data=tbl,
    x='academic year', y='vc_avg_remunerate', hue='russell group filter',
    dodge=True, zorder=1, warn_thresh=0.2
)
sb.lineplot(
    data=exeter, ax=vc,
    x='academic year', y='vc_avg_remunerate',
    color='g', label='Exeter', zorder=2, marker='o', markersize=10
)
vc.set_ylim(0,12)
vc.set(
    xlabel='Academic Year', 
    ylabel='Ratio of VC to avg-staff member total compentation',
    title="How does the VC's remuneration compare to the rest of staff?"
)
plt.legend(loc='lower right', title='Russell Group')
plt.savefig('./figures/vc_compensation.png')
plt.clf()


print("\tComparing average salaries for academics and ps-staff")
staff_salary = sb.lineplot(
    data=tbl[(tbl['academic_salary']!=0) & (tbl['ps_staff_salary']!=0)], 
    x='academic_salary', y='ps_staff_salary', hue='russell group filter',
    zorder=1, legend=True, marker='o', units='ukprn', estimator=None
)
sb.scatterplot(
    data=exeter[(exeter['academic_salary']!=0) & (exeter['ps_staff_salary']!=0)], ax=staff_salary,
    x='academic_salary', y='ps_staff_salary',
    color='g', s=200, label='Exeter', zorder=2
)
staff_salary.set_ylim(20,80)
staff_salary.set_xlim(20,80)
staff_salary.set(
    xlabel='Average Salary (k£) for Academic Staff', 
    ylabel='Average Salary (k£) for Professional Services',
    title='Comparing Salaries between sub-sectors in UKHE'
)
plt.plot(
    [20, 80], [20, 80], 
    color='black', linestyle='dashed', linewidth=2, label='Equality'
)
plt.legend(loc='upper right', title='Russell Group')
plt.savefig('./figures/compare_salaries.png')
plt.clf()
