import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid, Range1d, Div
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.io import curdoc
from bokeh.layouts import layout, column, row, widgetbox

axis_map = {'HP':'hp','Attack':'attack','Defense':'defense','Sp. Attack':'sp_attack',
    'Sp. Defense':'sp_defense', 'Speed':'speed', 'Height [m]':'height_m', 
    'Weight [kg]':'weight_kgs'}

classes = ['Any','Bug','Dark','Dragon','Electric','Fairy','Fighting',
    'Fire','Flying','Ghost','Grass','Ground','Ice','Normal','Poison',
    'Psychic','Rock','Steel','Water']

line_color = {'Normal':'#6D6D4E', 'Fire':'#F5AC78', 'Fighting':'#7D1F1A', 
	'Water':'#445E9C', 'Flying':'#6D5E9C', 'Grass':'#4E8234', 'Poison':'#682A68', 
	'Electric':'#A1871F', 'Ground':'#927D44', 'Psychic':'#A13959', 'Rock':'#786824',
	'Ice':'#638D8D', 'Bug':'#6D7815', 'Dragon':'#4924A1', 'Ghost':'#493963', 
	'Dark':'#49392F', 'Steel':'#787887', 'Fairy':'#9B6470'}

fill_color = {'Normal':'#A8A878', 'Fire':'#F08030', 'Fighting':'#C03028', 
	'Water':'#6890F0', 'Flying':'#A890F0', 'Grass':'#78C850', 'Poison':'#A040A0', 
	'Electric':'#F8D030', 'Ground':'#E0C068', 'Psychic':'#F85888', 'Rock':'#B8A038',
	'Ice':'#98D8D8', 'Bug':'#A8B820', 'Dragon':'#7038F8', 'Ghost':'#705898', 
	'Dark':'#705848', 'Steel':'#B8B8D0', 'Fairy':'#EE99AC'}

def load_data(file):
    df = pd.read_csv(file)
    df['type2'] = df['type2'].fillna('None')
    df['color'] = '#2468B1'
    df['alpha'] = 0.5
    df['legend'] = 'Standard'
    df.loc[df['is_legendary'], 'color'] = '#FCCF00'
    df.loc[df['is_legendary'], 'alpha'] = 0.8
    df.loc[df['is_legendary'], 'legend'] = 'Legendary'
    df.loc[df['is_mythical'], 'color'] = '#FF0000'
    df.loc[df['is_mythical'], 'alpha'] = 0.8
    df.loc[df['is_mythical'], 'legend'] = 'Mythical'
    df['line_color'] = df['type1'].apply(lambda x: line_color[x])
    df['fill_color'] = df['type1'].apply(lambda x: fill_color[x])
    return df

def select_pokemon():

    generation = generation_select.value 
    type1 = type1_select.value
    type2 = type2_select.value
    hp = hp_slider.value
    attack = attack_slider.value
    defense = defense_slider.value
    sp_attack = sp_attack_slider.value
    sp_defense = sp_defense_slider.value
    speed = speed_slider.value
    pokemon = pokemon_text.value.strip().lower()

    selected = df[
        (df.hp >= hp) &
        (df.attack >= attack) &
        (df.defense >= defense) &
        (df.sp_attack >= sp_attack) &
        (df.sp_defense >= sp_defense) &
        (df.speed >= speed)]

    if type1 != 'Any':
        selected = selected[selected.type1 == type1]
    if type2 != 'Any':
        selected = selected[selected.type2 == type2]
    if generation != 'All':
        selected = selected[selected.generation == int(generation)]
    if (pokemon != ''):
        selected = selected[selected.name.str.lower().str.contains(pokemon)==True]

    return selected

def update_plot():

    df = select_pokemon()
    #print(df.info())

    x_name = axis_map[x_axis_select.value]
    y_name = axis_map[y_axis_select.value]
    plot.xaxis.axis_label = x_axis_select.value
    plot.yaxis.axis_label = y_axis_select.value
    plot.title.text = "%d Unique Pokémon Selected" % len(set(df['pokedex_number']))

    plot.x_range.start=4
    plot.x_range.end=270
    if (x_name == 'weight_kgs'):
        plot.x_range.start=0.08
        plot.x_range.end=1000
    if (x_name == 'height_m'):
        plot.x_range.start=0.08
        plot.x_range.end=15

    plot.y_range.start=4
    plot.y_range.end=270
    if (y_name == 'weight_kgs'):
        plot.y_range.start=0.08
        plot.y_range.end=1000
    if (y_name == 'height_m'):
        plot.y_range.start=0.08
        plot.y_range.end=15
    
    source.data = dict(x=df[x_name], 
        y=df[y_name],
        icon=df['icon'],
        name=df['name'],
        pokedex_number=df['pokedex_number'],
		color=df['color'],
		alpha=df['alpha'],
		legend=df['legend'],
		hp=df['hp'],
		attack=df['attack'],
		defense=df['defense'],
		sp_attack=df['sp_attack'],
		sp_defense=df['sp_defense'],
		speed=df['speed'])

