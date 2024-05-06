from datetime import datetime


class BaseTopicDTO:
    id: int
    headline: str
    description: str
    teaser: str

    def __init__(self, topic):
        self.id = topic.id
        self.headline = topic.headline
        self.description = topic.description
        self.teaser = topic.teaser

    def to_dict(self):
        return {
            "id": self.id,
            "headline": self.headline,
            "description": self.description,
            "teaser": self.teaser
        }


class TopicDTO(BaseTopicDTO):
    author: str
    section: str
    subsection: str
    date: datetime
    image: str

    def __init__(self, topic):
        super(TopicDTO, self).__init__(topic)

        self.author = topic.author
        self.section = topic.section
        self.subsection = topic.subsection
        self.date = topic.publish_date.isoformat()
        self.image = topic.promo_image

    def to_dict(self):
        base_dict = super(TopicDTO, self).to_dict()
        base_dict.update({
            "author": self.author,
            "section": self.section,
            "subsection": self.subsection,
            "date": self.date,
            "image": self.image
        })
        return base_dict


class FullTopicDTO(TopicDTO):
    content: str

    def __init__(self, topic, content):
        super(FullTopicDTO, self).__init__(topic)

        self.content = content.split('<PARAGRAPH>')

    def to_dict(self):
        topic_dict = super(FullTopicDTO, self).to_dict()
        topic_dict["content"] = self.content
        return topic_dict


class ViewHistoryDTO:
    user_id: int
    topic_id: int

    def __init__(self, user_id, topic_id):
        self.user_id = user_id
        self.topic_id = topic_id

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "topic_id": self.topic_id,
        }


VIEW_TYPE = {
    'other': 0,
    'basic': 1,
    'recommended': 2,
    'relevant': 3,
}

SEARCH_TYPE = {
    'category': 1,
    'text': 2,
}
