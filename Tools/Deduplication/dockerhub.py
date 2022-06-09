#coding=utf-8

class Dockerhub:

    AI = 1
    EDGE = 2
    COMPONENT = 4
    SERVERLESS = 8
    VIDEO = 16

    __scenario2flag = {
        'ai': 1,
        'edge': 2,
        'component': 4,
        'serverless': 8,
        'video': 16
    }
    __flag2scenario = {
        1: 'ai',
        2: 'edge',
        4: 'component',
        8: 'serverless',
        16: 'video'
    }

    # __WORK_PATH = '/root/'
    __WORK_PATH = 'DockerHub_images/'
    __SCENARIO_PATH = __WORK_PATH + 'Scenario/'

    def __read_file(file_name):
        res = []
        with open(file_name, 'r', encoding='utf-8') as fd:
            for line in fd.readlines():
                line = line.strip().split()
                res.append(line[0])
        return res

    def get_images_with_new_version():
        return Dockerhub.__read_file(Dockerhub.__WORK_PATH + 'New.txt')

    def get_images_with_old_version():
        return Dockerhub.__read_file(Dockerhub.__WORK_PATH + 'Old.txt')

    def get_images_all():
        return Dockerhub.__read_file(Dockerhub.__WORK_PATH + 'All.txt')

    def get_repos_all():
        repos = set()
        for image in Dockerhub.get_images_all():
            repos.add(image.split(':')[0])
        return list(repos)

    def get_repos_ai():
        return Dockerhub.__read_file(Dockerhub.__SCENARIO_PATH + 'ai.txt')

    def get_repos_at():
        return Dockerhub.__read_file(Dockerhub.__SCENARIO_PATH + 'at.txt')

    def get_repos_edge():
        return Dockerhub.__read_file(Dockerhub.__SCENARIO_PATH + 'edge.txt')

    def get_repos_component():
        return Dockerhub.__read_file(Dockerhub.__SCENARIO_PATH + 'component.txt')

    def get_repos_serverless():
        return Dockerhub.__read_file(Dockerhub.__SCENARIO_PATH + 'serverless.txt')

    def get_repos_video():
        return Dockerhub.__read_file(Dockerhub.__SCENARIO_PATH + 'video.txt')

    def repo2scenario():
        res = {}
        for repo in Dockerhub.get_repos_all():
            res[repo] = 0
        
        for repo in Dockerhub.get_repos_ai():
            res[repo] |= Dockerhub.AI
        for repo in Dockerhub.get_repos_edge():
            res[repo] |= Dockerhub.EDGE
        for repo in Dockerhub.get_repos_component():
            res[repo] |= Dockerhub.COMPONENT
        for repo in Dockerhub.get_repos_serverless():
            res[repo] |= Dockerhub.SERVERLESS
        for repo in Dockerhub.get_repos_video():
            res[repo] |= Dockerhub.VIDEO
        return res

    def repotscenario():
        res = {}
        for repo in Dockerhub.get_repos_all():
            res[repo] = 0
        
        for repo in Dockerhub.get_repos_at():
            res[repo] |= Dockerhub.AI
        for repo in Dockerhub.get_repos_edge():
            res[repo] |= Dockerhub.EDGE
        for repo in Dockerhub.get_repos_component():
            res[repo] |= Dockerhub.COMPONENT
        for repo in Dockerhub.get_repos_serverless():
            res[repo] |= Dockerhub.SERVERLESS
        for repo in Dockerhub.get_repos_video():
            res[repo] |= Dockerhub.VIDEO
        return res

    def scenario2flag(scenario: str):
        return Dockerhub.__scenario2flag[scenario]

    def flag2scenario(flag: int):
        return Dockerhub.__flag2scenario[flag]

    def scenarios():
        return ['ai', 'edge', 'component', 'serverless', 'video']