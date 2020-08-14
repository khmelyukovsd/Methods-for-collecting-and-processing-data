# -*- coding: utf-8 -*-
import re
import json
import scrapy
from copy import deepcopy
from urllib.parse import urlencode
from InstaParser.items import InstaparserItem

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    insta_login = 'khmelyukovat'
    insta_password = '#PWD_INSTAGRAM_BROWSER:10:1592677325:AdFQAPgQIZdpTkc9C8tW2HdpetPch6H241M+mXaOtNFdOuI37Kx9rF7KYydhD1HvdxXiaXOIJca4nVJbkEUP6oAcpdpr/mhh2XaHe1STx8VjkgDXJhOKcOP4NOfsSDPhJBz7GBGn+3tqoFlI/s+4JqY='
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'

    #hash_posts = 'eddbde960fed6bde675388aac39a3657'
    hash_followers = 'c76146de99bb02f6415203be841dd25a'
    hash_following = 'd04b0a864b4b54837c0d870b0e77e076'
    graphql_url = 'https://www.instagram.com/graphql/query/?'

    def __init__(self, name_user):
        self.parser_user = name_user

    def parse(self, response):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.insta_login_link,
            method='POST',
            callback=self.parse_user,
            formdata={'username': self.insta_login,
                      'enc_password': self.insta_password},
            headers={'X-CSRFToken': csrf_token}
        )
        pass

    def parse_user(self, response):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            yield response.follow(
                f'/{self.parser_user}',
                callback=self.user_data_parse,
            )

    def user_data_parse(self, response):
        user_id = self.fetch_user_id(response.text, self.parser_user)
        variables = {"id": user_id,
                     "first": 12}

        url_followers = f'{self.graphql_url}query_hash={self.hash_followers}&{urlencode(variables)}'
        yield response.follow(
            url_followers,
            callback=self.followers_parse,
            cb_kwargs={'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

        url_following = f'{self.graphql_url}query_hash={self.hash_following}&{urlencode(variables)}'
        yield response.follow(
            url_following,
            callback=self.following_parse,
            cb_kwargs={'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

    def followers_parse(self, response, user_id, variables):
        j_body = json.loads(response.text)
        page_info = j_body.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            url_followers = f'{self.graphql_url}query_hash={self.hash_followers}&{urlencode(variables)}'

            yield response.follow(
                url_followers,
                callback=self.followers_parse,
                cb_kwargs={'user_id': user_id,
                           'variables': deepcopy(variables)}
            )

        followers = j_body.get('data').get('user').get('edge_followed_by').get('edges')
        for follower in followers:
            item = InstaparserItem(
                id=follower['node']['id'],
                username=follower['node']['username'],
                profile_pic=follower['node']['profile_pic_url'],
                status='followers'
            )
            yield item

    def following_parse(self, response, user_id, variables):
        j_body = json.loads(response.text)
        page_info = j_body.get('data').get('user').get('edge_follow').get('page_info')
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']

            url_following = f'{self.graphql_url}query_hash={self.hash_following}&{urlencode(variables)}'

            yield response.follow(
                url_following,
                callback=self.following_parse,
                cb_kwargs={'user_id': user_id,
                           'variables': deepcopy(variables)}
            )

        followers = j_body.get('data').get('user').get('edge_follow').get('edges')
        for follower in followers:
            item = InstaparserItem(
                id=follower['node']['id'],
                username=follower['node']['username'],
                profile_pic=follower['node']['profile_pic_url'],
                status='followed_by'
            )
            yield item

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(matched).get('id')
