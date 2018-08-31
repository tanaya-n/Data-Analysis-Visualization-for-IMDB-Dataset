
# coding: utf-8

# In[ ]:



import pandas as pd
import numpy as np
from bokeh.io import output_file, output_notebook, show, curdoc
from bokeh.plotting import figure
from bokeh.models import Circle
from bokeh.layouts import widgetbox, row, column
from bokeh.models import Title, RangeSlider, CategoricalColorMapper, Select, Button, Label, ColumnDataSource, LassoSelectTool,WheelZoomTool,PanTool, PolySelectTool, SaveTool, ResetTool, HoverTool

from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap
from bokeh.models import ColumnDataSource, HoverTool, CheckboxGroup, CustomJS, Button
from bokeh.palettes import GnBu3, OrRd3, Spectral11

from bokeh.layouts import row, gridplot, widgetbox
from collections import OrderedDict
from bokeh.models.callbacks import CustomJS
from bokeh.events import ButtonClick
from bokeh.models.renderers import GlyphRenderer


from bokeh.models.widgets import Panel, Tabs





TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
df = pd.read_csv('data\IMDB-Movie-Data.csv')
start = min(df.Year)
end = max(df.Year)


#Rank ,Runtime (Minutes),Rating,Votes,Revenue (Millions),Metascore
data = df
data_column=ColumnDataSource(data={
            'x'       : data.Votes/1000,
            'y'       : data.Rank,
            'title' : data.Title,
            'genre':data.Genre,
            'description':data.Description,
            'director':data.Director,
            'actors' : data.Actors,
            'votes' : data.Votes,
            'rank' : data.Rank,
            'year' : data.Year
        })


def update_plot(attr, old, new):
    (start,end) = slider.value
    data = df[(df.Year >= start) & (df.Year <= end)]
    
    x = x_select.value
    y = y_select.value    

    y_val = data[y]
    x_val = data[x]
    
    
    new_data = {
            'x'       : x_val,
            'y'       : y_val,
            'title' : data.Title,
            'genre':data.Genre,
            'description':data.Description,
            'director':data.Director,
            'actors' : data.Actors,
            'votes' : data.Votes,
            'rank' : data.Rank,
            'year' : data.Year
        }

    data_column.data = new_data
    plot.title.text = "Movie Data"
    plot.xaxis.axis_label=x
    plot.yaxis.axis_label=y
    
    plot.x_range.start = min(x_val)
    plot.x_range.end = max(x_val)
    plot.y_range.start = min(y_val)
    plot.y_range.end = max(y_val)


#tooltip options  
tool_tips=[('Title','@title'),('X value','@x'),('Y value','@y'),('Genre','@genre'),('Director','@director'),('Actors','@actors'),('Year','@year')]
#side menu
plot = figure(title='Movies', x_axis_label='Votes', y_axis_label='Rank',
           plot_height=700, plot_width=700,tools = TOOLS)


plot.add_tools(HoverTool(tooltips=tool_tips))


slider = RangeSlider(start=start,end=end,step=1,value=(start,end), title="Year")
slider.on_change('value',update_plot)



renderer = plot.circle(x='x', y='y', source=data_column,size=6,color='blue')

glyph = renderer.glyph
glyph.size = 6
glyph.fill_alpha = 0.5
glyph.line_color = "black"
#glyph.line_dash = [1]
glyph.line_width = 1


selected_circle = Circle(fill_alpha=1, fill_color="firebrick", line_color=None)
nonselected_circle = Circle(fill_alpha=0.2, fill_color="blue", line_color=None)

renderer.selection_glyph = selected_circle
renderer.nonselection_glyph = nonselected_circle

#plot.legend.location = 'top_right'
#Rank,Title,Genre,Description,Director,Actors,Year,Runtime (Minutes),Rating,Votes,Revenue (Millions),Metascore
dropdown_options = ['Rank', 'Rating', 'Votes', 'Revenue (Millions)', 'Metascore','Runtime (Minutes)']

