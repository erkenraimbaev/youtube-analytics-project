from googleapiclient.discovery import build
import os
import json


class Channel:
    """Класс для ютуб-канала"""
    youtube_object = None

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        api_key = os.environ.get('YOUTUBE_API')
        Channel.youtube_object = build('youtube', 'v3', developerKey=api_key)
        channel = Channel.youtube_object.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        # название канала
        self.__name = channel.get('items')[0].get('snippet').get('title')
        # описание канала
        self.__description = channel.get('items')[0].get('snippet').get('description')
        # custom URL канала
        self.__customURL = channel.get('items')[0].get('snippet').get('customUrl')
        # Общее количество просмотров
        self.__viewCount = int(channel.get('items')[0].get('statistics').get('viewCount'))
        # Количество подписчиков
        self.__subscriberCount = int(channel.get('items')[0].get('statistics').get('subscriberCount'))
        # Количество видео на канале
        self.__videoCount = int(channel.get('items')[0].get('statistics').get('videoCount'))

    def __str__(self):
        """
        Магический метод, отображает удобочитаемую строку для пользователя
        """
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """
        Метод срабатывает, когда используется оператор сложения.
        В параметре other хранится то, что справа от знака +
        """
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        """
        Метод срабатывает, когда используется оператор сложения.
        В параметре other хранится то, что справа от знака +
        """
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        """
        Метод срабатывает, когда используется оператор >.
        В параметре other хранится то, что справа от знака +
        """
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        """
        Метод срабатывает, когда используется оператор >=.
        В параметре other хранится то, что справа от знака +
        """
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        """
        Метод срабатывает, когда используется оператор <.
        В параметре other хранится то, что справа от знака +
        """
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        """
        Метод срабатывает, когда используется оператор <=.
        В параметре other хранится то, что справа от знака +
        """
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        """
        Метод срабатывает, когда используется оператор ==.
        В параметре other хранится то, что справа от знака +
        """
        return self.subscriber_count == other.subscriber_count

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__name

    @property
    def video_count(self):
        return self.__videoCount

    @property
    def view_count(self):
        return self.__viewCount

    @property
    def subscriber_count(self):
        return self.__subscriberCount

    @property
    def url(self):
        return 'https://www.youtube.com/channel/' + self.__channel_id

    @property
    def custom_url(self):
        return 'https://www.youtube.com/' + self.__customURL

    @property
    def description(self):
        return self.__description

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        channel = Channel.youtube_object.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return print(channel)

    @classmethod
    def get_service(cls):
        return cls.youtube_object

    def to_json(self):
        """Сохраняет в файл значения атрибутов экземпляра Channel.
        Название файла соответствует названию канала YouTube.
        """
        # Создаем словарь
        channel_dict = {'channel name': self.title,
                        'channel_id': self.__channel_id,
                        'description': self.__description,
                        'channel URL': self.url,
                        'channel custom URL': self.custom_url,
                        'subscriber count': self.subscriber_count,
                        'view count': self.view_count,
                        'video count': self.video_count
                        }
        file_name_list = [self.title, 'json']
        with open('.'.join(file_name_list), 'w', encoding='utf-8') as file:
            json.dump(channel_dict, file, indent=4)
