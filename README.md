# YouTube Downloader API (yt-dlp) for Vercel

## Usage

This API allows you to:

- Search YouTube videos (top 10 results)
- List available formats for a selected video
- "Download" a chosen format to the server temporary folder (demo purpose)

## Endpoints

- `GET /?q=SEARCH_TERM`  
Returns top 10 YouTube search results (title, ID, url)

- `GET /?q=SEARCH_TERM&choice=VIDEO_NUMBER`  
Returns available formats for the selected video (video + audio, audio only)

- `GET /?q=SEARCH_TERM&choice=VIDEO_NUMBER&format=FORMAT_ID`  
Downloads the selected format (server temp storage)

## Deployment

- Install Vercel CLI: `npm i -g vercel`
- Login: `vercel login`
- Deploy: `vercel` (from project folder)
- Access your deployment URL to use the API.