x_select = Select(
    options=dropdown_options,
    value='Votes',
    title='x-axis data'
)

y_select = Select(
    options=dropdown_options,
    value='Rank',
    title='y-axis data'
)


x_select.on_change('value', update_plot)
y_select.on_change('value', update_plot)
scatter_layout = row(widgetbox(slider, x_select, y_select), plot)







####
####






#df = pd.read_csv('data/IMDB-Movie-Data.csv')
# Creating a dataframe for year, genre and revenue
year = []
genre = []
revenue = []
for idx, row in df.iterrows():
    for a in row['Genre'].split(','):
        year.append(row['Year'])
        genre.append(a)
        revenue.append(row['Revenue (Millions)'])
df1 = pd.DataFrame()
df1['year'] = year
df1['genre'] = genre
df1['revenue'] = revenue


# In[83]:

# Grouping the data by Genre and Year - Get the count and avg Revenue for each category
grouped = pd.DataFrame(df1.groupby(['genre', 'year'])['revenue'].agg(['count','mean']).reset_index())
grouped['mean'].fillna(0,inplace=True)
grouped['year'].astype(str)

genre = grouped['genre'].tolist()
year = grouped['year'].tolist()
count = grouped['count'].tolist()
mean = grouped['mean'].tolist()
Years = pd.Series(df1.year.unique())
for g in df1.genre.unique():
    check_year = grouped[grouped['genre'] == g]['year']
    for y in Years.unique():
        if y not in check_year.unique():
            genre.append(g)
            year.append(y)
            count.append(0)
            mean.append(0)
df2 = pd.DataFrame()     
df2['genre'] = genre
df2['year'] = year
df2['count'] = count
df2['mean'] = mean


# In[84]:

#Converting to dictionary - data for hbar
years = ['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016']

counts = {'genre': df2['genre'].unique().tolist(),
          '2006': df2[df2['year'] == 2006].sort_values('genre')['count'],
          '2007': df2[df2['year'] == 2007].sort_values('genre')['count'],
          '2008': df2[df2['year'] == 2008].sort_values('genre')['count'],
          '2009': df2[df2['year'] == 2009].sort_values('genre')['count'],
          '2010': df2[df2['year'] == 2010].sort_values('genre')['count'],
          '2011': df2[df2['year'] == 2011].sort_values('genre')['count'],
          '2012': df2[df2['year'] == 2012].sort_values('genre')['count'],
          '2013': df2[df2['year'] == 2013].sort_values('genre')['count'],
          '2014': df2[df2['year'] == 2014].sort_values('genre')['count'],
          '2015': df2[df2['year'] == 2015].sort_values('genre')['count'],
          '2016': df2[df2['year'] == 2016].sort_values('genre')['count']
         }


# In[85]:

# Create the checkbox
#checkbox = CheckboxGroup(labels=[str(r.name) for i in N_plots],active=list(N_plots),width=200)
checkbox = CheckboxGroup(labels=years,active=[i for i in range(0,11)], width=100)


# Create the plot
p1 = figure(y_range=df2['genre'].unique(), plot_height= 540,  
            x_range=(0, sum(df2[df2['genre']=='Drama']['count'])), 
            title="No of movies by year",toolbar_location="below",tools = TOOLS)
renderers = p1.hbar_stack(years , y='genre',height = 0.8, source=ColumnDataSource(counts), 
                          color=Spectral11, legend = [" %s" %x for x in years],name=years)
p1.xaxis.axis_label = "No of films"
p1.yaxis.axis_label = "Genre"


p2 = figure(y_range=df2['genre'].unique(), plot_height= 540, 
            title="Select ONLY ONE year to display correct avg. revenue"
            ,toolbar_location="below",tools = TOOLS)
