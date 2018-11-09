
import bs4
import urllib
import pandas as pd
import itertools
import numpy as np
import re


input_url = 'https://www.quora.com/Where-can-I-find-full-data-science-case-studies'

def scrape_quora(input_url):
    """
    Description :
    Input  - Quora URL 
    Output - Dictionary with question as key and a DataFrame as value.
    DataFrame Contents : 'User_Name','Profile_Link','Occupation','Answered_On','Answer'
    
    Usage Example:
    
    input_url = 'https://www.quora.com/Where-can-I-find-full-data-science-case-studies'
    output = scrape_quora(input_url)
    """
    # scrape the page
    page = urllib.request.urlopen(input_url).read()
    soup = bs4.BeautifulSoup(page,'html.parser')
    question = soup.find('div',{'class':'QuestionArea'}).find('span',{'class':'ui_qtext_rendered_qtext'}).get_text()
        
    all_answers = soup.findAll('div',{'class':'answer_text_small'})    
    # create an empty DataFrame with structure needed.
    df = pd.DataFrame(columns=['User_Name','Profile_Link','Occupation','Answered_On','Answer'])   
    QandA = {}
    #loop through answers one by one and get the info
    for i in all_answers:
        answer_base = i.findAll('div',{'class':'Answer AnswerBase'})
        for j in answer_base:            
            user_info = j.find('div',{'class':'u-margin-right--sm'})
            try:
                user_name = user_info.find('a',{'class':'user'}).get_text()      
            except:
                user_name = 'Anonymous'
            try:
                user_link = 'https://www.quora.com'+user_info.find('a').get('href')
            except:
                user_link = np.nan
            try:
                occupation = user_info.find('span',{'class':'NameCredential'}).get_text()
            except:
                occupation = np.nan
            answered_on = user_info.find('span',{'class':'credibility_wrapper'}).get_text()
            answer = j.find('div',{'class':'ui_qtext_expanded'}).get_text()
            curr_row = {'User_Name': user_name,
                                     'Profile_Link':user_link,
                                     'Occupation':occupation,
                                     'Answered_On':answered_on,
                                     'Answer':answer}
            df = df.append(curr_row,ignore_index=True)
    QandA[input_url] = df
    
    return(QandA)


def scrape_related_questions(input_url):
    """   
    `
    Input  - Quora URL
    Output - Array with list of related questions.
    
    Usage -
    input_url = 'https://www.quora.com/Where-can-I-find-full-data-science-case-studies'
    output = scrape_related_questions(input_url)
    
    `
    """  
    related_questions = []
    page = urllib.request.urlopen(input_url).read()
    soup = bs4.BeautifulSoup(page,'html.parser')
    all_related_questions = soup.find('div',{'class':'question_related list side_bar'}).find('ul')
    for i in all_related_questions:
        try:
            url = 'https://www.quora.com'+i.find('a').get('href')
            related_questions.append(url)
        except:
            pass
    return(related_questions)

input_url = 'https://www.quora.com/What-are-the-best-institutes-to-study-data-science-in-chennai'

master_dictionary = scrape_quora(input_url)
related = scrape_related_questions(input_url)
for i in related:
    if i not in master_dictionary:
        tmp_dic = scrape_quora(i)
        master_dictionary[i] = tmp_dic[i]

master_df = pd.DataFrame.from_dict(master_dictionary,orient='index',columns=['Scraped_info'])

master_df.iloc[0]['Scraped_info']

