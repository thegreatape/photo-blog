import os, urllib2, time, re
from datetime import datetime
from BeautifulSoup import BeautifulStoneSoup

content = urllib2.urlopen('http://api.flickr.com/services/feeds/photos_public.gne?id=63503896@N00&tags=blog&lang=en-us&format=rss_200')
soup = BeautifulStoneSoup(content)
posts = os.listdir('_posts')
for item in soup('item'):
    datestr = re.sub(' [-\+]\d+$', '', item.pubdate.contents[0]) #strptime doesn't do timezones well :-(
    photo_date = datetime(*time.strptime(datestr, '%a, %d %b %Y %H:%M:%S')[:6])
    safe_title = re.sub(r'\s|/', '-', item.title.contents[0].lower());
    post_title = '%s-%s.markdown' % (photo_date.strftime('%Y-%m-%d'), safe_title)
    if not post_title in posts:
        print "creating new entry for %s" % item.title.contents[0]
        thumb = re.sub(r'(.*)_s.jpg', '\\1.jpg', item('media:thumbnail')[0]['url'])
        description = item('media:description')
        description = description[0].contents[0] if description else ''
        description = re.sub('&lt;[^&]*&gt;', '', description).replace('&amp;','&')
        post = ['---\n',
                'title: %s \n' % item.title.contents[0],
                'img: %s \n' % thumb,
                'img_link: %s \n' % item.link.contents[0],
                'date: %s \n' % photo_date.strftime('%Y-%m-%dT%H:%M:%S-05:00'),
                '---\n',
                description]
        open('_posts/%s' % post_title, 'w').writelines(post)