l = [p2.hbar(y=df2['genre'].unique(), height=0.5, left=0, right=df2[df2['year']== int(i)]['mean'], 
             color=Spectral11[years.index(i)],name=i) for i in years]
p2.xaxis.axis_label = "Avg revenue"
p2.yaxis.axis_label = "Genre"

#No output for revenue graph for the first time
for i in range(0,11):
    l[i].visible=False

# Interactive legend
p1.legend.click_policy="hide"

# Add hover tool
for r in renderers:
    year = r.name
    hover = HoverTool(tooltips=[
        ("Number of films in %s" % year, "@%s" % year),
        #("index", "$index")
    ], renderers=[r])
    p1.add_tools(hover)
    
for r in l:
    year = r.name
    hover = HoverTool(tooltips=[
        ("%s Avg Revenue" % year, "@%s" % year ),
        ("index", "$index")
    ], renderers=[r])
    p2.add_tools(hover)

# Create renderers
plots = [r for r in renderers]
N_plots = range(len(plots))

# Checkbox callback
iterable = [('p'+str(i),plots[i]) for i in N_plots]+[('l'+str(i),l[i]) for i in N_plots]+[('checkbox',checkbox)]
checkbox_code = ''.join(['p'+str(i)+'.visible = checkbox.active.includes('+str(i)+');'+'l'+str(i)+'.visible = checkbox.active.includes('+str(i)+');' for i in N_plots])
checkbox.callback = CustomJS(args={key: value for key,value in iterable}, code=checkbox_code)

# Create "Clear All" button and its callback
clear_button = Button(label='Clear All')
clear_button_code = "checkbox.active=[];"+checkbox_code
clear_button.callback = CustomJS(args={key: value for key,value in iterable}, code=clear_button_code)

# Create "Select All" button and its callback
check_button = Button(label='Select All')
checkbox_code2 = ''.join(['p'+str(i)+'.visible = checkbox.active.includes('+str(i)+');' for i in N_plots])
checkbox_code3 = ''.join(['l'+str(i)+'.visible = False;' for i in N_plots])
check_button_code = "checkbox.active="+str(list(N_plots))+";"+checkbox_code2+checkbox_code3
check_button.callback = CustomJS(args={key: value for key,value in iterable}, code=check_button_code)


# In[87]:

# Show the plot    
group = widgetbox(checkbox,clear_button,check_button)
p1.add_layout(Title(text="Source - https://www.kaggle.com/nachrism/imdb-eda/data", align="left", text_font_style='italic'), "below")
bars_layout = gridplot([[group,p1,p2]]) 




###
###

#Import the data into a DF.
#df = pd.read_csv('data/IMDB-Movie-Data.csv')
most_active_directors = df['Director'].value_counts().head(10)

#Determine how much revenue each of these top 10 directors' films brought in 
#(as a sum for each director) in millions
director_revenue_totals = np.zeros(len(most_active_directors))
i = 0
for director in most_active_directors.index:
    current_director = df['Director'].str.contains(director).fillna(False)
    director_film_revenue = df[current_director].xs('Revenue (Millions)', axis=1).sum()
    director_revenue_totals[i] = director_film_revenue
    i += 1
director_revenue_totals_df =  pd.DataFrame(np.column_stack([most_active_directors.index, director_revenue_totals]), 
                               columns=['Director', 'Revenue'])

#Load into columndatasource
ds = ColumnDataSource(director_revenue_totals_df)

#tooltip options  
tool_tips=[('Director','@Director'),('Total Revenue','@Revenue (Millions)')]

#Draw the Plot
directors_chart = figure(title='Revenue brought in by top 10 most active Directors in ten years', x_axis_label='Director', y_axis_label='Revenue (Millions)', x_range = director_revenue_totals_df['Director'].unique(),
           plot_height=600, plot_width=1100, active_drag='pan', active_scroll='wheel_zoom')
