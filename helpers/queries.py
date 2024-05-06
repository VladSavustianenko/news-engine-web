from domain.topic import Topic
from utils import db
from sqlalchemy import func, select


def select_latest_topics_of_all_categories(number: int, exclude_ids=[]):
    # Define an inner query to use ROW_NUMBER() over a partition by section, ordered by publish_date descending
    inner_stmt = db.session.query(
        Topic.id,
        Topic.section,
        Topic.publish_date,
        func.row_number().over(partition_by=Topic.section, order_by=Topic.publish_date.desc()).label('rn')
    ).subquery()

    # Define an outer query to select topics from the inner query where row number is <= number
    outer_stmt = select([inner_stmt]).where(inner_stmt.c.rn <= number)

    # Execute the query and fetch all results
    latest_topics_ids = db.session.execute(outer_stmt).fetchall()

    # Extract just the topic IDs from the query results
    topic_ids = [result.id for result in latest_topics_ids if result.id not in exclude_ids]

    # Now retrieve the full topic objects for these IDs
    return Topic.query.filter(Topic.id.in_(topic_ids)).order_by(Topic.publish_date.desc())
