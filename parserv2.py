from subprocess import Popen, PIPE
import requests
import shlex
import os
import time
import webbrowser

def execute_and_return(cmd):
    args = shlex.split(cmd)
    proc = Popen(args, stdout=PIPE, stderr=PIPE, cwd=os.path.dirname(os.path.abspath(__file__)))
    out, err = proc.communicate()
    return out, err

def make_req(error, tag="python"):
    print("searching for " + error)
    resp = requests.get("https://api.stackexchange.com/" + "/2.3/search?order=desc&sort=activity&tagged={}&intitle={}&site=stackoverflow".format(tag, error))
    return resp.json()

def get_urls(json_dict):
    url_list = []
    count = 0
    for i in json_dict["items"]:
        if i["is_answered"]:
            url_list.append(i["link"])
            count += 1
            if count == 3 or count == len(i):
                break
    return url_list

if __name__ == "__main__":
    filename = input("Enter the file name to execute: ")
    out, err = execute_and_return("python " + filename)
    error_message = err.decode("utf-8").strip().split("\r\n")[-1]
    print(error_message)
    if error_message:
        filter_out = error_message.split(":")
        print(filter_out)
        print(filter_out[0])
        json1 = make_req((filter_out[0]))
        json2 = make_req((filter_out[1]))
        json = make_req(error_message)
        url_list1 = get_urls(json1)
        url_list2 = get_urls(json2)
        url_list3 = get_urls(json)
        url_list = []
        if url_list1 is not None:
            url_list += url_list1
        if url_list2 is not None:
            url_list += url_list2
        if url_list3 is not None:
            url_list += url_list3
        if url_list:
            for url in url_list:
                webbrowser.open(url)
                time.sleep(1)  # wait for 1 second before opening the next URL
        else:
            print("No relevant urls found.")
    else:
        print("No error")
