import os
import hashlib
import zipfile
from send2trash import send2trash

def get_file_hash(path):
    hasher=hashlib.sha256()
    try:
        full_path=os.path.normpath(path)
        if os.name=='nt' and not full_path.startswith("\\\\?\\"):
            full_path="\\\\?\\"+full_path
        with open(full_path,'rb') as f:
            while chunk :=f.read(4096):
                hasher.update(chunk)
            return hasher.hexdigest()
    except (PermissionError,OSError):
        return None

def process_files(folder:str,callback=None):
    record={}
    duplicates_found=0
    space_saved=0
    compressed =0
    all_files=[]
    for root,dir,files in os.walk(folder):
        for f in files:
            all_files.append(os.path.join(root,f))
    total=len(all_files)
    for i,path in enumerate(all_files):
        try:
            if callback:
                callback(i+1,total)
            full_path=os.path.normpath(path)
            if os.name=='nt' and not full_path.startswith("\\\\?\\"):
                full_path="\\\\?\\"+full_path 
            if not os.path.exists(full_path):
                continue
            f_hash=get_file_hash(full_path)
            if f_hash in record:
                send2trash(full_path)
                duplicates_found+=1
                space_saved+=os.path.size(full_path)
            else:
                record[f_hash]=full_path
                if os.path.getsize(full_path)>50*1024*1024 and not path.endswith('.zip'):
                    zip_path=path+".zip"
                    with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as zipf:
                        zipf.write(path,os.path.basename(full_path))
                    send2trash(path)
                    compressed+=1
        except Exception:
            continue
    return duplicates_found,space_saved,compressed
