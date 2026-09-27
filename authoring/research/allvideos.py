"""Fetch every video (id, title, published text, view text) from a channel tab, following continuations."""
import json, re, sys, urllib.request, time
sys.path.insert(0, '.')
from yt import initial_data, walk, text

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'

def get(url, data=None):
    req = urllib.request.Request(url, data=data, headers={'User-Agent': UA, 'Accept-Language': 'en-US', 'Cookie': 'CONSENT=YES+1', 'Content-Type': 'application/json'})
    return urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'ignore')

def grid_token(obj):
    """The continuation for the video grid: inside richGridRenderer or appended continuationItems."""
    for d in walk(obj):
        container = None
        if 'richGridRenderer' in d: container = d['richGridRenderer'].get('contents', [])
        elif 'appendContinuationItemsAction' in d: container = d['appendContinuationItemsAction'].get('continuationItems', [])
        elif 'reloadContinuationItemsCommand' in d: container = d['reloadContinuationItemsCommand'].get('continuationItems', [])
        if container:
            for item in container:
                if 'continuationItemRenderer' in item:
                    for x in walk(item):
                        if 'continuationCommand' in x: return x['continuationCommand']['token']
    return None

def items_from(obj):
    vids, token = [], grid_token(obj)
    for d in walk(obj):
        if 'videoRenderer' in d or 'gridVideoRenderer' in d:
            r = d.get('videoRenderer') or d.get('gridVideoRenderer')
            vids.append({'id': r['videoId'], 'title': text(r.get('title')), 'published': text(r.get('publishedTimeText')), 'views': text(r.get('viewCountText')), 'length': text(r.get('lengthText'))})
        if 'shortsLockupViewModel' in d:
            sv = d['shortsLockupViewModel']
            vid = None
            for x in walk(sv):
                if 'reelWatchEndpoint' in x: vid = x['reelWatchEndpoint'].get('videoId')
            title = text(sv.get('overlayMetadata', {}).get('primaryText', {}))
            if vid: vids.append({'id': vid, 'title': title, 'short': True})
        if 'lockupViewModel' in d and d['lockupViewModel'].get('contentType') == 'LOCKUP_CONTENT_TYPE_VIDEO':
            lv = d['lockupViewModel']
            vids.append({'id': lv['contentId'], 'title': text(lv.get('metadata', {}).get('lockupMetadataViewModel', {}).get('title', {}))})
    return vids, token

def channel(handle, tab):
    html = get(f'https://www.youtube.com/@{handle}/{tab}')
    key = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', html).group(1)
    ver = re.search(r'"INNERTUBE_CLIENT_VERSION":"([^"]+)"', html).group(1)
    vids, token = items_from(initial_data(html))
    pages = 1
    while token and pages < 200:
        body = json.dumps({'context': {'client': {'clientName': 'WEB', 'clientVersion': ver, 'hl': 'en'}}, 'continuation': token}).encode()
        data = json.loads(get(f'https://www.youtube.com/youtubei/v1/browse?key={key}&prettyPrint=false', body))
        more, token = items_from(data)
        vids += more; pages += 1
        time.sleep(0.3)
    seen, out = set(), []
    for v in vids:
        if v['id'] not in seen: seen.add(v['id']); out.append(v)
    return out

if __name__ == '__main__':
    handle = sys.argv[1]
    result = {}
    for tab in ['videos', 'shorts', 'streams']:
        try:
            result[tab] = channel(handle, tab)
        except Exception as e:
            result[tab] = []; print(f'{handle}/{tab}: {e}', file=sys.stderr)
    json.dump(result, open(f'{handle}.json', 'w'), indent=1, ensure_ascii=False)
    print(handle, {k: len(v) for k, v in result.items()})
