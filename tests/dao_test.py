import pytest
from posts_dao import PostsDAO
import app

dao = PostsDAO()


class TestPostDAO:
    def test_create_postsDAO_object(self):
        assert isinstance(dao, PostsDAO) == True

    def test_list_get_posts(self):
        dao.get_posts()

        assert isinstance(dao.posts_list, list) == True
        assert isinstance(dao.posts_list[0], dict) == True
        assert dao.posts_list[0]["poster_name"]
        assert dao.posts_list[0]["poster_avatar"]
        assert dao.posts_list[0]["pic"]
        assert dao.posts_list[0]["content"]
        assert dao.posts_list[0]["views_count"]
        assert dao.posts_list[0]["likes_count"]
        assert dao.posts_list[0]["pk"]

    def test_list_get_comments(self):
        dao.get_comments()

        assert isinstance(dao.comments_list, list) == True
        assert isinstance(dao.comments_list[0], dict) == True
        assert dao.comments_list[0]['post_id']
        assert dao.comments_list[0]['commenter_name']
        assert dao.comments_list[0]['comment']
        assert dao.comments_list[0]['pk']

    def test_get_posts_by_user(self, data='leo'):
        assert isinstance(dao.get_posts_by_user(data), list) == True
        assert len(dao.get_posts_by_user(data)) > 0, 'Ожидается 1 и более'
        assert dao.get_posts_by_user(data)[0]['comments_count'], 'Ожидается наличие ключа comments_count'

    def test_get_post_by_keyword(self, data='ЕДА'):
        assert isinstance(dao.get_post_by_keyword(data), list) == True
        assert len(dao.get_post_by_keyword(data)) > 0, 'Ожидается 1 и более'

    def test_get_post_by_pk(self, data=1):
        post = dao.get_post_by_pk(data)

        assert type(post) == dict, "Ожидается dict"
        assert post["poster_name"]
        assert post["poster_avatar"]
        assert post["pic"]
        assert post["content"]
        assert post["views_count"]
        assert post["likes_count"]
        assert post["pk"]
        assert post['comments']
        assert post['comments_count']

    def test_get_posts_for_json(self):
        list_for_jsonify = dao.get_posts_for_json()

        assert isinstance(list_for_jsonify, list) == True
        assert len(list_for_jsonify) > 0, 'Ожидается 1 и более'

    def test_get_main_page(self):
        list_main_page = dao.get_main_page()

        assert isinstance(list_main_page, list) == True
        assert len(list_main_page) > 0, 'Ожидается 1 и более'


class TestAPI:

    def test_get_response_all_posts(self):
        response = app.app.test_client().get('/api/posts/')
        assert response.status_code == 200

    def test_get_all_posts_is_list(self):
        response = app.app.test_client().get('/api/posts/')
        assert type(response.json) == list, 'Не list'

    def test_get_all_posts_is_keys(self):
        allowed_keys = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count",
                        "pk", 'comments', 'comments_count'}

        response = app.app.test_client().get('/api/posts/')
        posts_list = response.json
        assert len(posts_list) > 0, "Пустой JSON"
        for post in posts_list[:3]:
            post_keys = set(post.keys())
            assert post_keys == allowed_keys, f"Ключи {post_keys} не соответствуют ожидаемым"
            assert post['pic'] != None, 'Отсутствует картинка'
            assert len(post['pic']) > 3, 'Очень короткий URL картинки'
            assert type(post['pic']) is str, 'URL картинки не является строкой'

    def test_get_response_one_post(self):
        response = app.app.test_client().get('/api/posts/1')
        assert response.status_code == 200

    def test_get_one_post_is_dict(self):
        response = app.app.test_client().get('/api/posts/1')
        assert type(response.json) is dict, f'{response} не является словарём'

    def test_get_one_post_is_keys(self):
        allowed_keys = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count",
                        "pk", 'comments', 'comments_count'}

        response = app.app.test_client().get('/api/posts/1')
        post_keys = response.json.keys()
        post_dict = response.json
        assert post_keys == allowed_keys, f"Ключи {post_keys} не соответствуют ожидаемым"
        assert post_dict['pic'] is not None, 'Отсутствует картинка'
        assert len(post_dict['pic']) > 3, 'Очень короткий URL картинки'
        assert type(post_dict['pic']) is str, 'URL картинки не является строкой'
