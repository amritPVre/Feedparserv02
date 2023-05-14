import streamlit as st
import feedparser
import pandas as pd
import csv
import datetime
import os
import google.auth


# Define function to scrape news headlines from RSS feed
def scrape_headlines(url):
    feed = feedparser.parse(url)
    headlines = []
    for entry in feed.entries:
        headline = {}
        headline['Title'] = entry.title
        headline['Published'] = entry.published
        headline['Source'] = feed.feed.title
        headlines.append(headline)
    if headlines:
        filename = f"{feed.feed.title}_headlines.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headlines[0].keys())
            writer.writeheader()
            writer.writerows(headlines)
        return headlines, filename
    else:
        return [], ''



# Define the Streamlit app

def app():
    st.title('Solar Energy News Headlines')

    # Display text input fields for the user to enter the URLs of the Solar news RSS feeds
    url1 = st.text_input('Enter the URL of the first Solar news RSS feed:', 'https://solarquarter.com/feed/')
    url2 = st.text_input('Enter the URL of the second Solar news RSS feed:', 'https://www.pv-magazine.com/feed/')
    url3 = st.text_input('Enter the URL of the third Solar news RSS feed:', 'https://www.solarpowerworldonline.com/feed/')
    url4 = st.text_input('Enter the URL of the fourth Solar news RSS feed:', 'https://www.pv-magazine.com/category/markets-policy/finance/feed/')

    # Display a Submit button for the user to submit the URLs
    if st.button('Submit'):
        # Scrape the news headlines using the RSS feeds
        headlines1, filename1 = scrape_headlines(url1)
        headlines2, filename2 = scrape_headlines(url2)
        headlines3, filename3 = scrape_headlines(url3)
        headlines4, filename4 = scrape_headlines(url4)

        # Combine the headlines from all feeds into a single dataframe
        headlines = headlines1 + headlines2 + headlines3 + headlines4
        headlines_df = pd.DataFrame(headlines)

        # Store the headlines in session state
        st.session_state.headlines_df = headlines_df

    # Display the news headlines in a table if they exist in session state
    if 'headlines_df' in st.session_state:
        headlines_df = st.session_state.headlines_df
        st.write('## News Headlines')
        if not headlines_df.empty:
            # Add checkboxes to select headlines
            selected_headlines = st.multiselect('Select headlines to include in the final CSV file:', headlines_df['Title'].tolist(), key='checkbox')
            if selected_headlines:
                # Filter the dataframe to only include selected headlines
                selected_headlines_df = headlines_df[headlines_df['Title'].isin(selected_headlines)]
                st.table(selected_headlines_df[['Title', 'Published', 'Source']])
            else:
                st.table(headlines_df[['Title', 'Published', 'Source']])

            # Display a Download button for the user to download the selected headlines as a CSV file
            if st.button('Generate Final CSV File'):
                selected_headlines_df.to_csv('selected_headlines.csv', index=False)
                st.success('CSV file generated successfully!')
                st.download_button(
                    label='Download Selected Headlines CSV',
                    data=open('selected_headlines.csv', 'rb').read(),
                        file_name='selected_headlines.csv',
                        mime='text/csv'
                    )
            else:
                st.table(headlines_df[['Title', 'Published', 'Source']])
        else:
            st.write('No headlines found.')



if __name__ == '__main__':
    app()
