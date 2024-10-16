import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))

from datetime import datetime
from enum import Enum

class RangeType(Enum):
    eDay = 0,
    eWeek = 1,
    eMonth = 2,
    eYear = 3

def plot_stats_range(
    actions,
    baseline,
    from_timestamp,
    to_timestamp,
    range_type,
    path,
    prefix,
    y_asis_text,
    x_asis_text,
    title_text):
    ranges = {'day': RangeType.eDay, 'week': RangeType.eWeek, 'month': RangeType.eMonth, 'year': RangeType.eYear}
    range_type = ranges[range_type]

    df = pd.DataFrame(actions)
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M %d.%m.%Y')
    df.sort_values('Time', inplace=True)

    df['Cumulative'] = baseline + df['Change'].cumsum()

    total_following_actions = df[df['Change'] > 0]['Change'].sum()
    total_unfollowing_actions = df[df['Change'] < 0]['Change'].sum()

    y_min = baseline + total_unfollowing_actions
    y_max = baseline + total_following_actions

    start_time = datetime.strptime(from_timestamp, '%H:%M %d.%m.%Y')
    end_time = datetime.strptime(to_timestamp, '%H:%M %d.%m.%Y')

    freq_values = {'eDay': '2h', 'eWeek': '4h', 'eMonth': '8h', 'eYear': '1d'}
    freq_value = freq_values[range_type.name]

    full_range = pd.date_range(start=start_time, end=end_time, freq=freq_value)

    full_day_df = pd.DataFrame(full_range, columns=['Time'])
    df_full = pd.merge(full_day_df, df, on='Time', how='left')
    df_full['Cumulative'].fillna(method='ffill', inplace=True)
    df_full['Cumulative'].fillna(baseline, inplace=True)

    height_values = {'eDay': 8, 'eWeek': 16, 'eMonth': 32, 'eYear': 64}
    width_values = {'eDay': 10, 'eWeek': 20, 'eMonth': 40, 'eYear': 120}
    plt.figure(figsize=(width_values[range_type.name], height_values[range_type.name]), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')

    for index, row in df.iterrows():
      color = 'green' if row['Change'] > 0 else 'red'
      plt.scatter(row['Time'], row['Cumulative'], color=color, label=f"{row['Username']}")

    offset_idx = 0
    offsets = []
    offsets_by_y = {}

    if(RangeType.eWeek is range_type):
      offsets = [(0, 20), (0, 30)]
    elif(RangeType.eMonth is range_type):
      offsets = [(0, 20), (0, 30), (0, 40)]
    elif(RangeType.eYear is range_type):
      offsets = [(0, 20), (0, 30), (0, 40), (0, 50), (0, 60)]
    else:
      offsets = [(0, 20), (0, 30)]

    for idx, row in df.iterrows():
      y_pos = row['Cumulative']

      if None is offsets_by_y.get(y_pos):
        offsets_by_y[y_pos] = 1
        offset_idx = 0
      else:
        offset_idx = offsets_by_y[y_pos]
        offsets_by_y[y_pos] = offset_idx + 1

        if offsets_by_y[y_pos] is len(offsets):
          offsets_by_y[y_pos] = 0

      plt.annotate(f"{row['Username']}", (row['Time'], row['Cumulative']),
        textcoords="offset points", xytext=offsets[offset_idx], ha='center', va='baseline', color='white',
        arrowprops=dict(arrowstyle="wedge", color='white', lw=0.25, alpha=0.5))

      offset_idx = offset_idx + 1

    if len(df) == 1:
        single_time = df['Time'].iloc[0]
        min_time = single_time - pd.Timedelta(hours=1)
        max_time = single_time + pd.Timedelta(hours=1)
        plt.xlim(min_time, max_time)

        single_cumulative = df['Cumulative'].iloc[0]
        min_cumulative = single_cumulative - 1
        max_cumulative = single_cumulative + 1
        plt.ylim(min_cumulative, max_cumulative)
    else:
        plt.xlim(df['Time'].min(), df['Time'].max())
        plt.ylim(df['Cumulative'].min(), df['Cumulative'].max())

    plt.title(title_text, color='white')
    plt.xlabel(x_asis_text, color='white')
    plt.ylabel(y_asis_text, color='white')
    plt.grid(True, color='gray')

    last_displayed_date = None
    custom_xticks = []
    custom_xtick_labels = []
    for time in full_range:

      if last_displayed_date != time.date():
        custom_xtick_labels.append(time.strftime('%H:%M %d.%m.%y'))
        last_displayed_date = time.date()
      else:
        custom_xtick_labels.append(time.strftime('%H:%M'))

      custom_xticks.append(time)

    plt.xticks(custom_xticks, custom_xtick_labels, rotation=45, color='white')
    plt.yticks(range(y_min, y_max + 1), color='white')

    save_path = path + '/instagram_followers_{}_{}_to_{}.png'.format(
      prefix,
      from_timestamp.replace(":", "_").replace(".", "_"),
      to_timestamp.replace(":", "_").replace(".", "_"))

    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()

    return save_path


def table_stats_range(data, path, prefix, from_ts, to_ts, title_text, lcolumn_text, rcolumn_text, column_text):
    df = pd.DataFrame(data)
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M %d.%m.%Y')
    df.sort_values('Time', ascending=False, inplace=True)

    followed = df[df['Action'] == 'follow'][['Username', 'Time']].assign(
        Followed=lambda x: '@' + x['Username'] + column_text + x['Time'].dt.strftime('%H:%M %d.%m.%Y'))
    unfollowed = df[df['Action'] == 'unfollow'][['Username', 'Time']].assign(
        Unfollowed=lambda x: '@' + x['Username'] + column_text + x['Time'].dt.strftime('%H:%M %d.%m.%Y'))

    table_data = pd.DataFrame({
        'Followed': followed['Followed'].reset_index(drop=True),
        'Unfollowed': unfollowed['Unfollowed'].reset_index(drop=True)
    }).fillna('').to_numpy().tolist()
    table_data.insert(0, [lcolumn_text, rcolumn_text])

    save_path : str = path + '/' + f'{prefix}_action_report_from_{from_ts}_to_{to_ts}.pdf'
    save_path = save_path.replace(' ', '_')
    doc = SimpleDocTemplate(save_path, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontName = 'DejaVuSans'
    title_style.fontSize = 14
    title_style.textColor = colors.white
    title = Paragraph(title_text, title_style)
    spacer = Spacer(1, 12)

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('GRID', (0, 0), (-1, -1), 1, colors.darkgrey),
    ]))

    def on_each_page(canvas, doc):
        canvas.setFillColor(colors.black)
        canvas.rect(0, 0, letter[0], letter[1], stroke=0, fill=1)

    elements.append(title)
    elements.append(spacer)
    elements.append(table)

    doc.build(elements, onFirstPage=on_each_page, onLaterPages=on_each_page)
    return save_path

