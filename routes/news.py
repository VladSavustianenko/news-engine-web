from flask import jsonify, request
from sqlalchemy import desc, or_, case

from domain.search_history import SearchHistory
from domain.topic import Topic, Content, TOPICS
from domain.view_history import ViewHistory
from helpers.functions import authorisation_required
from helpers.model_connector import fetch_recommendations, fetch_general_recommendations, collaborative_filter
from helpers.models import TopicDTO, FullTopicDTO, BaseTopicDTO, ViewHistoryDTO, SEARCH_TYPE
from helpers.queries import select_latest_topics_of_all_categories
from utils import app, db


@app.route('/api/news', methods=['GET'])
@authorisation_required
def get_news():
    latest_topics = select_latest_topics_of_all_categories(1).all()

    # Format the results
    result = [TopicDTO(topic).to_dict() for topic in latest_topics]

    return jsonify(result)


@app.route('/api/news/<id>', methods=['GET'])
@authorisation_required
def get_topic_by_id(id):
    try:
        # Attempt to convert the topic_id to an integer
        valid_id = int(id)
    except ValueError:
        # If conversion fails, return an error message indicating the problem
        return jsonify({'error': 'Invalid topic ID. Topic ID must be an integer.'}), 400

    if not id:
        return jsonify({"error": f"Invalid topic id: {id}"}), 400
    topic = Topic.query.filter_by(id=id).first()

    if topic is None:
        return jsonify({'error': f"Topic with id {id} not found"}), 404

    content = Content.query.filter_by(topic_id=id).first()

    return FullTopicDTO(topic, content.content).to_dict()


@app.route('/api/news/category/<category_name>', methods=['GET'])
@authorisation_required
def get_news_by_category(category_name):
    return get_news_by_category_and_subcategory(category_name)


@app.route('/api/news/category/<category_name>/<category_subname>', methods=['GET'])
@authorisation_required
def get_news_by_category_and_subcategory(category_name, session, category_subname=None):
    offset = request.args.get('offset')

    valid_topics = [topic['topic'] for topic in TOPICS]
    valid_subtopics = [subtopic for topic in TOPICS if topic['subtopics'] for subtopic in topic['subtopics']]

    if category_name not in valid_topics:
        return jsonify({"error": f"Category '{category_name}' is not valid"}), 400

    topics_query = Topic.query.filter_by(section=category_name)
    if category_subname and category_subname not in valid_subtopics:
        return jsonify({"error": f"Subcategory '{category_subname}' is not valid"}), 400
    elif category_subname:
        topics_query = topics_query.filter_by(subsection=category_subname)

    topics = topics_query.order_by(Topic.publish_date.desc()).offset(offset).limit(20).all()

    # Format the results
    result = [TopicDTO(topic).to_dict() for topic in topics]

    SearchHistory.add_history_item(user_id=session.user_id,
                                   value=category_subname if category_subname else category_name,
                                   search_type=SEARCH_TYPE['category'])

    return jsonify(result)


@app.route('/api/news/search', methods=['GET'])
@authorisation_required
def search_topics(session):
    search_text = request.args.get('text', '')
    offset = request.args.get('offset')

    if not search_text:
        return jsonify([])

    # Define a base query
    query = Topic.query

    # Scoring system: Increase score by 1 for each field match
    if search_text:
        # List of conditions for each field that the search text may match
        conditions = [
            Topic.headline.ilike(f'%{search_text}%'),
            Topic.description.ilike(f'%{search_text}%'),
            Topic.author.ilike(f'%{search_text}%'),
            Topic.teaser.ilike(f'%{search_text}%'),
            Topic.section.ilike(f'%{search_text}%'),
            Topic.subsection.ilike(f'%{search_text}%')
        ]
        condition_filters = or_(*conditions)
        # Calculating score for ordering directly in order_by
        score = (
            case([(Topic.headline.ilike(f'%{search_text}%'), 1)], else_=0) +
            case([(Topic.description.ilike(f'%{search_text}%'), 1)], else_=0) +
            case([(Topic.author.ilike(f'%{search_text}%'), 1)], else_=0) +
            case([(Topic.teaser.ilike(f'%{search_text}%'), 1)], else_=0) +
            case([(Topic.section.ilike(f'%{search_text}%'), 1)], else_=0) +
            case([(Topic.subsection.ilike(f'%{search_text}%'), 1)], else_=0)
        )

        # Apply the condition filter and scoring
        query = query.filter(condition_filters).order_by(desc(score), desc(Topic.publish_date))

    # Convert the results to a list of dictionaries
    result = [TopicDTO(topic).to_dict() for topic in query.offset(offset).limit(20).all()]

    SearchHistory.add_history_item(user_id=session.user_id, value=search_text, search_type=SEARCH_TYPE['text'])

    # Return the topics and pagination details
    return jsonify(result)


