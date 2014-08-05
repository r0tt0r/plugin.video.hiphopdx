# -*- coding: utf-8 -*-
#hiphopdx - by r0tt 2014. V0.0.1

import urllib,urllib2,re,string,xbmcaddon,xbmcplugin,xbmcgui,socket,sys,os

if sys.version_info < (2, 7):
    import json as simplejson
else:
    import simplejson

timeout = 25
socket.setdefaulttimeout(timeout)
pluginhandle = int(sys.argv[1])

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
 
cache = StorageServer.StorageServer("ArtworkDownloader",24)
addon = xbmcaddon.Addon('plugin.video.hiphopdx')
scriptpath = addon.getAddonInfo('path')
ua='Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/17.0 Firefox/17.0'
logo='/icon.png'
url='http://www.hiphopdx.com/index/videos/p.1'
        
def INDEX(url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', ua)
		response = urllib2.urlopen(req)
		link = response.read()
		response.close()
		url=re.sub("/p.(\d{0,9999})", "/p.", url)
		title=re.compile('alt=\"(.+? - .+?)\"\/><\/a>').findall(link)
		thumb=re.compile('							 src=\"(.+?)\"').findall(link)
		pagenext=re.compile('videos/p.(.+?)" class="uni-link right').findall(link)
		pagenext=int(str(pagenext).strip("'[]'"))
		pageurl=url + str(pagenext)
		addDir("Next Page "+str(pagenext), pageurl, 1, "")
		page1=pagenext + 1
		page10=pagenext + 10
		page100=pagenext + 100 
		pageurl10=url + str(page10)
		pageurl100=url + str(page100)
		title=re.compile('alt=\"(.+? - .+?)\"\/><\/a>').findall(link)
		thumb=re.compile('							 src=\"(.+?)\"').findall(link)
		vid=re.compile('<h3><a href=\"(.+?)\">').findall(link)
		vid=['http://www.hiphopdx.com'+li for li in vid]
		match=zip(title, vid, thumb)
		for name,url,thumb in match:
			name = str(name).replace('"','').replace('&#xfc;','ö').replace('&#xfc;','ü').replace(',','').replace('(','').replace(')','').replace("'","").replace('\\xc3\\xb6','ö').replace('\\xc3\\xbc','ü').replace('\\xc3\\xa4','ä').replace('\\xfc','ü').replace('\\xf6','ö').replace('\\xc3\\xa1','à').replace('\\xe4','ä').replace('&amp;','&').replace("&#039;","'").replace("&quot;",'"')
			addDir(name,url,2,thumb)
		addDir("Next 10 Pages "+str(page10), pageurl10, 1, "")
		addDir("Next 100 Pages "+str(page100), pageurl100, 1, "")
		xbmcplugin.endOfDirectory(pluginhandle)      

def VIDEOLINKS(url,name):
		req = urllib2.Request(url)
		req.add_header('User-Agent', ua)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		match1=str(re.compile('value="http://(.+?)/video').findall(link)).strip("['']")
		match2=str(re.compile('//(.+?)/embed/').findall(link)).strip("['']")
		match21=str(re.compile('value=\"http://(.+?)/v/').findall(link)).strip("['']")
		match3=str(re.compile('src=\"//(.+?)/video/').findall(link)).strip("['']")
		match4=str(re.compile('src=\"http\:\/\/(.+?)\/embed\/video\/').findall(link)).strip("['']")
		match41=str(re.compile('value="http://(.+?)/swf/').findall(link)).strip("['']")
		match5=str(re.compile('src=\'http://(.+?)/embed/').findall(link)).strip("['']")
		match51=str(re.compile('data="http://(.+?)/movie/').findall(link)).strip("['']")
		match6=str(re.compile('flv=http%3a//(.+?)/fmp/').findall(link)).strip("['']")
		match7=str(re.compile('\" src=\"http:\/\/(.+?)\/embed_iframe\/').findall(link)).strip("['']")
		if match1 == 'www.worldstarhiphop.com':
			match=str(re.compile('value=\"(.+?)\"></param><param name=\"allowFullScreen').findall(link)).strip("['']")
			r=urllib2.urlopen(match)
			r2=r.geturl()
			url=str(re.compile('&file=(.+?)&').findall(r2)).strip("['']")
			addLink(name,url,'')
			xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
		if match2 or match21 == 'www.youtube.com':
			match=str(re.compile('/embed/(.+?)\"').findall(link)).strip("['']")
			if match == '':
				match=str(re.compile('value=\"http://www.youtube.com/v/(.+?)&amp;').findall(link)).strip("['']")
				url='plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=%s' % match
				addLink(name,url,'')
				xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
			else:	
				url='plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=%s' % match
				addLink(name,url,'')
				xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
		if match3 == 'player.vimeo.com':
			match=str(re.compile('iframe src=\"//player.vimeo.com/video/(.+?)\"').findall(link)).strip("['']")
			url='plugin://plugin.video.vimeo/?action=play_video&videoid=%s' % match
			addLink(name,url,'')
			xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
		if match4 or match41 == 'www.dailymotion.com':
			match=str(re.compile('/embed/video/(.+?)\"></iframe>').findall(link)).strip("['']")
			if match == '':
				match=str(re.compile('value=\"http://www.dailymotion.com/swf/(.+?)\">').findall(link)).strip("['']")
				url='plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % match
				xbmc.Player().play(url)
				addLink(name,url,'')
			else:
				url='plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % match
				xbmc.Player().play(url)
				addLink(name,url,'')
		if match5 or match51 == 'www.myvideo.de':
			match=str(re.compile('/embed/(.+?)\'').findall(link)).strip("['']")
			if match == '':
				match=str(re.compile('/movie/(.+?)\" type=').findall(link)).strip("['']")
				url='plugin://plugin.video.myvideo_de/video/%s/play' % match
				addLink(name,url,'')
				xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
			else:
				url='plugin://plugin.video.myvideo_de/video/%s/play' % match
				addLink(name,url,'')
				xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
		if match6 == 'blazinstreetz.com':
			url=str(re.compile('value="flv=(.+?)\"').findall(link)).strip("['']").replace('%20',' ').replace('%3a',':')
			addLink(name,url,'')
			xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
		if match7 == 'cms.springboardplatform.com':
			match=str(re.compile('\" src=\"http:\/\/cms.springboardplatform.com\/embed_iframe\/(.+?)\"').findall(link)).strip("['']")
			url='http://cms.springboardplatform.com/embed_iframe/' + match
			req = urllib2.Request(url)
			req.add_header('User-Agent', ua)
			response = urllib2.urlopen(req)
			link=response.read()
			response.close()
			url=str(re.compile('<meta property=\"og:video\" content=\"(.+?)\" />').findall(link)).strip("['']")
			addLink(name,url,'')
			xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
		xbmcplugin.endOfDirectory(pluginhandle)
    
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable','true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
                  
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
		url='http://www.hiphopdx.com/index/videos/p.1'
		print ""
		INDEX(url)
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
