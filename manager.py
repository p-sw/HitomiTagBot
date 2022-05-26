import requests
from bs4 import BeautifulSoup
import db


def tag_crawler():
    FEMALE = '♀'
    MALE = '♂'

    for alphabet_num in range(ord('a'), ord('z')+1):
        api_url = f'https://hitomi.la/alltags-{chr(alphabet_num)}.html'
        print(f'SENT GET TO {api_url}')
        response = requests.get(api_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for posts in soup.find_all('ul', {'class': 'posts'}):
            for item in posts.find_all('li', recursive=False):
                tag = item.get_text()
                tag = tag.replace(" ", "_")
                tag_num = tag[tag.index('(')+1:tag.index(')')]
                tag = tag[:tag.index('(')]
                prefix = "tag"
                if FEMALE in tag:
                    prefix = "female"
                    tag = tag[:tag.index(FEMALE)]
                elif MALE in tag:
                    prefix = "male"
                    tag = tag[:tag.index(MALE)]
                if tag[-1] == '_':
                    tag = tag[:-1]
                print(f'("{prefix}", "{tag}", {tag_num})')
                query = f"INSERT INTO Tags VALUES ('{prefix}','{tag}',{tag_num})"
                db.DB_OBJECT.execute(query)
        db.DB_OBJECT.commit()
tag_crawler()
