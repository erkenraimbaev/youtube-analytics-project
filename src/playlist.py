import datetime
import os

import isodate
from googleapiclient.discovery import build


class PlayList:
    """Класс для работы с плейлистом YouTube.
    """
    youtube_obj = None

    def __init__(self, playlist_id: str):
        """
        Инициализация объекта плэйлист ютуб
        :param playlist_id: id плэйлиста
        :param playlist_title: подтягивается из данных
        """
        self.__playlist_id = playlist_id
        api_key = os.environ.get('YOUTUBE_API')
        youtube_obj = build('youtube', 'v3', developerKey=api_key)
        playlists_response = youtube_obj.playlists().list(id=playlist_id, part='contentDetails,snippet').execute()
        self.__title = playlists_response['items'][0]['snippet']['title']

    @classmethod
    def get_youtube_object(cls):
        """
        Метод для получения объекта ютуб по API
        """
        api_key = os.environ.get('YOUTUBE_API')
        youtube_obj = build('youtube', 'v3', developerKey=api_key)
        return youtube_obj

    def get_video_response(self):
        """
        Метод класса для получения информации видео плэйлиста
        : return: список видео из плэйлиста
        """
        playlist_videos = PlayList.get_youtube_object().playlistItems().list(playlistId=self.__playlist_id,
                                                                             part='contentDetails',
                                                                             maxResults=50).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = PlayList.get_youtube_object().videos().list(part='contentDetails,statistics',
                                                                     id=','.join(video_ids)
                                                                     ).execute()
        return video_response

    @property
    def title(self):
        """Возвращает название плейлиста"""
        return self.__title

    @property
    def url(self):
        """Возвращает ссылку на плейлист"""
        return f'https://www.youtube.com/playlist?list={self.__playlist_id}'

    def __str__(self):
        """
        :return: удобочитаемая строка для пользователя - название плэйлиста
        """
        return self.__title

    @property
    def total_duration(self):
        """
        Метод, который возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста
        """
        video_response = PlayList.get_video_response(self)
        count_duration = datetime.timedelta(hours=0, minutes=0, seconds=0)
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            count_duration += duration
        return count_duration

    def show_best_video(self):
        """
        Метод, который возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        video_response = PlayList.get_video_response(self)
        list_for_video = []
        count_like = 0
        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > count_like:
                count_like = int(video['statistics']['likeCount'])
                list_for_video.append(video)
                if len(list_for_video) > 1:
                    del list_for_video[0]
        return print(f'https://youtu.be/{list_for_video[0]["id"]}')