@app.route('/api/news/view', methods=['POST'])
@authorisation_required
def view_topic(session):
    topic_id = request.json.get('topicId')
    view_type = request.json.get('viewType')

    if not topic_id:
        return jsonify({'error': 'Topic id is not provided'}), 400

    if not view_type:
        return jsonify({'error': 'View type is not provided'}), 400

    ViewHistory.add_history_item(session.user_id, topic_id, view_type)

    return jsonify({'message': 'View history added'}), 201


@app.route('/api/topics', methods=['GET'])
@authorisation_required
def get_topics():
    return jsonify(TOPICS)


@app.route('/api/news/general-recommendations', methods=['GET'])
@authorisation_required
def get_general_recommendations(session):
    views_ids = [item[0] for item in db.session.query(ViewHistory.topic_id).filter(ViewHistory.user_id == session.user_id).distinct().all()]
    recommended_ids = []

    if not len(views_ids) or len(views_ids) < 5:
        ids = [ViewHistoryDTO(item[0], item[1]).to_dict() for item in db.session.query(ViewHistory.user_id, ViewHistory.topic_id).filter(
            ViewHistory.user_id != session.user_id).all()]
        recommended_ids = collaborative_filter(ids)['ids']
    else:
        base_topics = [BaseTopicDTO(topic).to_dict() for topic in Topic.query.filter(Topic.id.in_(views_ids)).all()]

        # last views
        last_views_ids = [item[0] for item in
            db.session.query(ViewHistory.topic_id)
            .filter(ViewHistory.user_id == session.user_id)
            .order_by(ViewHistory.created_at.desc())
            .all()
        ][:30]

        latest_topics = select_latest_topics_of_all_categories(50, last_views_ids).all()

        topics = [BaseTopicDTO(topic).to_dict() for topic in latest_topics]

        keywords = [item[0] for item in  db.session.query(SearchHistory.value).filter(SearchHistory.user_id == session.user_id).all()]

        recommended_ids = fetch_general_recommendations(base_topics, topics, keywords)['ids']

    recommended_topics = Topic.query.filter(Topic.id.in_(recommended_ids)).all()

    # Format the results
    result = [TopicDTO(topic).to_dict() for topic in recommended_topics]

    # Create a mapping from id to its index in the id_order list
    id_index = {id: index for index, id in enumerate(recommended_ids)}

    # Sort articles using the index of their id in the id_order list as the key
    sorted_articles = sorted(result, key=lambda x: id_index[x['id']])

    return jsonify(sorted_articles)


@app.route('/api/news/recommendations/<id>', methods=['GET'])
@authorisation_required
def get_recommendations(session, id):
    if not id:
        return jsonify({'message': 'Id is not provided'})

    base_topic = BaseTopicDTO(Topic.query.filter(Topic.id == id).first())

    # last views
    last_views_ids = [item[0] for item in
                      db.session.query(ViewHistory.topic_id)
                      .filter(ViewHistory.user_id == session.user_id)
                      .order_by(ViewHistory.created_at.desc())
                      .all()
                      ][:30]

    latest_topics = select_latest_topics_of_all_categories(50, last_views_ids).filter(Topic.id != base_topic.id).all()

    topics = [BaseTopicDTO(topic).to_dict() for topic in latest_topics]

    ids = fetch_recommendations(base_topic.to_dict(), topics)['ids']

    recommended_topics = Topic.query.filter(Topic.id.in_(ids)).all()

    # Format the results
    result = [TopicDTO(topic).to_dict() for topic in recommended_topics]

    # Create a mapping from id to its index in the id_order list
    id_index = {id: index for index, id in enumerate(ids)}

    # Sort articles using the index of their id in the id_order list as the key
    sorted_articles = sorted(result, key=lambda x: id_index[x['id']])

    return jsonify(sorted_articles)
