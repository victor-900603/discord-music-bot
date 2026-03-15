import yt_dlp
import asyncio
import aiohttp
import logging

logger = logging.getLogger("app")


async def download_audio(url: str) -> dict:
    """
    從 YouTube URL 提取音訊資訊（不下載檔案）
    
    :param url: YouTube 影片網址
    :return: 歌曲資訊字典，包含 source, title, webpage_url, thumbnail, channel, channel_url
    :raises Exception: 當無法提取音訊資訊時
    """
    def extract():
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch',
            'extract_flat': False,
            'force_generic_extractor': False,
            'allow_unplayable_formats': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info is None:
                raise Exception(f"無法提取音訊資訊: {url}")
            if 'entries' in info:
                info = info['entries'][0]  # 針對播放清單
            return {
                'source': info['url'],
                'title': info.get('title', 'Unknown'),
                'webpage_url': info.get('webpage_url', url),
                'thumbnail': info.get('thumbnail', ''),
                'channel': info.get('channel', 'Unknown'),
                'channel_url': info.get('channel_url', '')
            }
    
    try:
        return await asyncio.to_thread(extract)
    except Exception as e:
        logger.error(f"下載音訊失敗: {url}, 錯誤: {e}")
        raise


async def search_youtube(keyword: str) -> list[dict]:
    async def post_api(pl):
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
        async with aiohttp.ClientSession() as session:
            async with session.post( 
                'https://www.youtube.com/youtubei/v1/search',
                params=params,
                headers=headers,
                json=json_data,
            ) as response:
                response = await response.json() 
                
            content = response['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
            
            results = content[0]['itemSectionRenderer']['contents']
            next_token = content[1]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']

        return results, next_token

    def parse_results(results, data):
        for r in results:
            if 'videoRenderer' in r:
                info = r['videoRenderer']

                d = {
                    'videoId': info['videoId'],
                    'title': info['title']['runs'][0]['text'],
                    'thumbnail': info['thumbnail']['thumbnails'][0]['url'],
                    'length': info['lengthText']['simpleText'],
                    # 'viewCount': info['viewCountText']['simpleText'],
                    'channel': info['ownerText']['runs'][0]['text']
                }
                data.append(d)

    try:
        data = []
        results, next_token = await post_api(keyword)
        parse_results(results, data)
        return data
    except Exception as e:
        logger.error(f"搜尋 YouTube 失敗: {keyword}, 錯誤: {e}")
        raise



if __name__ == '__main__':
    print(asyncio.run(download_audio('https://www.youtube.com/watch?v=Jv3zvWZlXkk')))
    # print(asyncio.run(search_youtube('五月天')))