df = load_data('pokemon.csv')

source = ColumnDataSource(data=dict(x=[], 
	y=[], 
	icon=[], 
	name=[], 
	pokedex_number=[], 
	color=[], 
	line_color=[], 
	alpha=[], 
	legend=[],
	hp=[],
	attack=[],
	defense=[],
	sp_attack=[],
	sp_defense=[],
	speed=[]))

TOOLTIPS = """
    <div>
        <div>
            <img src="@icon" height="40" alt="@icon" width="40" style="float: none; align=top; margin: 0px 0px 0px 0px;" border="2"></img> <br>
            <span style="font-size: 10px; font-weight: bold;">@name</span>
            <span style="font-size: 10px; color: #966;">@pokedex_number</span> <br>
            <span style="font-size: 10px; background-color: #FF5959">@hp</span>
            <span style="font-size: 10px; background-color: #F5AC78">@attack</span>
            <span style="font-size: 10px; background-color: #FAE078">@defense</span>
            <span style="font-size: 10px; background-color: #9DB7F5">@sp_attack</span>
            <span style="font-size: 10px; background-color: #A7DB8D">@sp_defense</span>
            <span style="font-size: 10px; background-color: #FA92B2">@speed</span>
        </div>
    </div>
"""

plot = figure(title='Pokémon',
    x_axis_label='Weight [kg]',
    y_axis_label='Height [m]',
    title_location='above',
    toolbar_location='right',
	plot_height=666, 
	plot_width=866,
    x_axis_type='linear', 
    y_axis_type='linear',
    y_range=(0.08,15), 
    x_range=(0.08,1000),
    tooltips=TOOLTIPS)
	#sizing_mode='scale_both',

plot.circle(x='x', 
	y='y', 
	source=source, 
	color='color', 
	line_color=None, 
	size=10, 
	alpha='alpha', 
	legend='legend', 
	hover_color='red')
plot.grid.grid_line_alpha = 0.5
plot.legend.location = "top_right"

generation_select = Select(title='Generation', value='All', 
    options=['All', '1', '2', '3', '4', '5', '6', '7'])

type1_select = Select(title='Primary Type', value='Any', 
    options=classes)

type2_select = Select(title='Secondary Type', value='Any', 
    options=['None']+classes)

x_axis_select = Select(title="X-Axis", value='Attack',
    options=sorted(axis_map.keys()))

y_axis_select = Select(title="Y-Axis", value='Defense', 
    options=sorted(axis_map.keys()))

hp_slider = Slider(title='Minimum HP', 
    start=0, end=255, value=0, step=5)

attack_slider = Slider(title="Minimum Attack", 
    start=0, end=255, value=0, step=5)

defense_slider = Slider(title="Minimum Defense", 
    start=0, end=255, value=0, step=5)

sp_attack_slider = Slider(title="Minimum Sp. Attack", 
    start=0, end=255, value=0, step=5)

sp_defense_slider = Slider(title="Minimum Sp. Defense", 
    start=0, end=255, value=0, step=5)

speed_slider = Slider(title='Minimum Speed', 
    start=0, end=255, value=0, step=5)

pokemon_text = TextInput(title='Pokémon Name Contains (e.g. \'saur\')', value='')

controls = [generation_select, type1_select, type2_select, 
    x_axis_select, y_axis_select, pokemon_text, hp_slider, attack_slider, 
    defense_slider, sp_attack_slider, sp_defense_slider, speed_slider]

for control in controls:
    control.on_change('value', lambda attr, old, new: update_plot())

inputs = column(widgetbox(controls, sizing_mode='scale_height'), width=300)

desc = Div(text="""
	<h1>Pokémon Data Explorer</h1>
	<p>Looking to build a team? Use the widgets on the left to select a subset of Pokémon to plot. Hover 
	over the circles to see more information about each Pokémon. </p>
	<p>Data is taken from the following 
	<a href="https://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_base_stats_(Generation_VII-present)">
	Bulbapedia</a> page and consists of all Pokémon through the 7th generation (including Alolan forms and 
	Mega Evolutions), along with their main stats. </p>
	<p>Battle statistics are highlighted using the following color scheme: 
	<span style="font-size: 10px; background-color: #FF5959">HP</span>
    <span style="font-size: 10px; background-color: #F5AC78">Attack</span>
    <span style="font-size: 10px; background-color: #FAE078">Defense</span>
    <span style="font-size: 10px; background-color: #9DB7F5">Sp. Attack</span>
    <span style="font-size: 10px; background-color: #A7DB8D">Sp. Defense</span>
    <span style="font-size: 10px; background-color: #FA92B2">Speed</span>.</p>
	""", width=1166, height=125)

l = layout([
	[desc], 
	[inputs, plot],
], sizing_mode="fixed")

update_plot() # initial load of the data

curdoc().add_root(l)
curdoc().title = "Pokemon!"
