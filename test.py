import os,zipfile,re,time,json
import shutil
import trans
class extractJar():
    def __init__(self,file_path):
        self.file_path=file_path
        self.file_mods=file_path+"\\mods"
        self.file_middle_mods=file_path+"\\middle_mods"
        self.file_taget_mods=file_path+"\\target_mods"
        self.mkdir(self.file_mods)
        self.mkdir(self.file_middle_mods)
        self.mkdir(self.file_taget_mods)
        pass
    def mkdir(self,path):
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path) 
        else:
            print(111)
    def openfile(self):
        files=os.listdir(self.file_mods)
        print("载入文件中...")
        for file in files:
            print("发现文件:"+file)
            print("解压文件:"+file)
            filename_jar=self.ex_jar(file)
            
    def findfile(self,path):
        files=os.listdir(path)
        try:
            path=path+"\\"+files[0]
        except IndexError:
            return
        try:
            files=os.listdir(path)
        except NotADirectoryError:
            return
        if "lang"  in files:
            path=path+"\\lang"
            files=os.listdir(path)
            if "zh_CN.lang" not in files and "zh_cn.lang" not in files and "zh_cn.guess" not in files and "zh_cn.json" not in files:
                print(files)
                
                if "en_us.lang" in files:
                    
                    paths=path+'\\zh_cn.lang'
                    
                    path=path+"\\en_us.lang"
                    with open(path, 'r', encoding="utf-8") as f:
                        s=f.read()
                        reg=re.findall(r".*name=(.*)\n",s)
                        for i in reg:
                            re_s=trans.transf(i)
                            s=s.replace('name='+i, 'name='+re_s)
                            time.sleep(0.1)
                        f1=open(paths,'w',encoding="utf-8")
                        f1.write(s)
                        f1.close()
                        print("ok!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        f.close()
                        self.re_jar()
                    print("US") 
                elif "en_US.lang." in files:
                    paths=path+'\\zh_CN.lang'
                    path=path+"\\en_US.lang"
                    with open(path, 'r', encoding="utf-8") as f:
                        s=f.read()
                        reg=re.findall(r".*=(.*)\n",s)
                        for i in reg:
                            re_s=trans.transf(i)
                            s=s.replace('='+i, '='+re_s)
                            time.sleep(0.1)
                        f1=open(paths,'w',encoding="utf-8")
                        f1.write(s)
                        f1.close()
                        print("ok!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        f.close()
                        self.re_jar()
                    print("us")
                elif "en_us.json" in files:
                    paths=path+'\\zh_cn.json'
                    path=path+"\\en_us.json"
                    f = open(path,'r',encoding='utf-8')
                    try:
                        m = json.load(f)
                    except json.decoder.JSONDecodeError:
                        return
                    f.close()
                    for text in m:
                        print(m[text])
                        m[text]=trans.transf(m[text])
                        time.sleep(0.1)
                    f1=open(paths,'w',encoding='utf-8')
                    f1.write(json.dumps(m))
                    f1.close()
                    self.re_jar()
        else:
            pass
    def ex_jar(self,path):
        filename_jar=path.split(".jar")[0]
        self.filename_jar=filename_jar
        zf = zipfile.ZipFile(self.file_mods+"\\"+path)
        try:
            zf.extractall(path=self.file_middle_mods+"\\"+filename_jar)
            self.jar_path=path=self.file_middle_mods+"\\"+filename_jar
            self.findfile(self.file_middle_mods+"\\"+filename_jar+"\\assets")
        except FileNotFoundError:
            pass
        return filename_jar
    def re_jar(self):
        dir_name =self.jar_path#要压缩目录
        zip_file = self.file_taget_mods+"\\"+self.filename_jar+'.jar'#压缩位置
        self.folder_to_zip(dir_name,zip_file)
        print('目录压缩成功')
 
    def folder_to_zip(self,folderpath, zipath):
        """
        folderpath : 待压缩文件夹的路径
        zipath     ：压缩后文件存放的路径    
        """
        zip = zipfile.ZipFile(zipath, "w", zipfile.ZIP_DEFLATED)
        for path, dirnames, filenames in os.walk(folderpath):
            # 将待压缩文件夹下的所有文件逐一添加到压缩文件
                fpath = path.replace(os.path.dirname(folderpath), '')
                print(fpath)
                fpath=fpath.replace('\\'+self.filename_jar, '')
                for filename in filenames:
                    print("path:"+path+"filename:"+filename)
                    zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
        zip.close()
def file_to_zip(filepath, zipath):
    '''
    filepath : 待压缩文件的路径
    zipath   ：压缩后文件的路径
    '''
    zf = zipfile.ZipFile(zipath, 'w', zipfile.ZIP_DEFLATED) # 创建压缩文件对象
    zf.write(filepath, os.path.basename(filepath)) # 传入待压缩文件路径，进行压缩
    zf.close()
a=extractJar("C:\\Users\\folk\\Desktop\\transforms_jar2")
a.openfile()