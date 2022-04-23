from flask import Flask, request, render_template, jsonify
from posts_dao import PostsDAO
import logging

logging.basicConfig(encoding='utf-8', level=logging.INFO)

dao = PostsDAO()
app = Flask(__name__)


@app.route('/')
def get_main_page():
    posts_list = dao.get_main_page()
    return render_template('index.html', posts_list=posts_list)


@app.route('/posts/<int:post_id>/')
def get_post_by_id(post_id):
    single_post_dict = dao.get_post_by_pk(post_id)
    return render_template('post.html', post=single_post_dict)


@app.route('/search/')
def get_search():
    search_str = request.args.get('s')
    logging.info(f'Поисковая фраза: {search_str}')

    post_list = dao.get_post_by_keyword(search_str)[:10]
    logging.info(f'Поисковый список: {post_list}')
    search_count = len(post_list)

    return render_template('search.html', post_list=post_list, scount=search_count)


@app.route('/users/<string:username>/')
def get_posts_by_user(username):
    user_posts = dao.get_posts_by_user(username)
    return render_template('user-feed.html', posts=user_posts)


@app.route('/api/posts/')
def get_posts_json_api():
    posts_list = dao.get_posts_for_json()
    return jsonify(posts_list)


@app.route('/api/posts/<int:post_id>')
def get_post_json_api(post_id):
    post = dao.get_post_by_pk(post_id)
    return jsonify(post)


app.config['JSON_AS_ASCII'] = False

if __name__ == '__main__':
    app.run()