import os, urllib2, time, re
from datetime import datetime
from BeautifulSoup import BeautifulStoneSoup

content = urllib2.urlopen('http://api.flickr.com/services/feeds/photos_public.gne?id=63503896@N00&lang=en-us&format=rss_200')
soup = BeautifulStoneSoup(content)
last_post = max(os.listdir('_posts'))
last_date = datetime(*time.strptime(re.match(r'(\d{4}-\d{1,2}-\d{1,2}).*', last_post).group(1), '%Y-%m-%d')[:3])
for item in soup('item'):
    datestr = re.sub(' [-\+]\d+$', '', item.pubdate.contents[0]) #strptime doesn't do timezones well :-(
    photo_date = datetime(*time.strptime(datestr, '%a, %d %b %Y %H:%M:%S')[:6])
    if photo_date >= last_date:
        thumb = re.sub(r'(.*)_s.jpg', '\\1.jpg', item('media:thumbnail')[0]['url'])
        description = item('media:description')
        description = description[0].contents[0] if description else ''
        description = re.sub('&lt;[^&]*&gt;', '', description).replace('&amp;','&')
        post = ['---\n',
                'title: %s \n' % item.title.contents[0],
                'img: %s \n' % thumb,
                'img_link: %s \n' % item.link.contents[0],
                '---\n',
                description]
        safe_title = re.sub(r'\s', '-', item.title.contents[0].lower());
        open('_posts/%s-%s.markdown' % (photo_date.strftime('%Y-%m-%d'), safe_title), 'w').writelines(post)
