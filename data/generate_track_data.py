import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import csv
import pandas as pd


def get_playlist_uri(playlist_link):
    return playlist_link.split("/")[-1].split("?")[0]


def get_track_data(playlists):
    index = 0
    for index in range(len(playlists)):
        scope = "user-library-read"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        tracks = []
        playlist_uri = get_playlist_uri(
            playlists[index])

        # Getting features of the playlists -> songs
        for track in sp.playlist_tracks(playlist_uri)["items"]:
            track_uri = track["track"]["uri"]
            track_name = track["track"]["name"]

            artist_uri = track["track"]["artists"][0]["uri"]
            artist_info = sp.artist(artist_uri)

            track_pop = track["track"]["popularity"]
            track_genre = artist_info["genres"]
            result = track_name, track_pop, track_genre, sp.audio_features(
                track_uri)
            tracks.append(result)

        # Dumps the playlist data into json
        json_object = json.dumps(tracks, indent=4)
        with open('playlist' + str(index) + '.json', "w") as outfile:
            outfile.write(json_object)
        with open('playlist' + str(index) + '.json') as json_file:
            data = json.load(json_file)

        # print(data)

        data_file = open('playlist' + str(index) + '.csv', 'w')
        csv_writer = csv.writer(data_file)

        # Song Titles
        song_titles = []
        for i in range(len(data)):
            song_title_data = data[i][0]
            song_titles.append(song_title_data)
            # print(anijpop_playlist)

        df = pd.DataFrame(song_titles)
        df = df.rename({0: 'artists'}, axis=1)

        # Track Popularity

        pop_scores = []
        for i in range(len(data)):
            pop_data = data[i][1]
            pop_scores.append(pop_data)

        df2 = pd.DataFrame(pop_scores)
        df2 = df2.rename({0: 'popularity'}, axis=1)

        # Genre

        genres = []
        for i in range(len(data)):
            genre_data = data[i][2]
            genres.append(genre_data)

        df3 = pd.DataFrame(genres)
        # print(df3)
        df3 = df3.iloc[:, 0]

        # Audio Features
        count = 0
        for i in range(len(data)):
            feature_data = data[i][3]

            for ap in feature_data:
                if count == 0:
                    # Writing headers of CSV file
                    header = ap.keys()
                    csv_writer.writerow(header)
                    count += 1

                # Writing data of CSV file
                csv_writer.writerow(ap.values())

        data_file.close()

        playlist_data = pd.read_csv('playlist' + str(index) + '.csv')

        playlist_data['song_title'] = df
        playlist_data['popularity_scores'] = df2
        playlist_data['genre'] = df3

        # Combined all the dataframes and saves into csv in designated folder
        playlist_data.to_csv(
            'playlists-set-9/playlist' + str(index+147) + '.csv')

    index += 1


