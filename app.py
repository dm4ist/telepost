from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import telebot
import schedule
import time
import threading
import os

app = Flask(__name__, static_folder='../dist', static_url_path='')
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///telegram_poster.db'
db = SQLAlchemy(app)

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    fields = db.Column(db.JSON, nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'), nullable=False)
    content = db.Column(db.JSON, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    scheduled_time = db.Column(db.DateTime)
    views = db.Column(db.Integer, default=0)

class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    chat_id = db.Column(db.String(100), nullable=False)
    bot_token = db.Column(db.String(100), nullable=False)

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/templates', methods=['GET', 'POST'])
def handle_templates():
    if request.method == 'POST':
        data = request.json
        new_template = Template(name=data['name'], fields=data['fields'])
        db.session.add(new_template)
        db.session.commit()
        return jsonify({"message": "Template created successfully", "id": new_template.id}), 201
    else:
        templates = Template.query.all()
        return jsonify([{"id": t.id, "name": t.name, "fields": t.fields} for t in templates])

@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    if request.method == 'POST':
        data = request.json
        new_post = Post(
            channel_id=data['channel_id'],
            template_id=data['template_id'],
            content=data['content'],
            status='scheduled',
            scheduled_time=datetime.fromisoformat(data['scheduled_time'])
        )
        db.session.add(new_post)
        db.session.commit()
        return jsonify({"message": "Post scheduled successfully", "id": new_post.id}), 201
    else:
        posts = Post.query.all()
        return jsonify([{
            "id": p.id,
            "channel_id": p.channel_id,
            "template_id": p.template_id,
            "content": p.content,
            "status": p.status,
            "scheduled_time": p.scheduled_time.isoformat(),
            "views": p.views
        } for p in posts])

@app.route('/api/channels', methods=['GET', 'POST'])
def handle_channels():
    if request.method == 'POST':
        data = request.json
        new_channel = Channel(name=data['name'], chat_id=data['chat_id'], bot_token=data['bot_token'])
        db.session.add(new_channel)
        db.session.commit()
        return jsonify({"message": "Channel added successfully", "id": new_channel.id}), 201
    else:
        channels = Channel.query.all()
        return jsonify([{"id": c.id, "name": c.name, "chat_id": c.chat_id} for c in channels])

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    posts = Post.query.filter_by(status='sent').all()
    total_views = sum(post.views for post in posts)
    return jsonify({
        "total_posts": len(posts),
        "total_views": total_views,
        "average_views": total_views / len(posts) if posts else 0
    })

def send_scheduled_posts():
    posts = Post.query.filter_by(status='scheduled').all()
    for post in posts:
        if post.scheduled_time <= datetime.now():
            channel = Channel.query.get(post.channel_id)
            bot = telebot.TeleBot(channel.bot_token)
            
            try:
                # Отправка текста
                message = bot.send_message(channel.chat_id, post.content['text'])
                
                # Отправка медиа (если есть)
                if 'media' in post.content:
                    media_type = post.content['media']['type']
                    media_url = post.content['media']['url']
                    
                    if media_type == 'photo':
                        bot.send_photo(channel.chat_id, media_url)
                    elif media_type == 'video':
                        bot.send_video(channel.chat_id, media_url)
                    elif media_type == 'document':
                        bot.send_document(channel.chat_id, media_url)
                
                post.status = 'sent'
                post.views = message.views
                db.session.commit()
            except Exception as e:
                print(f"Error sending post {post.id}: {str(e)}")
                post.status = 'error'
                db.session.commit()

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    schedule.every(1).minutes.do(send_scheduled_posts)
    threading.Thread(target=run_scheduler).start()
    app.run(debug=True)