#coding:utf8
#python2.7x,pywin32
 
import win32api,win32con,win32gui
import re,urllib
 
url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
file_name = 'D:\\picture\\'
base_url = 'https://cn.bing.com' 

def set_wallpaper_from_path(img_path):
    #打开指定注册表路径
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    #最后的参数:2拉伸,0居中,6适应,10填充,0平铺
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    #最后的参数:1表示平铺,拉伸居中等都是0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    #刷新桌面
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, img_path, win32con.SPIF_SENDWININICHANGE)

def get_content(url):
    '''doc.'''
    html = urllib.urlopen(url)
    content = html.read().decode('utf-8')
    html.close()
    
    return content

def get_images(info):
    '''
      {"images":[{"startdate":"20180724","fullstartdate":"201807241600","enddate":"20180725",
      "url":"/az/hprichbg/rb/HomerWatercolor_ZH-CN11392693224_1920x1080.jpg",
      "urlbase":"/az/hprichbg/rb/HomerWatercolor_ZH-CN11392693224",
      "copyright":"波士顿美术馆收藏的画家温斯洛·霍默的水彩画'Rocky Shore' (© Alamy)","copyrightlink":
      "http://www.bing.com/search?q=%E6%B3%A2%E5%A3%AB%E9%A1%BF%E7%BE%8E%E6%9C%AF%E9%A6%86&form=hpcapt&mkt=zh-cn",
      "quiz":"/search?q=Bing+homepage+quiz&filters=WQOskey:%22HPQuiz_20180724_HomerWatercolor%22&FORM=HPQUIZ",
      "wp":false,"hsh":"3e5768ef8c7bfa7363e564287bac7744","drk":1,"top":1,"bot":1,"hs":[]}],"tooltips":
      {"loading":"正在加载...","previous":"上一个图像","next":"下一个图像","walle":"此图片不能下载用作壁纸。","walls":"下载今日美图。仅限用作桌面壁纸。"}}
    '''
    regex = r'"url":"(.*?)"' # r 为原始字符串？？  # . 除反斜杠任意字符， + 至少有一个， ? 找到一个就结束
    
    pat = re.compile(regex)
    image_code = re.findall(pat, info)
    
    image_str = ''.join(image_code)
    image_url = base_url + image_str
    
    image_name = image_str.split('/').pop()
    image_path = file_name + image_name
    urllib.urlretrieve(image_url, image_path) # download image
    print image_path
    return image_path
 
if __name__ == '__main__':
    content = get_content(url)
    image_path = get_images(content)
    set_wallpaper_from_path(image_path)