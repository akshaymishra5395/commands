#pip install request 

import requests
r = requests.get("https://www.google.com/")

help(r)     #---- class of object (Class Response )
dir(r)      #---- Attributes and methods of the Class with object r
r.text      #---- content in response in unicode ,HTML of page
r.links     #---- Link in page
r.content     #---- content of response in bytes ,image when url is image url 
r.status_code #----200 (Success),300(Redirect),400(error),500(Server Error)
r.ok          #--- True for less and 300 else False 
r.headers     #---  header of response
r.url         #---- url used in response 
r.json()        #convert r to dict
#*****Imgage content Download and save as Image file*****
r = requests.get("https://www.google.com/image1.jpg")
if r.staus_code == 200:
  with open('comic.jpg' ,'wb') as f:
    r.content
 
#*****get request with params *****
payload= {'pae':2,'count':25}
r = requests.get("https://httpbin.org/get",params=payload)

#*****Post request with params *****
payload= {'username':"akshay",'password':"abc"}
r = requests.get("https://httpbin.org/get",data=payload)
print(r.text)     #see form value Password is seen clearly


#*****Post request with params *****
payload= {'username':"akshay",'password':"abc"}
r = requests.get("https://httpbin.org/post",data=payload)
print(r.text)     #see form value Password is seen clearly
r_dict = r.json()  #print(r_dict["form"])

#*****GET request with auth *****
payload= ('corey","test")
r = requests.get("https://httpbin.org/basic-auth/corey/testing",auth=payload)
#can give 200  #401
          

#*****GET request with timeout *****  
r = requests.get("https://httpbin.org/basic-auth/delay/1",timeout=3)
#if not come within time ,then request.exception.ReadTimeout
#This prevent from longer waiting
          


    


    
