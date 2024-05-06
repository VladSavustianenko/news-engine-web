from utils import db


class Topic(db.Model):
    __tablename__ = 'Topic'
    __bind_key__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String)
    headline = db.Column(db.String)
    website_url = db.Column(db.String)
    teaser = db.Column(db.String)
    promo_image = db.Column(db.String)
    publish_date = db.Column(db.DateTime)
    description = db.Column(db.String)
    section = db.Column(db.String)
    subsection = db.Column(db.String)


class Content(db.Model):
    __tablename__ = 'Content'
    __bind_key__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)
    content = db.Column(db.String)


TOPICS = [
    {
        'topic': 'world',
        'subtopics': ['africa', 'europe', 'middle-east', 'americas', 'asia-pacific']
    },
    {
        'topic': 'wellbeing',
        'subtopics': ['mind', 'food-nutrition', 'fitness', 'life', 'body', 'extreme-weather', 'hurricanes-tropical-storms']
    },
    {
        'topic': 'usa',
        'subtopics': ['traffic-commuting', 'virginia', 'dc', 'public-safety', 'obituaries', 'maryland', 'education']
    },
    {
        'topic': 'travel',
        'subtopics': ['news', 'tips']
    },
    {
        'topic': 'transportation',
        'subtopics': None
    },
    {
        'topic': 'style',
        'subtopics': ['power', 'media', 'fashion', 'of-interest']
    },
    {
        'topic': 'sports',
        'subtopics': ['nba', 'soccer', 'olympics', 'highschools', 'mlb', 'colleges', 'boxing-mma', 'golf', 'wnba', 'nfl', 'nhl']
    },
    {
        'topic': 'space',
        'subtopics': None
    },
    {
        'topic': 'science',
        'subtopics': None
    },
    {
        'topic': 'religion',
        'subtopics': None
    },
    {
        'topic': 'politics',
        'subtopics': ['polling', 'courts-law', 'the-fix', 'the-202-newsletters', 'white-house']
    },
    {
        'topic': 'personal-tech',
        'subtopics': ['internet-access', 'tech-your-life', 'ethical-issues', 'whats-new', 'tech-work', 'data-privacy']
    },
    {
        'topic': 'personal-finance',
        'subtopics': None
    },
    {
        'topic': 'opinions',
        'subtopics': ['letters-to-the-editor', 'local-opinions', 'global-opinions', 'guest-opinions', 'the-posts-view']
    },
    {
        'topic': 'national',
        'subtopics': ['investigations', 'morning-mix']
    },
    {
        'topic': 'military',
        'subtopics': None
    },
    {
        'topic': 'made-by-history',
        'subtopics': None
    },
    {
        'topic': 'lifestyle',
        'subtopics': ['on-parenting', 'home-garden']
    },
    {
        'topic': 'justice',
        'subtopics': None
    },
    {
        'topic': 'immigration',
        'subtopics': None
    },
    {
        'topic': 'history',
        'subtopics': None
    },
    {
        'topic': 'health-care',
        'subtopics': None
    },
    {
        'topic': 'health',
        'subtopics': ['medical-mysteries']
    },
    {
        'topic': 'gender-identity',
        'subtopics': ['comics', 'workday', 'voices', 'more-stories']
    },
    {
        'topic': 'food',
        'subtopics': ['news', 'how-to']
    },
    {
        'topic': 'entertainment',
        'subtopics': ['theater', 'tv', 'video-games', 'art', 'comics', 'movies', 'music']
    },
    {
        'topic': 'energy',
        'subtopics': None
    },
    {
        'topic': 'economy',
        'subtopics': None
    },
    {
        'topic': 'economic-policy',
        'subtopics': None
    },
    {
        'topic': 'climate-environment',
        'subtopics': ['climate-lab', 'green-living', 'business-of-climate', 'environment']
    },
    {
        'topic': 'business',
        'subtopics': ['cryptocurrency', 'on-small-business', 'technology']
    },
    {
        'topic': 'animals',
        'subtopics': None
    },
    {
        'topic': 'abortion',
        'subtopics': None
    },
]
