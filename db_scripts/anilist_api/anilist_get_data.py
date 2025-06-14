import requests
from time import sleep
#uncomment valid one
#from insert_into_tables import insert_into
from db_scripts.anilist_api.table_movies_genres import insert_into
query_template = '''
query ($page: Int) {
  Page(page: $page, perPage: 50) {
    pageInfo {
      total
      currentPage
      lastPage
      hasNextPage
    }
    media(type: ANIME, sort: ID_DESC) {
      id
      title {
        romaji
        english
        native
      }
      description
      coverImage {
        medium
      }
      genres
      averageScore
      seasonYear
    }
  }
}
'''

url = 'https://graphql.anilist.co'

page = 1
while True:
    print(f"Fetching page {page}...")
    response = requests.post(url, json={
        'query': query_template,
        'variables': {'page': page}
    })
    if response.status_code != 200:
        print(response.json())
        break
    json_data = response.json()
    media_list = json_data['data']['Page']['media']
    if not media_list:
        break
    for media in media_list:
        insert_into(media)
    page_info = json_data['data']['Page']['pageInfo']
    if not page_info['hasNextPage']:
        break

    page += 1
    sleep(2) #set depending on current limit of api load (now 30 requests/min)