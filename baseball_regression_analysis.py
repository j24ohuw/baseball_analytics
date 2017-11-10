import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm
from matplotlib.ticker import FuncFormatter



def millions(x, pos):
    'The two args are the value and tick position'
    return '$%1.1fM' % (x*1e-6)

formatter = FuncFormatter(millions)

#plot salaries vs wins for the year parameter
def plot_factor_wins(teams, factor_x, factor_y, year):
    #select the year
    teams_year = teams.loc[year]
    #create subplots fig, ax = plt.subplots()
    fig, ax = plt.subplots()
    #loop through all the teams for the given year
    for i in teams_year.index:
    #plot scatter oak, nya, bos, rest. color =
        if i == 'OAK':
            ax.scatter(teams_year[factor_x][i], teams_year[factor_y][i], color="lightblue", s=200)
            ax.annotate(i, (teams_year[factor_x][i], teams_year[factor_y][i]),
                        bbox=dict(boxstyle="round", color="lightblue"),
                        xytext=(-30, 30), textcoords='offset points',
                        arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90,rad=10"))
        elif i == 'NYA':
            ax.scatter(teams_year[factor_x][i], teams_year[factor_y][i], color="green", s=200)
            ax.annotate(i, (teams_year[factor_x][i], teams_year[factor_y][i]),
                        bbox=dict(boxstyle="round", color="green"),
                        xytext=(-30, 30), textcoords='offset points',
                        arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90,rad=10"))
        elif i == 'BOS':
            ax.scatter(teams_year[factor_x][i], teams_year[factor_y][i], color="red", s=200)
            ax.annotate(i, (teams_year[factor_x][i], teams_year[factor_y][i]),
                        bbox=dict(boxstyle="round", color="red"),
                        xytext=(-30, 30), textcoords='offset points',
                        arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90,rad=10"))
        else:
            ax.scatter(teams_year[factor_x][i], teams_year[factor_y][i], color="grey", s=50)
    
    #ax.xaxis.set_major_formatter(formatter) 
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    ax.set_xlabel(factor_x, fontsize=20)
    ax.set_ylabel(factor_y , fontsize=20)
    ax.set_title(factor_x +' - '+ factor_y + ' ' + str(year), fontsize=25, fontweight='bold')
    plt.show()



teams = pd.read_csv(r'C:\Users\John\Desktop\lahman-csv_2014-02-14\Teams.csv')
salaries = pd.read_csv(r'C:\Users\John\Desktop\lahman-csv_2014-02-14\Salaries.csv')

teams = teams[teams['yearID'] >= 1985]
teams = teams[['yearID', 'teamID', 'Rank', 'R', 'RA', 'G', 'W', 'L', 'H', 'BB', 'HBP', 'AB', 'SF', 'HR', '2B', '3B']]
teams = teams.set_index(['yearID', 'teamID'])

salaries_by_yearID_teamID = salaries.groupby(['yearID', 'teamID'])['salary'].sum()
#salaries_by_yearID_teamID.describe()

teams = teams.join(salaries_by_yearID_teamID)

#plt.scatter(teams['salary'][2001],teams['W'][2001])
#plt.show()
teams['BA'] = teams['H']/teams['AB']
teams['OBP'] = (teams['H'] + teams['BB'] + teams['HBP']) / (teams['AB'] + teams['BB'] + teams['HBP'] + teams['SF'])
teams['SLG'] = (teams['H'] + teams['2B'] + (2*teams['3B']) + (3*teams['HR'])) / teams['AB']
teams['WL'] = teams['W']/teams['L']
teams['win_ratio'] = teams['W']/(teams['W'] + teams['L'])

regression_model1 = sm.ols("R~BA+OBP+SLG", teams).fit()
regression_model2 = sm.ols("R~OBP+SLG", teams).fit()
regression_model3 = sm.ols("R~BA", teams).fit()
regression_model4 = sm.ols("win_ratio~R", teams).fit()
regression_model5 = sm.ols("win_ratio~OBP+SLG", teams).fit()

print(regression_model1.summary())
print(regression_model2.summary())
print(regression_model3.summary())
print(regression_model4.summary())
print(regression_model5.summary())
plot_factor_wins(teams, 'R', 'win_ratio', 2004)
