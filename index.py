import json
from yt_dlp import YoutubeDL

def handler(event, context):
    query = event.get('queryStringParameters', {}) or {}
    search_term = query.get('q')
    video_choice = query.get('choice')
    format_id = query.get('format')

    if not search_term:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing query parameter 'q' for search term."})
        }

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'default_search': 'ytsearch10',
        'noplaylist': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_term, download=False)
        videos = info.get('entries', [])

    if not videos:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "No videos found for the query."})
        }

    # Return top 10 results if no video choice yet
    if not video_choice:
        results = []
        for i, v in enumerate(videos):
            results.append({
                "index": i + 1,
                "title": v['title'],
                "id": v['id'],
                "duration_seconds": v['duration'],
                "url": v['webpage_url']
            })
        return {
            "statusCode": 200,
            "body": json.dumps({"search_results": results})
        }

    # Validate selected video choice
    try:
        video_idx = int(video_choice) - 1
        selected_video = videos[video_idx]
    except (IndexError, ValueError):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid video selection."})
        }

    video_url = selected_video['webpage_url']

    # Return available formats if no specific format requested yet
    if not format_id:
        with YoutubeDL({'quiet': True, 'noplaylist': True}) as ydl:
            video_info = ydl.extract_info(video_url, download=False)
            formats = video_info.get('formats', [])

            video_audio_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') != 'none']
            audio_only_formats = [f for f in formats if f.get('vcodec') == 'none' and f.get('acodec') != 'none']

            fmt_list = {
                "video_audio": [{
                    "format_id": f['format_id'],
                    "ext": f['ext'],
                    "resolution": f.get('resolution', ''),
                    "fps": f.get('fps', ''),
                    "filesize": f.get('filesize') or "Unknown"
                } for f in video_audio_formats],

                "audio_only": [{
                    "format_id": f['format_id'],
                    "ext": f['ext'],
                    "abr": f.get('abr', ''),
                    "filesize": f.get('filesize') or "Unknown"
                } for f in audio_only_formats]
            }

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "title": selected_video['title'],
                    "formats": fmt_list
                })
            }

    # Download format - note: on Vercel we can't serve the file directly, so just simulate download
    ydl_opts = {
        'format': format_id,
        'outtmpl': '/tmp/%(title)s.%(ext)s',
        'quiet': True,
        'merge_output_format': 'mp4',
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Downloaded '{selected_video['title']}' format {format_id} to server's temporary storage."
        })
    }
