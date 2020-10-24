"""
画像を保存してあるディレクトリをアーカイブする。
"""
import argparse
import glob
import logging
import os
import zipfile
from tqdm import tqdm

logging_fmt = "%(asctime)s %(levelname)s: %(message)s"
logging.basicConfig(format=logging_fmt)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

def add_directory_to_zip(zipf:zipfile.ZipFile,path:str):
    """
    ZIPファイルにディレクトリを追加する。
    """
    for root,dirs,files in os.walk(path):
        for file in files:
            zipf.write(
                os.path.join(root,file),
                os.path.relpath(os.path.join(root,file),os.path.join(path,".."))
            )

def main(images_dir:str,save_dir:str,dirs_per_archive:int,resume_index:int):
    os.makedirs(save_dir,exist_ok=True)

    pathname=os.path.join(images_dir,"*")
    directories=glob.glob(pathname)

    num_archives,mod=divmod(len(directories),dirs_per_archive)
    if mod!=0:
        num_archives+=1
    
    for i in tqdm(range(num_archives)):
        if i<resume_index:
            continue

        start_index=i*dirs_per_archive
        if i==num_archives-1:
            end_index=len(directories)
        else:
            end_index=(i+1)*dirs_per_archive
        target_directories=directories[start_index:end_index]

        zip_filepath=os.path.join(save_dir,str(i)+".zip")
        with zipfile.ZipFile(zip_filepath,"w",zipfile.ZIP_DEFLATED) as zipf:
            for target_directory in target_directories:
                add_directory_to_zip(zipf,target_directory)

if __name__=="__main__":
    parser=argparse.ArgumentParser()

    parser.add_argument("--images_dir",type=str)
    parser.add_argument("--save_dir",type=str)
    parser.add_argument("--dirs_per_archive",type=int,default=500)
    parser.add_argument("--resume_index",type=int,default=-1)

    args=parser.parse_args()

    main(args.images_dir,args.save_dir,args.dirs_per_archive,args.resume_index)
