import os
from googleapiclient.discovery import build


class Video:
    """Класс для ролика YouTube"""
    youtube_obj = None

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео.
        :param video_id: id видео
        video_title = название видео
        url = ссылка на видео
        view_count = количество просмотров
        like_count = количество лайков
        """
        self.__video_id = video_id
        api_key = os.environ.get('YOUTUBE_API')
        Video.youtube_obj = build('youtube', 'v3', developerKey=api_key)
        video_response = Video.youtube_obj.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=self.__video_id
                                                         ).execute()
        self.__video_title: str = video_response['items'][0]['snippet']['title']
        self.__url: str = 'https://www.youtube.com/channel/' + self.__video_id
        self.__view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.__like_count: int = video_response['items'][0]['statistics']['likeCount']

    @property
    def youtube_object(self):
        return Video.youtube_obj

    @property
    def video_title(self):
        return self.__video_title

    @property
    def view_count(self):
        return self.__view_count

    @property
    def like_count(self):
        return self.__like_count

    @property
    def url(self):
        return f'https://www.youtube.com/watch?v={self.__video_id}'

    def __str__(self):
        """
        :return: Название видео
        """
        return self.__video_title

    def print_info(self):
        """
        Выводит всю информацию о видео в json-формате
        :return: массив информации о видео
        """
        api_key = os.environ.get('YOUTUBE_API')
        Video.youtube_obj = build('youtube', 'v3', developerKey=api_key)
        video_response = Video.youtube_obj.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=self.__video_id
                                                         ).execute()
        print(video_response)


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id

    def __repr__(self):
        return super().__repr__() + '\n' + f"id плейлиста: {self.playlist_id}"
