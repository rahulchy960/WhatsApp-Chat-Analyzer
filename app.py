import streamlit as st
from matplotlib import pyplot as plt
import seaborn as sns
import preprocessor
import utility


st.sidebar.title("Analyzer")
st.sidebar.markdown('**How to export chat text file?**')
st.sidebar.text('Follow the steps :')
st.sidebar.text('1) Open the individual or group chat.')
st.sidebar.text('2) Tap options > More > Export chat.')
st.sidebar.text('3) Choose export without media.')

st.sidebar.markdown('*You are all set to go*.')

st.title("WhatsApp Chat Analyzer")
st.markdown("This app is use to analyze your WhatsApp Chat using the exported text file.")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # st.text(data)                         # print the file
    df = preprocessor.preprocess(data)      # calling our preprocess function from preprocessor
    # st.dataframe(df)                        # print the dataframe

    # fetch unique user
    userList = df['User'].unique().tolist()
    # userList.remove('group_notification')
    userList.sort()
    userList.insert(0, 'Overall')
    selectedUser = st.sidebar.selectbox('Show Analysis wrt', userList)

    # Adding the Analysis button
    if st.sidebar.button('Show Analysis'):

        # stats area

        totalMsg, words, media_msg, links = utility.fetch_stats(selectedUser, df)

        st.header("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader('Total Messages')
            st.title(totalMsg)
        with col2:
            st.subheader('Total Words')
            st.title(words)
        with col3:
            st.subheader('Media Shared')
            st.title(media_msg)
        with col4:
            st.subheader('Link Shared')
            st.title(links)

        # Finding the busiest User (group level)

        if selectedUser == 'Overall':
            st.title("Most Engaged Users")
            x, y = utility.user_engage(df)
            fig, ax = plt.subplots(figsize=(8, 6))

            col1, gap, col2 = st.columns([4, 1, 3])

            with col1:
                ax.bar(x.index, x.values, color='green')
                plt.xticks(rotation=90)
                st.pyplot(fig)
            with col2:
                st.dataframe(y, height=280)

        # Most Common Words

        most_common_df = utility.most_common_words(selectedUser, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1], color='blue')
        st.title("Most Common Words")
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Emoji Analysis

        emoji_df = utility.emoji_analysis(selectedUser, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            # st.subheader('Top 5')
            fig, ax = plt.subplots()
            ax.pie(emoji_df['Frequency'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)

        # monthly timeline

        st.title("Monthly Timeline")
        timeline = utility.monthly_timeline(selectedUser, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['Time'], timeline['Message'],color='red')
        plt.xticks(rotation='vertical')
        fig.set_size_inches(18, 10)
        # st.dataframe(timeline)
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = utility.daily_timeline(selectedUser, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['Date'], daily_timeline['Message'], color='black')
        plt.xticks(rotation='vertical')
        fig.set_size_inches(18, 10)
        # st.dataframe(timeline)
        st.pyplot(fig)

        # Activity MAp
        st.title('Activity Map')
        col1, col2 = st.columns([1,1])

        with col1:
            st.subheader("Most Busy Day")
            busy_day = utility.week_activity_map(selectedUser,df)
            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_day.index, busy_day.values, color='orange')
            st.pyplot(fig)

        with col2:
            st.subheader("Most Busy Month")
            busy_month = utility.month_activity_map(selectedUser,df)
            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_month.index, busy_month.values, color='brown')
            st.pyplot(fig)

        # Activity HeatMap (defines when a user active in time period in each days)

        st.title('Weekly Activity Map')
        activity_table = utility.activity_heatmap(selectedUser,df)
        fig, ax = plt.subplots(figsize=(20, 6))
        ax = sns.heatmap(activity_table, annot=False, cmap="magma")
        st.pyplot(fig)

        # WordCould

        st.title("Wordcloud")
        df_wc = utility.create_wordcloud(selectedUser, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis('off')
        st.pyplot(fig)