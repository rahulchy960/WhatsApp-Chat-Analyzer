from urlextract import URLExtract
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import emoji

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # fetch the number of msgs
    num_msgs = df.shape[0]

    # fetch total number of words
    words = []
    for msg in df['Message']:
        words.extend(msg.split())

    # fetch total number of media
    media_msg = df[df['Message'] == "<Media omitted>"].shape[0]

    # fetch total number of links
    extractor = URLExtract()
    links = []
    for link in df['Message']:
        links.extend(extractor.find_urls(link))

    return num_msgs, len(words), media_msg, len(links)

def user_engage(df):
    x = df['User'].value_counts().head(7)
    df = (round((df['User'].value_counts() / df.shape[0]) * 100, 2)).reset_index().rename(columns={'count': 'Percentage'})
    return x, df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    temp = df[df["User"] != 'group_notification']  # remove group notification
    temp = temp[temp['Message'] != '<Media omitted>']  # remove media omitted msgs
    wc = WordCloud(width=300, height=600, min_font_size=9, background_color='white',)
    df_wc = wc.generate(temp['Message'].str.cat(sep=" "))
    return df_wc

def remove_emoji(text):
    return emoji.replace_emoji(text, replace='')
def most_common_words(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # remove stop words
    temp = df[df["User"] != 'group_notification']  # remove group notification
    temp = temp[temp['Message'] != '<Media omitted>']  # remove media omitted msgs
    temp['Message'] = temp['Message'].apply(remove_emoji) # remove emojis

    f = open('stopWords.txt', 'r', encoding='utf-8')
    stop_words = f.read().split('\n')
    # print(stop_words)
    words = []
    for msg in temp['Message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)

    feq = Counter(words).most_common(20)
    most_common_df = pd.DataFrame(feq)
    return most_common_df

def emoji_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    emojis = []
    for msg in df['Message']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])
    emoji_counts = Counter(emojis)
    most_common_emojis = emoji_counts.most_common(10)
    emoji_df = pd.DataFrame(most_common_emojis, columns=['Emoji', 'Frequency'])
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['Year', 'monthNum', 'Month']).count()['Message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + '-' + str(timeline['Year'][i]))
    timeline['Time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    dailytimeline = df.groupby('Date').count()['Message'].reset_index()
    return dailytimeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['DayName'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['Month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    activity_table = df.pivot_table(index='DayName', columns='Period', values='Message', aggfunc='count').fillna(0)

    return activity_table