directors_chart.vbar(x='Director', width=0.5, bottom=0, top='Revenue', color="#CAB2D6", source=ds, 
         alpha=.8, hover_color='orchid')
directors_chart.add_tools(HoverTool(tooltips=tool_tips))



###
###


plots = []
movie_names = ['batmanvsuperman','deadpool', 'civilwar', 'fantasticbeasts', 
'findingdory', 'junglebook', 'rogueone', 'secretlifeofpets', 'suicidesquad', 'zootopia' ]

for movie_name in movie_names:
    movie = pd.read_csv('data/movies/' + movie_name + '.csv')
    genders = ['male','female']
    mapper = CategoricalColorMapper(factors=genders, palette=Spectral6)
    source = ColumnDataSource(data=dict(gender=movie.gender, 
                                         character=movie.character,
                                         total_words=movie.total_words,
                                         speaking_turns=movie.speaking_turns))
    p = figure(title="Gender distribution of dialogue for " + movie_name.capitalize() , 
      x_axis_label='Characters', y_axis_label='Total Words', tools = TOOLS,
      plot_width=1300, plot_height=400, x_range=movie.character.values)
    p.vbar(x='character', width=0.5, bottom=0,source=source, legend="gender",
           top='speaking_turns', color=dict(field='gender', transform=mapper))
    p.add_tools(HoverTool(tooltips=[('Character', '@character'),('Word Count', '@total_words')]))
    p.xaxis.major_label_orientation = 1
    plots.append(p)








###
###


#Top 10 ranked movies Ratings and Metascore
top_ten_movies_data = df.head(10)

x = top_ten_movies_data['Rank']
y0 = top_ten_movies_data['Rating']
y1 = top_ten_movies_data['Metascore']
y2 = top_ten_movies_data['Revenue (Millions)']
title = top_ten_movies_data['Title']
director = top_ten_movies_data['Director']

# create a column data source for the plots to share
source = ColumnDataSource(data=dict(x=x, y0=y0, y1=y1, y2=y2, title=title, director=director))

TOOLS = 'pan,box_select,lasso_select,help,reset'
#tooltip options  
tool_tips=[('Title','@title'), ('Director', '@director'), ('Rank', '@x'), ('Rating', '@y0')]

# create Rating plot
first = figure(tools=TOOLS, plot_width=450, plot_height=450, x_axis_label='Rank', y_axis_label='Rating', title='Rank vs Rating')
first.circle('x','y0',size=10, color='darkred', source = source)
first.add_tools(HoverTool(tooltips=tool_tips))

# create Metascore plot
second = figure(tools=TOOLS, plot_width=450, plot_height=450, x_range=first.x_range, y_range=first.y_range, x_axis_label='Rank', y_axis_label='Metascore', title='Rank vs Metascore')
second.triangle('x','y1', size=10, color='green', source = source)
second.add_tools(HoverTool(tooltips=tool_tips))

# create Revenue plot
third = figure(tools=TOOLS, plot_width=450, plot_height=450, x_range=first.x_range, x_axis_label='Rank', y_axis_label='Revenue', title='Rank vs Revenue(Millions)')
third.square('x','y2',size=10, color='darkmagenta', source = source)
third.add_tools(HoverTool(tooltips=tool_tips))

#Create gridplot to display all the plots.
rank_LinkingBrushingChart = gridplot([[first,second,third]], toolbar_location='right')


tab1 = Panel(child=scatter_layout, title="Scatter Plot")
tab2 = Panel(child=bars_layout, title="Analysis by Year")
tab3 = Panel(child=directors_chart, title="Directors")
tab4 = Panel(child=column(children=plots), title="Dialogue by gender")
tab5 = Panel(child=rank_LinkingBrushingChart , title="Top 10 Ranked Movies")

tabs = Tabs(tabs=[ tab3, tab5, tab1, tab2 , tab4 ])




curdoc().title = 'Final Project'
curdoc().add_root(tabs)

