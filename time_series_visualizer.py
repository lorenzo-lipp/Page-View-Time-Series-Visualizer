import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('./fcc-forum-pageviews.csv',
                 index_col='date',
                 parse_dates=True)

# Clean data
df = df[(df['value'] > df['value'].quantile(0.025))
        & (df['value'] < df['value'].quantile(0.975))]

def draw_line_plot():
  # Draw line plot
  fig = plt.figure(figsize=(20, 8))
  plt.plot(df.index, df['value'], color="red")
  plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
  plt.xlabel("Date")
  plt.ylabel("Page Views")
  
  # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['month'] = df_bar.index.month
    df_bar['year'] = df_bar.index.year
    df_bar = df_bar.groupby(['month', 'year'])['value'].mean().reset_index()
    
    normalize = pd.DataFrame({
      "month": [1, 2, 3, 4],
      "year": [2016, 2016, 2016, 2016],
      'value': [0, 0, 0, 0]})
    df_bar = pd.concat([df_bar, normalize]).sort_values(by=['month','year'], ignore_index=True)

    # Draw bar plot
    x_1 = np.arange(12) - 2
    x_2 = [x + 12 for x in np.arange(12)]
    x_3 = [x + 26 for x in np.arange(12)]
    x_4 = [x + 40 for x in np.arange(12)]
  
    fig = plt.figure(figsize=(12, 8))
    cmap = matplotlib.colormaps.get_cmap('tab20')
    colors = cmap(np.arange(12))
  
    bar_1 = plt.bar(x_1, df_bar[df_bar['year'] == 2016]['value'], width=1, color=colors)
    plt.bar(x_2, df_bar[df_bar['year'] == 2017]['value'], width=1, color=colors)
    plt.bar(x_3, df_bar[df_bar['year'] == 2018]['value'], width=1, color=colors)
    plt.bar(x_4, df_bar[df_bar['year'] == 2019]['value'], width=1, color=colors)
  
    plt.xticks([5.75, 17.5, 31.5, 45.5], ['2016', '2017', '2018', '2019'])
    plt.title("Average Page Views")
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(iter(bar_1), ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'), title="Months", fontsize=8)
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1,2, figsize=(20, 8))
  
    sns.boxplot(x="year", y="value", data=df_box, ax=ax[0])
    ax[0].set_title("Year-wise Box Plot (Trend)")
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel("Page Views")
    ax[0].set_yticks(np.arange(0, 200001, 20000))
  
    sns.boxplot(x="month", y="value", data=df_box, ax=ax[1], order=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("Page Views")
    ax[1].set_yticks(np.arange(0, 200001, 20000))
  
    plt.subplots_adjust(left=0.06, right=0.98, top=0.9, bottom=0.1)
    fig = fig.figure
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
