from app import create_app
from models import db, User, Camera, ObjectItem, Event

app = create_app()
with app.app_context():
    print('=== USERS ===')
    for user in User.query.all():
        print(f'ID: {user.id}, Username: {user.username}, Email: {user.email}, Role: {user.role}')
    
    print('\n=== CAMERAS ===')
    cameras = Camera.query.all()
    if cameras:
        for camera in cameras:
            print(f'ID: {camera.id}, Name: {camera.name}, Type: {camera.type}')
    else:
        print('No cameras in database')
    
    print('\n=== OBJECTS ===')
    objects = ObjectItem.query.all()
    if objects:
        for obj in objects:
            print(f'ID: {obj.id}, Name: {obj.name}, Classification: {obj.classification}')
    else:
        print('No objects in database')
    
    print('\n=== EVENTS ===')
    events = Event.query.all()
    if events:
        for event in events:
            print(f'ID: {event.id}, Type: {event.type}, Timestamp: {event.timestamp}')
    else:
        print('No events in database')
