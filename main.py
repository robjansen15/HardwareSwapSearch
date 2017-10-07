#!/usr/bin/python
import praw


#INPUTS
search_query = 'Dell'
price_max = 500


# Find between [W] and [H]
def find_between_r(str, first, last ):
    try:
        start = str.rindex( first ) + len( first )
        end = str.rindex( last, start )
        return str[start:end]
    except ValueError:
        return ""


# Parse the body for the search criteria
def find_matches(str, search):
    search_criteria = []
    try:
        for split in str.splitlines():
            if(split.find(search) == -1):
                continue
            else:
                search_criteria.append(split)
        return search_criteria
    except ValueError:
        return ""


# Get number from a string
def get_value(str):
    try:
        for s in str.split():
            if s.isdigit():
                return s
    except ValueError:
        return ""


#CONSTANTS
start_string = '[H]'
end_string = '[W]'

#MAIN
reddit = praw.Reddit(client_id='BadL5FdbIk7neA',
                    client_secret='m7vInPM4UTDWu0_9uza7nueT6jA',
                    user_agent='practiceagent')

subreddit = reddit.subreddit('hardwareswap')
search_query = search_query.lower()

for submission in subreddit.stream.submissions():
    try:
        #Get the title
        title = find_between_r(submission.title, start_string, end_string)

        #Get the body
        body = submission.selftext.lower()
        #Search the body
        search_list = find_matches(submission.selftext, search_query)
        for search_item in search_list:
            value_text = find_between_r(search_item, "$", " ")
            if(value_text != ""):
                value = get_value(value_text)
                if int(value) < price_max :
                    print('Found! ' + search_query + " - $" + value)
                    print(submission.url)

    except Exception as e:
        pass

