# coding=utf-8

import requests
import sys
import os
import re


proxies = {
    "http": "10.193.13.69:80",
    "https": "10.193.13.69:80",
}

def get_source(nickname, page_index):
    aim_url = "https://%s.tumblr.com/page/%d" % (nickname, page_index)
    print('[o] 正在从博客获取资源 %s ...' % aim_url)
    try:
        response_string = requests.get(url=aim_url, proxies=proxies, timeout=50).content.decode('utf8').replace('\n', '')
        if "posts-no-posts content" not in response_string:
            source_elements = re.findall(r'<iframe(.+?)>', response_string)

            if len(source_elements) > 0:
                dir_path = sys.path[0] + '/' + aim_url.split('//')[1].split('.')[0] + '/'
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

                for this_source in source_elements:
                    if "/video/" in this_source:
                        video_dir = dir_path + 'video/'
                        if not os.path.exists(video_dir):
                            os.makedirs(video_dir)
                        video_url = re.findall(r"src='(.+?)'", this_source)[0]
                        video_response = requests.get(url=video_url, proxies=proxies, timeout=50).content.decode('utf8').replace('\n', '')
                        video_source = re.findall(r'<source src="(.+?)"', video_response)[0]
                        video_name = video_source.split('/')[-1] + '.mp4'
                        print(video_source)
                        video_source = "https://vtt.tumblr.com/" + video_name
                        print(video_source)
                        write_file(video_source, video_dir, video_name)

            else:
                print('[x] 获取不到资源！')
            page_index += 1
            get_source(nickname, page_index)
        else:
            print('[!] 获取资源成功!')
    except Exception as e:
        print(e)
        get_source(nickname, page_index)

def write_file(source_url, dir_path, file_name):
    if not os.path.exists(dir_path + file_name):
        print('[*] 资源 %s 正在下载...' % file_name)
        file_download = requests.get(url=source_url, proxies=proxies, timeout=50)
        print(file_download.status_code)
        if file_download.status_code == 200:
            with open(dir_path + file_name, 'wb') as code:
                code.write(file_download.content)
    else:
        print('[*] 资源 %s 下载完成.' % file_name)


if __name__ == '__main__':
    user_nickname = sys.argv[1]
    get_source(user_nickname, 1)
