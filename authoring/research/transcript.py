"""Fetch a YouTube video's transcript (caption track) as [(startSeconds, text)]. Cached on disk."""
import json, os, re, sys, urllib.request, html as htmlmod, xml.etree.ElementTree as ET
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'transcripts')
os.makedirs(CACHE, exist_ok=True)

def get(url, data=None, headers=None):
    h = {'User-Agent': UA, 'Accept-Language': 'en-US', 'Cookie': 'CONSENT=YES+1'}
    h.update(headers or {})
    return urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h), timeout=30).read().decode('utf-8', 'ignore')

def transcript(video_id):
    """[(start seconds, text)] from YouTube's player API (ANDROID client), English track;
    human captions preferred over auto-generated (asr). Cached in transcripts/."""
    path = os.path.join(CACHE, video_id + '.json')
    if os.path.exists(path):
        return json.load(open(path))
    lines = []
    try:
        body = json.dumps({'context': {'client': {'clientName': 'ANDROID', 'clientVersion': '20.10.38', 'androidSdkVersion': 30, 'hl': 'en'}}, 'videoId': video_id}).encode()
        pr = json.loads(get('https://www.youtube.com/youtubei/v1/player?prettyPrint=false', body, {'Content-Type': 'application/json'}))
        tracks = pr.get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get('captionTracks', [])
        en = [t for t in tracks if t.get('languageCode', '').split('-')[0] == 'en']
        track = next((t for t in en if t.get('kind') != 'asr'), None) or (en[0] if en else None)
        if track:
            root = ET.fromstring(get(track['baseUrl']))
            for p in root.iter('p'):
                txt = ''.join(p.itertext()).strip()
                if txt: lines.append((int(p.get('t', '0')) / 1000, htmlmod.unescape(txt).replace('\n', ' ')))
            if not lines:
                for t in root.iter('text'):
                    if t.text: lines.append((float(t.get('start', '0')), htmlmod.unescape(t.text).replace('\n', ' ')))
    except Exception as e:
        print(f'{video_id}: {e}', file=sys.stderr)
    json.dump(lines, open(path, 'w'))
    return lines

if __name__ == '__main__':
    t = transcript(sys.argv[1])
    print(len(t), 'lines')
    for s, x in t[:5]: print(int(s), x)
