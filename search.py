#!/usr/bin/python
import praw


#INPUTS
search_query = 'lo&lo'
#search_query = 'gtx, a'
#search_query = 'gtx,1080'
price_max = 500


# Find between [W] and [H]
# Find between $ and *space*
def find_between_r(str, first, last ):
    try:
        start = str.rindex( first ) + len( first )
        end = str.rindex( last, start )
        return str[start:end]
    except ValueError:
        return ""


# Parse the body for the search criteria
# Going to simplify once I get all of the paths
def find_matches(str, search):
    search_criteria = []
    if search.find(',') != -1:
        for search_str in search.split(','):
            search_criteria.extend(get_matches(str, search_str))
    else:
        search_criteria.extend(get_matches(str, search))

    return search_criteria


# Get matches
def get_matches(str, search_str):
    if search_str.find('&') != -1:
        all_conditions = True
        for condition in search_str.split('&'):
            try:
                if not get_matches_base(str, condition):
                    all_conditions = False
            except:
                pass
        if all_conditions:
            return get_matches_base(str, search_str.split('&')[0])
        else:
            return []
    else:
        return get_matches_base(str,search_str);


# Get matches base
def get_matches_base(str, search_str):
    temp_search_list = []
    for split in str.splitlines():
        try:
            if split.find(search_str) != -1:
                temp_search_list.append(split)
        except:
            pass
    return temp_search_list


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
            if value_text != "":
                value = get_value(value_text)
                if int(value) < price_max :
                    #print('Found! ' + search_item + " - $" + value)
                    print(submission.url)

    except Exception as e:
        pass

