import time
import requests
import os
class aparat_paylist_downloader:
    def __init__(self):
        pass
    def __call__(self):
        pass
        
    def fetch_list(self,add_to_idm=True):
        listId=input(prompt="Enter Channel ID ")
        self.channel_id=listId
        print('-'*40)
        list_url='https://www.aparat.com/api/fa/v1/video/playlist/one/playlist_id/{}'.format(listId)
        response=requests.get(list_url)
        listpage_json = response.json()
        url_template='https://www.aparat.com/api/fa/v1/video/video/show/videohash/{}?pr=1&mf=1&referer=direct'
        video_urls=[]
        for item in range(len(listpage_json['included'])):
            try:
                video_urls.append(url_template.format(listpage_json['included'][item]['attributes']['uid']))
            except:
                pass
            
        self.links=[]
        self.titles=[]
        
        for url in video_urls:
            response=requests.get(url)
            videoPage_json=response.json()
            x=videoPage_json['data']['attributes']['file_link_all']
            self.titles.append(videoPage_json['data']['attributes']['title'])
            print(videoPage_json['data']['attributes']['title'], " is found!")
            self.links.extend(x[len(x)-1]['urls'])
        print('-'*40,"\n",len(self.titles), " video urls extracted!")
        if add_to_idm:
            add_to_IDM()
    
    def add_to_IDM(self,delay=.3):
        stream = os.popen('path')
        output = stream.read()
        if output.find("Internet Download Manager")==-1:
            print("You need to add IDM directory to your path variable by !path 'path\\to\\IDM';%PATH%")
        else:
            print('-'*40)
            for index in range(len(self.links)):
                clean_name=str(self.titles[index]).replace("\\","-").replace("/","-").replace("*","-").replace("!","-")
                cmd='idman /d {url} /f \"{fname}\" /a'.format(url=self.links[index],fname=clean_name+".mp4")
                time.sleep(delay)
                os.popen(cmd)
        print('Probably ',len(self.titles), " videos were added to IDM")

