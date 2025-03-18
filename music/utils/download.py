import yt_dlp
import asyncio
import requests


def download_audio(url):
    """使用 yt-dlp 下載音頻"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch',
        'extract_flat': False,
        'force_generic_extractor': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            info = info['entries'][0]  # 針對播放清單
        return {
            'source': info['url'],
            'title': info['title'],
            'webpage_url': info['webpage_url'],
            'thumbnail': info['thumbnail'],
            'channel': info['channel'],
            'channel_url': info['channel_url']
        }
    
def search_and_download(keyword):
    def postApi(pl):
        added_payload = {'query': pl} 

        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }
        params = {
            'prettyPrint': 'false',
        }
        json_data = {
            'context': {
                'client': {
                    'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36,gzip(gfe)',
                    'clientName': 'WEB',
                    'clientVersion': '2.20240606.06.00',
                    'timeZone': 'Asia/Taipei',
                },
                'user': {
                    'lockedSafetyMode': False,
                },
                'request': {
                    'useSsl': True,
                    'internalExperimentFlags': [],
                    'consistencyTokenJars': [],
                },
            },
        }
        json_data.update(added_payload)
        response = requests.post(
            'https://www.youtube.com/youtubei/v1/search',
            params=params,
            headers=headers,
            json=json_data,
        )
        content = response.json()['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
        
        results = content[0]['itemSectionRenderer']['contents']
        next_token = content[1]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']

        return results, next_token

    def parseResults(results, data):
        for r in results:
            if 'videoRenderer' in r:
                info = r['videoRenderer']
                d = {
                    'videoId': info['videoId'],
                    'title': info['title']['runs'][0]['text'],
                    # 'length': info['lengthText']['simpleText'],
                    # 'viewCount': info['viewCountText']['simpleText'],
                    # 'channel': info['ownerText']['runs'][0]['text']
                }
                data.append(d)

    data = []
    results, next_token = postApi(keyword)
    parseResults(results, data)


    return data

if __name__ == '__main__':
    # asyncio.run(download_audio('https://www.youtube.com/watch?v=Jv3zvWZlXkk'))
    # print((search_and_download('五月天')))
    print(download_audio('https://youtu.be/d9ktAt-Gg2k?si=CIYG-A35KogrtH-4'))
