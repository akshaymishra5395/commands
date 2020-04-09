pip install request 

import requests
r = requests.get("https://www.google.com/")

help(r)     ---- class of object (Class Response )
dir(r)      ---- Attributes and methods of the Class with object r
r.text      ---- content in response in unicode (HTML of page)
r.links     ---- Link in page
r.content     ---- content of response in bytes ,image when url is image url 
r.status_code ----200 (Success),300(Redirect),400(error),500(Server Error)
r.ok  --- True for less and 300 else False 
r.headers   ---  header of response

*Imgage content Download and save as Image file*
r = requests.get("https://www.google.com/image1.jpg")
if r.staus_code == 200:
  with open('comic.jpg' ,'wb') as f:
    r.content
