# Flat rent

Flat rent - is my pet project, just for learning some web technologies. 

## It is not commercial. 
- It is using the Telegram API to fetch messages about what flats are available for rent now.
- Celery is used to refresh and clear the database periodically. 
- Idea is that the database is not a core of the project and can be switched later. For example, from MongoDB to PostgreSQL, without changing the code of other project components. 
- Something like "Clear architecture", where components are separated and communicate with each other just by APIs. Their implementation details are hidden. For example, other services should not feel the difference in using PostgreSQL or MongoDB.
- Product results will be available by RESTful API provided by the Flask microframework. 
- Web UI will be added later.