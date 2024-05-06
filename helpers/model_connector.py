import requests

model_url = 'http://127.0.0.1:1000'

headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json'
}


def fetch_recommendations(base_topic, topics):
    return requests.post(
        url=model_url + '/recommendations',
        headers=headers,
        json={'topics': topics, 'base_topic': base_topic}
    ).json()


def fetch_general_recommendations(base_topics, topics, keywords=[]):
    return requests.post(
        url=model_url + '/general_recommendations',
        headers=headers,
        json={'topics': topics, 'base_topics': base_topics, 'keywords': keywords}
    ).json()


def collaborative_filter(data):
    return requests.post(
        url=model_url + '/collaborative-filter',
        headers=headers,
        json=data
    ).json()
