import yt_dlp
import asyncio
import aiohttp


async def download_audio(url):
    def extract():
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
    
    return await asyncio.to_thread(extract)
    
async def search_yotube(keyword):
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

    data = []
    results, next_token = await post_api(keyword)
    parse_results(results, data)

    return data

if __name__ == '__main__':
    print(asyncio.run(download_audio('https://www.youtube.com/watch?v=Jv3zvWZlXkk')))
    # print(asyncio.run(search_yotube('五月天')))