if __name__ == "__main__":
  import random
  import config
  from datetime import datetime, timedelta

  def generate_actions(start_date, end_date, usernames):
      actions = []
      last_actions = {username: 'unfollow' for username in usernames}
      current_time = start_date

      while current_time <= end_date:
          username = random.choice(usernames)
          # Toggle actions based on the last action recorded for the user
          if last_actions[username] == 'follow':
              action = 'unfollow'
              change = -1
          else:
              action = 'follow'
              change = 1

          actions.append({
              'Time': current_time.strftime('%H:%M %d.%m.%Y'),
              'Action': action,
              'Change': change,
              'Username': username
          })

          # Update the last action
          last_actions[username] = action

          # Random delay for the next action, ranging from 4 hours to 48 hours (2 days)
          hours_delay = random.randint(4, 48)
          current_time += timedelta(hours=hours_delay)

      return actions

  start_date = datetime.strptime('23:00 15.04.2024', '%H:%M %d.%m.%Y')
  end_date = datetime.strptime('23:00 22.04.2024', '%H:%M %d.%m.%Y')

  usernames = ['@grterer', '@audemarspiguet', '@httttt.in']

  unique_numbers = [22]

  while len(unique_numbers) < 20:
    number = unique_numbers[0]
    while number in unique_numbers:
       number = random.randint(0, 200)
    unique_numbers.append(number)

  for num in unique_numbers:
    usernames.append(f'@sample_user_{num}')

  actions = generate_actions(start_date, end_date, usernames)

  for action in actions:
    print(f"{action}\n")

  baseline = 63
  from_timestamp = '23:00 15.04.2024'
  to_timestamp = '23:00 22.04.2024'
  #plot_stats_range(actions, baseline, from_timestamp, to_timestamp, 'week', config.LOCAL_STORAGE_PATH, '123', '111', '222', '333')

  # Create a DataFrame
  df = pd.DataFrame(actions)
  table_stats_range(
    df,
    config.LOCAL_STORAGE_PATH,
    123,
    from_timestamp,
    to_timestamp,
    f'Following activity report [from: {from_timestamp}, to: {to_timestamp}]',
    'Target k137sd has followed',
    'Target k137sd has unfollowed',
    ' at ')
