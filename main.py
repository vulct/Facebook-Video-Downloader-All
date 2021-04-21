import re
import requests
import urllib.request
import os
import time
import browser_cookie3

def createFolder(id):
    print("-----------------------------")
    print("Dang tao folder luu du lieu...")
    #-----PATH------
    #Duong dan luu file tai ve ten = ID page
    output_dir = '{0}'.format(id)
    # Make output directory if not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    #-----END PATH------
    print("Tao folder xong!!!")
    print("-"*15) 

def get_content_type(url):
    response = requests.head(url)
    #length_file = response.headers['Content-Length']
    type_file = response.headers['Content-Type']
    return type_file

def downloadImage(idPage,linkAPI):
    #https://graph.facebook.com/v2.3/2059064644349478/photos?fields=source,name,length&limit=100&access_token=

    os.chdir(idPage)
    ##################
    ###THƯ MỤC LƯU ẢNH
    folder_image = "Image"
    if not os.path.exists(folder_image):
        os.makedirs(folder_image)
    cj = browser_cookie3.load()
    #Get URL video
    time.sleep(5)
    response = requests.get(linkAPI,cookies=cj)
    source = response.json()['data']
    count_file = 1
    i = len(source)
    for x in source:
        ## TAI ANH : URL = FULL_PICTURE
        if x['type'] == "photo":
            ## Lưu name
            try:
                content = x['message'] + "\nThoi gian:" + x['created_time']
            except:
                content = ""
            try:
                url = x['full_picture']
            except:
                url = ""
            if url != "":
                type = get_content_type(url)
                arr1 = type.split('/', 1)
                os.chdir("Image")
                # Folder bài viết = ID.
                output_dir_file = '{0}'.format(x['id'])
                # Nếu chưa có thì tạo folder đó.
                if not os.path.exists(output_dir_file):
                    os.makedirs(output_dir_file)
                ########################
                ########################
                save_path = output_dir_file + '/' + x['id'] + "." + arr1[1]
                ## Đường dẫn lưu name photo
                save_content = output_dir_file + '/' + x['id'] + ".txt"
                print(f"Save name of photo ID: {x['id']}.......")
                with open(save_content,'w',encoding = 'utf-8') as f:
                    f.write(content)
                print(f"Downloading photo ID: {x['id']}............... \n")
                urllib.request.urlretrieve(url, save_path)
                print("{1}. Download file ID: {0} complete! \n".format(x['id'], count_file))
                i += 1
                count_file += 1
                os.chdir("../")
                time.sleep(1)
        ############################################################ 
    clear = lambda: os.system('cls') #on Windows System
    clear()
    sourcemoi = response.json()['paging']
    try:
        linkmoi = sourcemoi['next']
    except:
        linkmoi = ""
        print("Da tai xuong tat ca hinh anh cua page.")
    if linkmoi is not None:
        print("Dang get link.................")
        time.sleep(5)
        os.chdir("../")
        downloadImage(idPage,linkmoi)
    else:
        print(f"Da tai xuong {count_file} hinh anh cua page.")

def downloadVideo(idPage,linkAPI):
    os.chdir(idPage)
    # ####################
    # ###THƯ MỤC LƯU VIDEO
    folder_video = "Video"
    if not os.path.exists(folder_video):
        os.makedirs(folder_video)
    cj = browser_cookie3.load()
    #Get URL video
    time.sleep(5)
    response = requests.get(linkAPI,cookies=cj)
    source = response.json()['data']
    count = 1
    i = len(source)
    for x in source:
        ## Lưu name
        try:
            content = x['name'] + "\nThoi gian: " + x['updated_time']
        except:
            content = ""
        try:
            url = x['source']
        except:
            url = ""
        if url != "":
            ## BAT DAU TAI XUONG 
            os.chdir("Video")
            # Folder bài viết = ID.
            output_dir_file = '{0}'.format(x['id'])
            # Nếu chưa có thì tạo folder đó.
            if not os.path.exists(output_dir_file):
                os.makedirs(output_dir_file)
            ########################
            ########################
            save_path = output_dir_file + '/' + x['id'] + ".mp4"
            ## Đường dẫn lưu message video
            save_content = output_dir_file + '/' + x['id'] + ".txt"
            print("Save message.......")
            with open(save_content,'w',encoding = 'utf-8') as f:
                f.write(content)
            print("Downloading............... \n")
            urllib.request.urlretrieve(url, save_path)
            print("{1}. Download file ID: {0} complete! \n".format(x['id'], count))
            i += 1
            count += 1
            os.chdir("../")
            time.sleep(1)
            ###########################################
    clear = lambda: os.system('cls') #on Windows System
    clear()
    sourcemoi = response.json()['paging']
    try:
        linkmoi = sourcemoi['next']
    except:
        linkmoi = ""
        print("Da tai xuong tat ca video cua page.")
    if linkmoi is not None:
        print("Dang get link.................")
        time.sleep(5)
        os.chdir("../")
        downloadVideo(idPage,linkmoi)
    else:
        print(f"Da tai xuong {count} video cua page.")

def main():
    linkAPI_Video = ""
    linkAPI_Image = ""
    tokenUser = input("Nhap vao token user: ")
    print("-"*15)
    idPage = input("Nhap vao ID page: ")
    createFolder(idPage)
    print("-"*15)
    print("-"*15)
    print("1.Tai hinh anh cua page.")
    print("2.Tai video cua page.")
    print("3.Tai hinh anh + video cua page.")
    selectOption = input("Lua chon chuc nang: ")
    if (selectOption == "1"):
        linkAPI_Image = "https://graph.facebook.com/"+idPage+"/feed?fields=full_picture,type,message&limit=100&access_token="+tokenUser
        downloadImage(idPage,linkAPI_Image)
    elif (selectOption == "2"):
        linkAPI_Video = "https://graph.facebook.com/"+idPage+"/videos?fields=source,name&limit=100&access_token="+tokenUser
        downloadVideo(idPage,linkAPI_Video)
    elif (selectOption == "3"):
        linkAPI_Image = "https://graph.facebook.com/"+idPage+"/feed?fields=full_picture,type,message&limit=100&access_token="+tokenUser
        linkAPI_Video = "https://graph.facebook.com/"+idPage+"/videos?fields=source,name&limit=100&access_token="+tokenUser
        try:
            downloadImage(idPage,linkAPI_Image)
        except:
            downloadVideo(idPage,linkAPI_Video)
        
if __name__ == "__main__":
    main()