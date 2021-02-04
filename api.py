from math import pi
import pandas as pd
import numpy as np
from bokeh.io import output_file, show
from bokeh.palettes import inferno
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.layouts import layout
from github import Github

with open("token.txt","r") as text:
	token=text.readline()
g = Github(token)
username = "steipete"
user = g.get_user(username)
stars = []
forks = []
tempnames = []
totalCommits = []
issues =[]
for repo in user.get_repos():
	stars.append(repo.stargazers_count)
	forks.append(repo.forks)
	tempnames.append(repo.full_name)
	totalCommits.append(repo.get_commits().totalCount)
	issues.append(repo.get_issues().totalCount)
names = [str(i).replace( username + '/', '') for i in tempnames]
output_file("test.html")
x = dict(zip(names,totalCommits))

data = pd.Series(x).reset_index(name='Commits').rename(columns={'index':'Repository'})
data['angle'] = data['Commits']/data['Commits'].sum() * 2*pi
data['color'] = inferno(len(x))

p1 = figure(plot_height=350, title="Repository Commits: " + username, toolbar_location=None,
               tools="hover", tooltips="@Repository: @Commits", x_range=(-0.5, 1.0))

p1.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='Repository', source=data)

p1.axis.axis_label=None
p1.axis.visible=False
p1.grid.grid_line_color = None
p1.legend.visible = False

p2 = figure(x_range=names, plot_height=350, title="Stargazers: " + username)
p2.vbar(x=names, top=stars, width=0.9)

p2.xgrid.grid_line_color = None
p2.y_range.start = 0

p3 = figure(plot_width=600, plot_height=350, title="Stars vs Forks: " + username)
p3.circle(stars, forks, size=10, color="yellow", alpha=0.5)

p4 = figure(plot_width=600, plot_height=350, title="Issues vs Commits: " + username)
p4.square(issues, totalCommits, size=10, color="red", alpha=0.5)



show(layout([
	[[p1],[p2]],
	[[p3],[p4]]
]))