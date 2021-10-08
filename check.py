import sys
import json
import zipfile
import argparse

class CheckApp():

    def __init__(self, myapp):
        self.jiagu_app = myapp
        self.jiagu_config = 'config.txt'
        self.allFileName = []

    def findFileName(self):
        zip_file = zipfile.ZipFile(self.jiagu_app)
        zip_list = zip_file.namelist()
        for evFileName in zip_list:
            if 'assets/' in evFileName or 'lib/' in evFileName:
                self.allFileName.append(evFileName.split('/')[-1])
        zip_file.close()
        return self.allFileName

    def check(self):
        with open('config.txt','r',encoding='utf8') as r:
            for line in r:
                jiaguArray = json.loads(line.strip())
                jiaguCompany = list(jiaguArray.keys())[0]
                jiaguFile = list(jiaguArray.values())[0]
                for evjiaguFile in jiaguFile:
                    if evjiaguFile in self.allFileName:
                        return jiaguCompany,evjiaguFile
        return False

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description='please input apk name'
    parser.add_argument("-a", help="apkname", dest="apkname", type=str, default=False)
    args = parser.parse_args()

    if args.apkname is False:
        print('Usage: check.py -a test.apk')
        sys.exit()

    try:
        ca = CheckApp(args.apkname)
        ca.findFileName()
        finares = ca.check()
        print('OK: Company: {0} - File: {1}'.format(*finares))
    except Exception as e:
        print('Error: Bad Check, {}'.format(e))
