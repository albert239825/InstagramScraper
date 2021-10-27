from instascrape import Profile, scrape_posts, Post
from selenium.webdriver import Chrome
from datetime import datetime
import pandas as pd
import numpy as np
import pickle
from openpyxl.workbook.child import INVALID_TITLE_REGEX
import re


def get_top_post(scraped_posts, cut_off_date=datetime(2021, 8, 1)):
    # Checking if an empty array was inputed
    if (type(scraped_posts) != list):
        raise TypeError("Input is not a list")
    if (len(scraped_posts) == 0):
        raise ValueError("Empty posts list imported")

    # Returning Post with the highest number of likes
    top_post = scraped_posts[0]

    for post in scraped_posts:
        if (type(post) != Post):
            raise TypeError(
                "One or more objects in the list is not a Post object")
        if (datetime.fromtimestamp(post.timestamp) < cut_off_date):
            if (post.likes > top_post.likes):
                top_post = post
        else:
            print("Post posted on {}, after the deadline".format(
                datetime.fromtimestamp(post.timestamp)))

    return top_post


def check_valid_username(users):
    for i in range(0, len(users)):
        if (not pd.isnull(users.iloc[i]['IG Username'])):
            try:
                print(users.iloc[i]["IG Username"])
                profile = Profile(users.iloc[i]['IG Username'])
            except:
                print("{} is not a valid user name, the username is located at index {}, its name is {}".format(
                    users.iloc[i]["IG Username"], i, users.iloc[i]['School']))


def create_post_df(scraped_posts):
    # Create Data Frame with collumns for post attributes
    df = pd.DataFrame(
        columns=['post_url', 'date_posted', 'number_of_likes', 'number_of_comments'])

    # Declaring types for each collumn
    df['post_url'] = df['post_url'].astype(object)
    df['date_posted'] = df['date_posted'].astype('datetime64[ns]')
    df['number_of_likes'] = df['number_of_likes'].astype('Int64')
    df['number_of_comments'] = df['number_of_comments'].astype('Int64')

    for i in range(0, len(scraped_posts)):
        cur_post = scraped_posts[i]
        df.at[i, 'post_url'] = "instagram.com/p/{}".format(cur_post.shortcode)
        df.at[i, 'date_posted'] = datetime.fromtimestamp(cur_post.timestamp)
        df.at[i, 'number_of_likes'] = cur_post.likes
        df.at[i, 'number_of_comments'] = cur_post.comments

    # return filled dataframe
    return df


def write_to_excel(user_post_dfs, users_df):
    if (len(user_post_dfs) != users_df.shape[0]):
        raise ValueError("length of the posts dataframes and user dataframes are mismatched, there are {} posts dataframes and {} rows in the user dataframe".format(
            len(user_post_dfs), users_df.shape[0]))

    with pd.ExcelWriter('User Data.xlsx', engine='openpyxl') as writer:
        for i in users_df.index:
            # this regex statement replaces excel's invalid characters with and underscore
            print(users_df.at[i, 'School'])
            title = re.sub(INVALID_TITLE_REGEX, '_', users_df.at[i, 'School'])
            users_df.iloc[[i]].to_excel(writer, sheet_name=title, index=False)
            user_post_dfs[i].to_excel(
                writer, startrow=3, sheet_name=title, index=False)
