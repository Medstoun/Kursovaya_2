import json
from pprint import pprint
from config import *


class PostsDAO:

    def __init__(self):
        self.posts_list = None
        self.comments_list = None
        self.tags_list = None

    def load_posts(self):
        with open(POSTS_JSON, 'r', encoding='utf-8') as file:
            self.posts_list = json.load(file)

    def load_comments(self):
        with open(COMMENTS_JSON, 'r', encoding='utf-8') as file:
            self.comments_list = json.load(file)

    def get_posts(self):
        self.load_posts()

    def get_comments(self):
        self.load_comments()

    def get_all(self):
        self.get_posts()
        self.get_comments()

    def get_posts_by_user(self, user_name):
        user_posts_list = []
        self.get_posts()
        for post in self.posts_list:
            if post['poster_name'] == user_name:
                post_pk = post['pk']
                post = self.get_post_by_pk(post_pk)
                user_posts_list.append(post)
        return user_posts_list

    def get_comments_by_post_id(self, post_id):
        comments_list = []
        self.get_comments()
        for comment in self.comments_list:
            if comment['post_id'] == post_id:
                comments_list.append(comment)
        return comments_list

    def get_count_comments_for_post(self, post_id):
        all_posts_comments = self.get_comments_by_post_id(post_id)
        return len(all_posts_comments)

    def get_post_by_keyword(self, keyword):
        post_list = []
        self.get_posts()
        for post in self.posts_list:
            if keyword.lower() in post['content'].lower():
                post = self.get_post_by_pk(post['pk'])
                post_list.append(post)
        return post_list[:10]

    def get_post_by_pk(self, pk):
        self.get_all()
        for post in self.posts_list:
            if post['pk'] == pk:
                post['comments'] = self.get_comments_by_post_id(pk)
                post['comments_count'] = self.get_count_comments_for_post(pk)
                return post

    def get_posts_for_json(self):
        self.get_posts()
        posts_list = []
        for post in self.posts_list:
            posts_list.append(self.get_post_by_pk(post['pk']))
        return posts_list

    def get_main_page(self):
        self.get_all()
        posts_list = []
        for post in self.posts_list:
            post_id = post['pk']
            comments_count = self.get_count_comments_for_post(post_id)
            post['comments_count'] = comments_count
            posts_list.append(post)
        return posts_list

    def get_all_tags(self):
        self.get_posts()
        for post in self.posts_list:
            content = post['content'].lower()
            if '#' in content:
                content_list = content.split(' ')
                tags_list = []
                for word in content_list:
                    pass