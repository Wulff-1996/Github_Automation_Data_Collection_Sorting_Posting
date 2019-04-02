##  imports
import json
import os
import re
import subprocess
from urllib.error import URLError
from urllib.request import Request, urlopen
import sys


##  get content from url
def requestURL(someurl):
    req = Request(someurl)
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            sys.exit()
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            sys.exit()
    else:
        return json.loads(response.read())

##  convert all info to name url dictionary
def convertJsonListToUrlDictionary(json_list):
    urlDictionary = {}
    count = 0

    while count < len(json_list):
        name = json_list[count]['name']
        url = json_list[count]['html_url']
        urlDictionary[name] = url
        count += 1

    return urlDictionary


def create_subdirectories_clone_pull (url_directory):
    for k,v in url_directory.items():
        path = '/Users/jake/Desktop/python/mandatory/repositories/' + k

        ## create sub directories for the specific folders if not exists
        if not os.path.exists(path):
            ## make directory
            os.mkdir(path)

        ##  clone if subdirectory is empty
        if not os.listdir(path):
            print('is empty: ', path)
          
            cmd = 'git clone ' + v + ' ' + path
            pipe = subprocess.Popen(cmd, shell=True)
            pipe.wait()

        ##  pull when not empty    
        else:
            print("PULL: directory not empty")

            basePath = '/Users/jake/Desktop/python/mandatory/repositories/' 
            os.chdir(path)

            cmd = 'pwd'
            pipe = subprocess.Popen(cmd, shell=True)
            pipe.wait()

            cmd = 'git reset --hard origin/master'
            pipe = subprocess.Popen(cmd, shell=True)
            pipe.wait()

            cmd = 'cd ..'
            pipe = subprocess.Popen(cmd, shell=True)
            pipe.wait()

def get_required_reading_urls(urlDictionary):

    lines = {}

    for k,v in urlDictionary.items():
        path = '/Users/jake/Desktop/python/mandatory/repositories/' + k
        
        ##  skip python-elective-1-spring-2019.github.io
        if k == 'python-elective-1-spring-2019.github.io': continue

        ##  go to subdirectory
        os.chdir(path)

        ##  get the readme file
        file = open('README.md', 'r')
        text = file.read()

        print('\n', k)

        lines2 = {}
        isRequiredReading = False
        for line in text.splitlines():
            
            if 'Supplementary reading' in line: 
                print('\tSupplementary reading break')
                break
            elif 'Required reading' in line:
                print('\tRequired reading')
                isRequiredReading = True
            if isRequiredReading:
                if len(line) > 0 and line[0] == '*':
                    name = line[line.find('[')+1 : line.find(']')]
                    url = line[line.find('(')+1 : line.find(')')]
                    print('\t\tadd: ', '\n\t\t  name: ', name, '\n\t\t  url: ', url)
                    lines2[name] = url
        lines[k] = lines2
            

        ## go back to base directory
        cmd = 'cd ..'
        pipe = subprocess.Popen(cmd, shell=True)
        pipe.wait()

    return lines

def create_required_reading_md_file(required_reading):
    
    path = '/Users/jake/Desktop/python/mandatory/required_reading/'

    if not os.path.exists(path):
        os.mkdir(path)

    f = open(path + 'required_reading.md', 'w+')

    f.write('# Required readingbob')
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write('\n### by Jakob Wulff')

    for k, v in sorted(required_reading.items(), key=lambda x: x[0]):
        f.write('\n## ' + k )
        if len(v) <= 0: 
            f.write('\ncontent will come soon')
            continue
        for x, y in sorted(v.items(), key=lambda x: x[0]):
            x = x.capitalize()
            f.write('\n* [' + x + '](' +  y + ')')
        f.write('\n')


def main():

    ##  get info for repositoires
    link = 'https://api.github.com/orgs/python-elective-1-spring-2019/repos?per_page=100'
    repositoryInfo = requestURL(link)

    ##  save name and url to a dictionary
    urlDictionary = convertJsonListToUrlDictionary(repositoryInfo)

    path = '/Users/jake/Desktop/python/mandatory/repositories'
    
    ##  create root directory for repos if not exists
    if not os.path.exists(path):
        os.mkdir(path)

    ##  create subdirectories, and clone/pull repo to subdirectory
    create_subdirectories_clone_pull(urlDictionary)

    ##  traverse subdirectories and get links for required reading
    required_reading = get_required_reading_urls(urlDictionary)

    ##  create a required_reading.md file
    create_required_reading_md_file(required_reading)

    ##  post requiredReading.md file to git
    path = '/Users/jake/Desktop/python/mandatory/required_reading'
    os.chdir(path)

    print('---git init')
    cmd = 'git init'
    pipe = subprocess.Popen(cmd, shell=True)
    pipe.wait()

    print('---git remote add origin https://github.com/Wulff-1996/python_required_reading')
    cmd = 'git remote add origin https://github.com/Wulff-1996/python_required_reading'
    pipe = subprocess.Popen(cmd, shell=True)
    pipe.wait()

    print('---git add required_reading.md')
    cmd = 'git add required_reading.md'
    pipe = subprocess.Popen(cmd, shell=True)
    pipe.wait()

    print('---git commit -m "first commit"')
    cmd = 'git commit -m "first commit"'
    pipe = subprocess.Popen(cmd, shell=True)
    pipe.wait()

    

    print('---git pull origin master')
    cmd = 'git pull origin master'
    pipe = subprocess.Popen(cmd, shell=True)
    pipe.wait()

    print('---git push -u origin master -f')
    cmd = 'git push -u origin master -f'
    pipe = subprocess.Popen(cmd, shell=True)
    pipe.wait()



##  create a main
if __name__ == '__main__':
    print('This program is being run by itself')
    main()
else:
    print('I am being imported from another module')
