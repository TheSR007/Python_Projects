import requests, sys, re
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from functools import partial

#used to play iframe in python(built in browser)
from PyQt5.QtWebEngineWidgets import QWebEngineView

#uncomment these and adjust if you want to use browser to play the videos
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
# options = Options()
# if brave_path:
#     options.binary_location = brave_path
# options.add_argument("--incognito --enable-chrome-browser-cloud-management")
# driver = webdriver.Chrome(options=options)
# driver.get(url)   #must always keep this tab open


#uncomment these if you want to use vlc
# import subprocess

# # Path to VLC executable
# vlc_path = "C:/Program Files/VideoLAN/VLC/vlc.exe"

# def vlc_play(url):
#     command = [vlc_path, url]
#     subprocess.Popen(command)


url = 'Website_Base_Url'

# from urllib.parse import urlparse  #urlpasrse can parse specific parts of url, mainly used to get specific part of the url like full url with path or quesries etc

# example
# url = 'https://www.example.com/path/to/page?query=123#section'
# parsed_url = urlparse(url)
# print("Scheme:", parsed_url.scheme)
# print("Netloc:", parsed_url.netloc)
# print("Path:", parsed_url.path)
# print("Query:", parsed_url.query)
# print("Fragment:", parsed_url.fragment)

# output
# Scheme: https
# Netloc: www.example.com
# Path: /path/to/page
# Query: query=123
# Fragment: section


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.filter_buttons = {}
        self.initUI()

    def initUI(self):
        self.Hlayout = QHBoxLayout()
        self.match = []
        self.nexturl = []
        self.previousurl = []
        self.filtered = False
        self.Vlayout = QVBoxLayout()
        self.layout =  QHBoxLayout()
        self.list_widget = QListWidget()

        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.black)
        palette.setColor(self.foregroundRole(), Qt.white)
        self.setPalette(palette)
        self.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: white;
                border: none;
            }
            QListWidget {
                background-color: #333;
                color: white;
                border: none;
            }
            QListWidget::item {
                background-color: #222;
            }
            QListWidget::item:selected {
                background-color: #444;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        #Most of the fetures will be commented out as they are website specific only using the default name, img and url and play

        # directories = ['category', 'tags', 'filter']
        # for iteam in directories:
        #     self.addButton(iteam)   #adding catgory, tags, ad filter button 

        # self.filter = ['latest', 'most-viewed', 'popular', 'longest', 'random']
        # for filt in self.filter:
        #     self.addButton(filt, hide=True, filter=True)    #filter buttons toggle on the filter clicked
        

        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_widget.itemClicked.connect(self.onListItemClicked)
        self.list_widget.itemEntered.connect(self.onListItemClicked)
        self.Vlayout.addWidget(self.list_widget)

        # self.addButton("Next",hide=True)  #next button for linear structure webpage
        # self.addButton("Previous",hide=True) #previous button for linear structure webpage

        self.layout.addLayout(self.Vlayout)

        self.image_label = QLabel() #to show the img of videos
        self.image_label.setFixedSize(400, 400)
        self.Hlayout.addWidget(self.image_label)

        # self.Gbutton =  QPushButton("GO")   #to go in that link
        # self.Gbutton.clicked.connect(self.GO)
        # self.Gbutton.setFixedSize(50,50)
        # self.Hlayout.addWidget(self.Gbutton)

        self.Pbutton =  QPushButton("Play") # to play the video
        self.Pbutton.clicked.connect(self.Play)
        self.Pbutton.setFixedSize(50,50)
        self.Hlayout.addWidget(self.Pbutton)

        self.layout.addLayout(self.Hlayout)

        # comment out these 3 line if you want to remove the Iframe
        self.web_view = QWebEngineView(self) #web_view for Iframe
        self.Vlayout.addWidget(self.web_view)
        self.web_view.setFixedSize(400,400)

        self.setLayout(self.layout)
        self.setWindowTitle('Kodi')
        self.List(url)  #lists the default website home page
        self.show()

    def addButton(self, item, hide=False, filter=False):
        button = QPushButton(item)
        self.Vlayout.addWidget(button)
        if hide:
            button.hide() #hidden by default
            self.filter_buttons[item] = button  #adding them in a dictionary to use as toggle 
        if filter:
            button.clicked.connect(partial(self.List, url + f"?filter={item}")) #on button click filters url?filter= any of these 'latest', 'most-viewed', 'popular', 'longest', 'random'
            return
        button.clicked.connect(getattr(self,item))  # for other buttons like category, tags, next, previous etc
        

    def List(self, url, category=False, tags=False):
        self.list_widget.clear()

        html = requests.get(url).text
        if not category and  not tags:
            #example regex, must match to work or adjust to work
            self.match = re.compile(r'''<a\s+href="([^"]+)"\s+title="([^"]+)">\s+.*?<img\s+[^>]*data-src="([^"]+)".*?</a>''', re.DOTALL | re.IGNORECASE).findall(html)
        # elif category:
        #     self.match = re.compile(r'''regex here for category''', re.DOTALL | re.IGNORECASE).findall(html) # if you know all the category like filters you can use category like filters too
        # elif tags:
        #     self.match = re.compile(r'''regex here for tags>''', re.DOTALL | re.IGNORECASE).findall(html)
        for match in self.match:
            self.list_widget.addItem(match[1])  #in this case the first match[0] is the url, [1] is the title of the video and [2] is the img url
        # nextp = re.compile(r'''href="([^"]+)">Next''').search(html) #next page link regex to find the next page url
        # prevp = re.compile(r'''href="([^"]+)">Previous''').search(html) #previous page link regex to find the previous page url
        # if nextp:    
        #     self.filter_buttons["Next"].show()  #toogle on for button if next url is found
        #     self.nexturl = nextp.group(1)   #putting the url in nexturl to be used in next button click
        # else:
        #     self.filter_buttons["Next"].hide() #hiding the button if no url is found
        # if prevp:  
        #     self.filter_buttons["Previous"].show()
        #     self.prevurl = prevp.group(1)
        # else:
        #     self.filter_buttons["Previous"].hide()
    
    # def category(self): #category button trigger
    #     self.List(url+'categories/', category=True) #lists the things of url + category using self.List using the regex of category in the List()

    # def filter(self):
    #     if not self.filtered: #to toggle filter button
    #         for filt in self.filter:  
    #             self.filter_buttons[filt].show()  #showing all the filter buttons
    #         self.filtered = True
    #     elif self.filtered:
    #         for filt in self.filter:
    #             self.filter_buttons[filt].hide()
    #         self.filtered = False

    # def tags(self):
    #     self.List(url+'tags/', tags=True)
    
    # def Next(self):
    #     self.List(self.nexturl)

    # def Previous(self):
    #     self.List(self.prevurl)

    # def GO(self):
    #     index = self.list_widget.currentRow() #the index of the selected  item in the list
    #     if 0 <= index < len(self.match):
    #         match = self.match[index]  #here match is the match of that index where match[0]=url which is to be listed when go is clicked
    #         self.List(match[0])
        

    def onListItemClicked(self):    #on the list item clicked it shows the img
        index = self.list_widget.currentRow()
        if 0 <= index < len(self.match):
            match = self.match[index]
            if len(match) > 2:      #checking if match has img_url which is at index 2
                self.set_image(match[2])    #setting the img using function

    def set_image(self, image_url): #getting the img using requests and loading it using pixmap
        pixmap = QPixmap()
        response = requests.get(image_url)
        if response.status_code == 200:
            image_data = response.content
            pixmap.loadFromData(image_data)
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)
        else:
            print("Error loading image:", response.status_code)

    def Play(self): #the play button trigger will give 3 options
        #  using iframe in the python window mainly used in Embed and iframes
        #  using vlc to play in the pc a little complex as the direct video url is needed for network streaming
        #  opening a browser tab with the video link easy but chromedriver and selenium is needed but works for all videos
        index = self.list_widget.currentRow()
        if 0 <= index < len(self.match):
            match = self.match[index]       
            html = requests.get(match[0]).text
            videolink = re.search(r"<iframe\s+src='(.*?)'\s+[^>]*></iframe>", html) #must match the regex of website to work
            if  videolink is not None:
                # uncomment this if you want to use Iframe
                self.web_view.setUrl(videolink.group(1))
                #uncomment these if you want to use browser to use
                # self.open_video(videolink.group(1)) #opening the video url in the browser as direct video link is not necessary
                #uncomment these if you want to use vlc to use
                # vlc_play(videolink.group(1)) #use if the iframe url is direct video link which most of the time isn't the case

                
    # def open_video(self, url):
    #     driver.execute_script(f"window.open('{url}');")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