def main():
    playlists = [
        # set 1 friends 1
        # 'https://open.spotify.com/playlist/51oJafNKqhO86MvrSUNnM6?si=45e3ffaf67c74f24',
        # 'https://open.spotify.com/playlist/3gDerXsHo97eVrvJb7xuZA?si=8996ad90fb1f4ad7',
        # 'https://open.spotify.com/playlist/2npVMxHA2kmMfwQyRubcQ2?si=ed647080f4d54ac7',
        # 'https://open.spotify.com/playlist/6XNkqs1Qx4UmqNKnjjSwvN?si=e3a0571fe0d3439c',
        # 'https://open.spotify.com/playlist/4XFFrQU7Hd8xkqlIKWgsDC?si=44d528a9e3e64002',
        # 'https://open.spotify.com/playlist/0uSmsYVXyuAVWksWXLJJ4K?si=99ccb2ede7cc4557',
        # 'https://open.spotify.com/playlist/5Em8wFOn6HUhgxyZfwL20L?si=9a11ee0d2e6547c9',
        # 'https://open.spotify.com/playlist/66tnEJe5aLT6sTHCv2jTdL?si=92b9e0f55c0f451a',
        # 'https://open.spotify.com/playlist/696lRmFa6jYp001xGqEszS?si=bf5378d1540946e4',
        # 'https://open.spotify.com/playlist/6KwmGN7iMbG84QvFSEs8F4?si=c9b23765a23b4e94',
        # 'https://open.spotify.com/playlist/2SaFA9fLH4BC5HellRivKG?si=ee46a1a435e14682',
        # 'https://open.spotify.com/playlist/4fDvqcJ2mTYMBaKkCmD6ZK?si=687a919f06304ba7',
        # 'https://open.spotify.com/playlist/7FSafMPY4wfkYsEOA1Maof?si=6722c6caa2e44be4',
        # 'https://open.spotify.com/playlist/1GICOv937KVIsBe5gqosjH?si=9e9dc1c3ebd34048',
        # 'https://open.spotify.com/playlist/4mLp6u7cpvne2Clx15UtcD?si=zgjjvIH4TImdIIHIQ3yYEQ',
        # 'https://open.spotify.com/playlist/1l6LRdr88FXAJQzDSHTKL1?si=4UsXetGpRsG3m84rrr96zg',
        # 'https://open.spotify.com/playlist/4Ot23cru9zh1c7DFBt0hc8?si=xvrZq_-XQcuB_DY4CM8kTQ',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWTyiBJ6yEqeu?si=78abe6c3c7a040ac',
        # 'https://open.spotify.com/playlist/70nQiAeZNwz72Zp8Ji3DWU?si=47afb31f6a214909',
        # set 2 friends 2
        # 'https://open.spotify.com/playlist/4FwnnxYj9yC9Srguemg55K?si=66d6f39ede7d4127',
        # 'https://open.spotify.com/playlist/5Sj51iMZeEei4Zr6YxhKg0?si=bc7e61c18eb2433b',
        # 'https://open.spotify.com/playlist/2AykYs5NvswgHGpSPeHNML?si=4888f7bb65c846e2',
        # 'https://open.spotify.com/playlist/1PHnod9qiHpMA2LyHfw32h?si=e89c512ba73c4297',
        # 'https://open.spotify.com/playlist/0RGR9cdie1VsSviJMHOTxm?si=30ca7d07e7e04e4b',
        # 'https://open.spotify.com/playlist/57I9L3SMX3Q2g2jZq5E8e9?si=f764ce85c7144e26',
        # 'https://open.spotify.com/playlist/2ZSFPolXxxtP7WDgc1b1ug?si=e8ddb80f93764d81',
        # 'https://open.spotify.com/playlist/6pRmBey0v4G0L45wkFzVHl?si=21408e9dc967435a',
        # 'https://open.spotify.com/playlist/67VdGYC314gd9lRHoPX3TG?si=WYeHIkfwSA-ipaT7ZPz1sQ',
        # 'https://open.spotify.com/playlist/37i9dQZF1EQoqCH7BwIYb7?si=46b8cb1a354142e7',
        # 'https://open.spotify.com/playlist/7pnXMyM4ZHBZ2zZ3qT5T9U?si=08b129ec68a6461d',
        # 'https://open.spotify.com/playlist/40FynzUKesvErz1sUcJHVz?si=BpGDLpHrT5GLUj7rI1D54Q',
        # 'https://open.spotify.com/playlist/0afRrhtWgKTdlxTLg4xyNQ?si=GXU0Ra4iT0WOOS8gKdgimw',
        # 'https://open.spotify.com/playlist/5mtjrZfMHT7oeP8KTQwEuc?si=5OUauQVfS2CIZP7wCdlVTg',
        # 'https://open.spotify.com/playlist/6SXrv07TbW9iik8aOMwLy4?si=bUVqWHziQ7Wr2MmsQZ5UNg',
        # 'https://open.spotify.com/playlist/6DMpzQqLzXZotqKxxxlnhw?si=jhjShETDTK2DTGA4Hv-uHQ',
        # 'https://open.spotify.com/playlist/1fo8W9rhbCJOZSWlssnT7d?si=UiEWndDBRlq8exmmYfs2Dw',
        # 'https://open.spotify.com/playlist/1huPtxdnida06a4pPU1XDU?si=vX9UL_5EQLGotfiee2X8JA',
        # 'https://open.spotify.com/playlist/6n7dOANQwREKLH9NRIu4A7?si=tR_nF2hcQuWcRlFCTEOpYg'
        # set 3 random top 100
        # 'https://open.spotify.com/playlist/37i9dQZF1DXdfOcg1fm0VG?si=1d7e700635a94e54',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXcj60FvXn3Et?si=752ea80b83a7499a',
        # 'https://open.spotify.com/playlist/37i9dQZF1EQn2GRFTFMl2A?si=149979f0714f43a9',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX3bH0P2uDnWA?si=a8bb9fea9d584355',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX9oMffF6CrwU?si=9811a87960174174',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX3z5yKRkYm4P?si=7685fecb4ea849a3',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWSeucCBlpRLm?si=05d9acb0c02b4258',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX0A8zVl7p82B?si=b4a8a3cd2138437e',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX0MuOvUqmxDz?si=679f016e7610445a',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX0MuOvUqmxDz?si=498f5768fdf942b2',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXahjk49z40fT?si=c875803c2ba04d5d',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXan38dNVDdl4?si=db3e813ba76749ea',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXan38dNVDdl4?si=81c9977ab65e4ea1',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX6ZXORV9goKF?si=a90ed6db5e604244',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX8yLfjPY8emY?si=f1e4d23ee3654573',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWUFmUp1ez7YB?si=6b8833e6c3b24851',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX2piJKuRdKIA?si=521ed4b47dc44661',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX2zJGRjWhK7Q?si=3f0b5860d0794f37'
        # set 4 specific spotify top 100 Telugu/Tamil
        # 'https://open.spotify.com/playlist/37i9dQZF1DX6XE7HRLM75P?si=70848e2bd42341f7',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX5ZiKQxiA17z?si=0e5342081ac44796',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWZdcdjsv83gQ?si=60bff3fffc7743f5',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX0TyiNWW7uUQ?si=5ffa9049677d4b2d',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX3VuB7FVwxmc?si=fb269f919d7e4e11',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX1i3hvzHpcQV?si=ed1e0d426ee74d28',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX6XE7HRLM75P?si=223a130b1b5341a0',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX5EbPl0mQHmo?si=70d45497f6344a56',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX5EbPl0mQHmo?si=4431832c8d55490d',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX5VOFoIqmrOV?si=cd1ce137fd6646a4',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX2RftDh9uXrP?si=eac768aee91544ba',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX5ZiKQxiA17z?si=377c2890a8964484',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWUs3YnDlHYW8?si=46a6414cf5844252',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX0YDqnWWzvxD?si=019c2a8972974b79',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX5VOFoIqmrOV?si=1dc752cfcd6346c7',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX7iLHyU2xMyJ?si=4bd858e8d02a4990',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX0YDqnWWzvxD?si=5442f6941fcb47dd',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXbVipT9CLvYD?si=bb83680779944de7',

        # set 5 hindi/ indian classical / Tastemakers?
        # 'https://open.spotify.com/playlist/37i9dQZF1DWXvIf6Zpqk5Q?si=2841fd66e0174377',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXbGl1Tg8AFHx?si=a724d335fb5e4eab',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWUKXFmhEN5MF?si=38735b6169144728',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWX7nMmBhSzhN?si=9eff24063bc1436c',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX0F3lb30Ibi9?si=d6b03a8438b54e51',
        # 'https://open.spotify.com/playlist/71EOlNARIzTqcFXI4tUqsd?si=89449476d4eb4989',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX5rOEFf3Iycd?si=d8cb759321b94828',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXdcRZAcc2QFU?si=88c2f712fb8f4b73',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX3A421vEQpsl?si=b7b068eebd3640de',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWTCoIfIXcr8r?si=88e17ea628a54b59',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWXjoRs40XkRL?si=97fcdda9678948a0',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXbw9rGYPXetO?si=92b2613ecdea4327',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX0Ggu1WtO1dT?si=b485462b82a14c76',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX6QsiGlwQqfw?si=f9f26d1a99894abd',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXdC7eRcOJUCw?si=11bd8414e4454733',
        # 'https://open.spotify.com/playlist/1s2jwVSrmxKxxvvDoMWl32?si=77c3369b869940ab',
        # 'https://open.spotify.com/playlist/3ckau7CzXJzdTbR2ngbia3?si=1a7b674ee2724367',
        # 'https://open.spotify.com/playlist/0TCGmWarQmctdyQIKQXHo2?si=4467d40445284034',
        # # set 6
        # 'https://open.spotify.com/playlist/3ckau7CzXJzdTbR2ngbia3?si=b058459ce3a14640',
        # 'https://open.spotify.com/playlist/4dYgkdqQ7zFy44UQ3Pbsxl?si=62f5f0dc003847d6',
        # 'https://open.spotify.com/playlist/7guZiIqh3BbulKdXnS7vIb?si=e0fd91e818334047',
        # 'https://open.spotify.com/playlist/6cMOxomY5UW0TYHTvuv78N?si=cf2080346ed84d39',
        # 'https://open.spotify.com/playlist/1wkT3U3e6gnsgvi0dqMCEE?si=a3510c0fb1734c04',
        # 'https://open.spotify.com/playlist/2peJPuYDQJMsmEpjqMALnl?si=86b6eb8501e14c8c',
        # 'https://open.spotify.com/playlist/7HQu1GUDVSx64GdCpaB88I?si=6bff89c094fe4c86',
        # 'https://open.spotify.com/playlist/2f6tXtN0XesjONxicAzMIw?si=daed57aed3854bda',
        # 'https://open.spotify.com/playlist/1AHEmHn86cbWR6vOvVq08R?si=5623962b89d04698',
        # 'https://open.spotify.com/playlist/5JdrbiLfh3yupiAByJwEWi?si=d3ead32a241f46f0',
        # 'https://open.spotify.com/playlist/30NUF2CthTzSBEYHmBjfER?si=656c987021e947e9',
        # 'https://open.spotify.com/playlist/0BXZFUhCvDu1cTb1mX01ix?si=94aa1a6950484090',
        # 'https://open.spotify.com/playlist/360efsjHeGOQCxim8gFlBc?si=24b7edd3768e4a04',
        # 'https://open.spotify.com/playlist/4oCdiaZmiKLPpKUHlFjovZ?si=783d2e3c6886450a',
        # 'https://open.spotify.com/playlist/6kXNv8J3HCYztxjOIUzApv?si=9b4ceb76448e47ca',
        # 'https://open.spotify.com/playlist/5lf3ULcD47BmEgIjAgSW2X?si=1d84d76018f9402d',
        # 'https://open.spotify.com/playlist/6yU1l4H28UbyNjgTX1ozHv?si=2d08a7b3f83f4b1b',
        # 'https://open.spotify.com/playlist/0dxnlXUttzpueYSwe74J2c?si=e80ff463a3344334',
        # 'https://open.spotify.com/playlist/5cAz3DR6eFPhxH4ozTKQcx?si=684d5d5a9347494f',
        # # set 7 Taste Maker/ Mexican
        # 'https://open.spotify.com/playlist/4LIb2PKCU2q36oMfA4eNHl?si=85fc8bb5b97b41ee',
        # 'https://open.spotify.com/playlist/78RB8LnUdj52Z5LVX9gEc7?si=9404eeb6c4fe4b93',
        # 'https://open.spotify.com/playlist/3h2IgKtlJYBhfbxPRuHMEG?si=9d1458bb086a4cc6',
        # 'https://open.spotify.com/playlist/60xWeQ4ak8TFjjcvYyjn0x?si=69cc86e24a674aa5',
        # 'https://open.spotify.com/playlist/0Xb9zZnc2MHkRocj5kqPWU?si=9f85dd1d528a4dfa',
        # 'https://open.spotify.com/playlist/1QBiXlEscYkB1YauNmOcUS?si=a8515dd53e724a38',
        # 'https://open.spotify.com/playlist/7A2YimOfIrmAWkCeSIY8Rq?si=8e09382662a646c4',
        # 'https://open.spotify.com/playlist/4QuJ2DbcTe7R8lzqfNXz7v?si=437f8491d6264501',
        # 'https://open.spotify.com/playlist/6Qf2sXTjlH3HH30Ijo6AUp?si=45e448713fef4f70',
        # 'https://open.spotify.com/playlist/1x6GrB4XNiHiMCA2ADWjUZ?si=1066793efcf0441e',
        # 'https://open.spotify.com/playlist/6dm9jZ2p8iGGTLre7nY4hf?si=e5e2dd9a20434b50',
        # 'https://open.spotify.com/playlist/56cov9xwW00rgProJEHERp?si=1b38a3d82c3340bc',
        # 'https://open.spotify.com/playlist/49MqbWUSYMpxaUzog7MDqG?si=9324d0a4c5274356',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXdC7eRcOJUCw?si=e8c9048ce6624850',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX53wq0WYtg5L?si=13cf5a52341b4055',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWT1J5CAuMUxr?si=cf87cb4ca67940e4',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX6EM3TTcpK4b?si=0108ccaaa928417d',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWZLL3REk8t1E?si=a36d9d8e06ff4c90',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWTyvco9C4Og0?si=71679d7d25d048f9',
        # # set 8 more mexican/indo pacific
        # 'https://open.spotify.com/playlist/37i9dQZF1DWTyvco9C4Og0?si=cb9ce2f83eec4476',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWZQGZ7yvpH00?si=570de38ce0414486',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWVPkWIRD16c8?si=769507a3f03c4f1b',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXd6QWbEewZmM?si=0630961b11cd4a4d',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWUuQG5KIiBcn?si=5916f5d6eff54fdf',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXdcb8m3Nt9YW?si=26bc930042794cc1',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXaRkwbkfuyXo?si=28d1860b273144cd',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWU43UtgmzCjN?si=8fa8c563e5d84f53',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXdDoYRQ4LfQJ?si=c5ff2dc9c3444118',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWWhMyyrqZlaY?si=b661a9ea97e241bc',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX5471jEhaq8X?si=92d1fe8fcb8149c2',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX2shzuwwKw0y?si=0fd3f9cf58e3452c',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWU24O1KPl8Ai?si=18387682b65149a3',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWU24O1KPl8Ai?si=4b1e420ac44c4bd5',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWVFEIJKF33Nk?si=352a9c6492ef438e',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXaBIwevZ5Lux?si=80dcea62047b42db',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX2b9oUJWXOaZ?si=597e148e7058429e',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWSzuTydUOXRi?si=7e377bec89444300',
        # # set 9 cont/ pride / punjabi
        'https://open.spotify.com/playlist/37i9dQZF1DX7eWGbr5dV3X?si=ccc3190869ff4355',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWY0N3eAirRjZ?si=aa15af6dda574563',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX1kZBqCJkwLM?si=34f0e9db40284f6a',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX6KwoIt0pZYP?si=c874af36219d4d71',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX6KwoIt0pZYP?si=1152f691dba44d21',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXcPGEMJEYxNg?si=defdedb297fd4fd3',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX5IOhx43PGIa?si=b38da4f7b95c448d',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXe7IKgrJ3ej1?si=ff069c6564ed4bb2',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX2Ntl47Kk60U?si=243094c870b5436a',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWWKWmC5fAz6a?si=0083dec58562447c',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX5KARSfd7WcM?si=fc8a63acc1d543c2',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX4YipRSmIneQ?si=dc49b2360ea94d07',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX1SbnWqcjJBz?si=e181dbb83ea844bf',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX0g1UNPczC9q?si=639d4ca07b034e02',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX7YE2tQ4q86h?si=da2eac243a534457',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWW2hj3ZtMbuO?si=1530a4715b39408d',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX9WDOjoils23?si=c9560a0e9a4f43cd',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWUrsIisHoG3z?si=defe4f53127b432a',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX1ZY1DoggQaf?si=3103ee7f54d240d3',
        # # set 10 black
        # 'https://open.spotify.com/playlist/37i9dQZF1DXbrVWoy56uMj?si=994301a6eb204c3b',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX8qj1nSNkJqB?si=4e35325aa27f4578',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWStljCmevj7t?si=8eae8861dae7485a',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWXVJK4aT7pmk?si=aa3d4a1d6ccc4474',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX5baCFRgbF3x?si=7f59a690afee4c70',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX5cZuAHLNjGz?si=c38b51c811ff44be',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX7OIddoQVdRt?si=13eb564089a14fd9',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXaXDsfv6nvZ5?si=35c35a41ff6a47b1',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXaPeYMCDRQeg?si=c77a41fe1fd340ab',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX28ZIZjK8SGt?si=1e83b7802d4f4d8d',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWYNNUgvFqsgZ?si=25a93a0e09114e03',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWSIO2QWRavWZ?si=d4f0ae5f88d046cd',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX7DCJxqVk5NA?si=e1d3addbc6944666',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX2r0FByV5U4C?si=af41a53f5cc14849',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWWAqc46ZJdZf?si=b150a1cc406545ea',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWViXqZVTGO3Z?si=f1770bcdddc943d8',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX2eGcUpDGev2?si=ef64caed84414a60',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX82qPOvdCxxq?si=0a5912b73b8b4faa',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX7Bi6W3YuUlA?si=89d4488c669849f4',
        # # set 11
        # 'https://open.spotify.com/playlist/37i9dQZF1DX2sJGkrvCPgm?si=a9185463c22f4bf3',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX9lAYMw7KoAO?si=1f838d5f0fbf4842',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX9lAYMw7KoAO?si=ef648c47afdb468c',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX0IXk7nnh7Jx?si=8a0de5cc0a1144e4',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXaky0wMRgvaj?si=2b0e10ce45304942',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX3ZaylsK87YU?si=b0204bdd104349dd',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX1tZzam7CfKP?si=ab547a86e6e7409c',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX4WgZiuR77Ef?si=c972cb8d55ac43c3',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX23YPJntYMnh?si=906a73e80f164c29',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX8f5qTGj8FYl?si=e67dbe4e1bbc44b6',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWTTiDL22vZpS?si=3149a1bed078475f',
        # 'https://open.spotify.com/playlist/37i9dQZF1DXdb5FEvfgsH9?si=8a56290688b84a3b',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWUcRrhkfhG22?si=bb868aa66c4a491c',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX6drTZKzZwSo?si=197b252ce03f4e7c',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWZgauS5j6pMv?si=cbb55217d3284837',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX2aCk0vzzaZQ?si=202b4afe8b324689',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWUajed02NzWR?si=6a9a3cb27c314362',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX9dX3aBjsxqd?si=83e53e958fe44aa6',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX7dzHXrANAir?si=3bdb8b6e93c24a6b',
        # # set 12
        # 'https://open.spotify.com/playlist/37i9dQZF1DX1ACGg8vzTNZ?si=7cb2e9f24b5a4c5f',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX4s3V2rTswzO?si=2614353c2fe346bd',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWXi6GqUgtvam?si=7bb7c9bbed6f404d',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWW7gj0FcGEx6?si=f14739b4837c4420',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWXtBjoO4Thyy?si=fae036876b9f4104',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX1jDTenPbqLo?si=13ee79b5c77040f9',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWXjj6kdiviS0?si=3fe2256e7ca744a5',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX7Ope5RE4ePQ?si=98d19b2f96b64dc8',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX561TxkFttR4?si=210cd601e956429a',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX7GTqMQDhOum?si=9aad033b35d04b33',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWV2mRphxMWjR?si=0b7944708685455a',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWXkVfVmXHa7l?si=853ff8f20e244f45',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX01AtpaIYjQE?si=98e65e39e63b477c',
        # 'https://open.spotify.com/playlist/37i9dQZF1DZ06evO02uS96?si=f63f63d9bb1a4dd5',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWZipvLjDtZYe?si=99a2257982194219',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX1PCNEM81iS6?si=c7bf6101c1a54f9a',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWUxyGpMcGpaI?si=19fdec2d3e7345bb',
        # 'https://open.spotify.com/playlist/37i9dQZF1DWT8aqnwgRt92?si=4b5c225e08e24f7e',
        # 'https://open.spotify.com/playlist/37i9dQZF1DX6uQZwMgKlWb?si=c90dffccf05b4072',

    ]
    get_track_data(playlists)


if __name__ == '__main__':
    main()
