import os


class Config(object):
    def __class_getitem__(self, item):
        return getattr(self, item)

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        self.key = value


class ProjectConfig(Config):
    Global = {
        'Task_Id': None,
        'I/O_Mode': ['Json', 'Json'],
        'Config_File': os.path.realpath(__file__),
    }

    Path = {
        'Project_Path': os.path.dirname(Global['Config_File']),
        'Static_Path': os.path.join(os.path.dirname(Global['Config_File']), 'static'),
        'Templates_Path': os.path.join(os.path.dirname(Global['Config_File']), 'templates'),
    }

