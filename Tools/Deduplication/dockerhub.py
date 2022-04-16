#coding=utf8

class Dockerhub:

    AI = 1
    EDGE = 2
    SERVERLESS = 4
    COMPONENT = 8
    VIDEO = 16

    __SCENARIO2FLAG = {
            'ai': 1,
            'edge': 2,
            'serverless': 4,
            'component': 8,
            'video': 16
        }
    __FLAG2SCENARIO = {
            1: 'ai',
            2: 'edge',
            4: 'serverless',
            8: 'component',
            16: 'video'
        }

    __REPO2FLAG = {
            'julia': AI,
            'adminer': COMPONENT,
            'kong': EDGE,
            'crux': SERVERLESS | AI | COMPONENT | EDGE | VIDEO,
            'joomla': VIDEO
        }

    def __init__(self) -> None:
        pass

    def scenario2flag(scenario):
        return Dockerhub.__SCENARIO2FLAG[scenario]

    def flag2scenario(flag):
        return Dockerhub.__FLAG2SCENARIO[flag]

    def repo2scenario_flag(repo):
        return Dockerhub.__REPO2FLAG[repo]
    
    def repos2flag():
        return Dockerhub.__REPO2FLAG

    def scenarios():
        return ['ai', 'edge', 'serverless', 'component', 'video']

    def get_images_with_new_version():
        return ["julia:buster", "adminer:standalone", "kong:latest", "crux:3.4", "joomla:php8.1-fpm-alpine"]

    def get_images_with_old_version():
        return ["julia:bullseye", "adminer:fastcgi", "kong:ubuntu", "crux:3.2", "joomla:php8.1-fpm"]
    
    def get_repositories():
        return ['julia', 'adminer', 'kong', 'crux', 'joomla']
        