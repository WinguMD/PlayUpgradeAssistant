import traceback
from pathlib import Path
import os
import shutil

from typing import List

from models.FileData import FileData


class FileUtil:
    me = "FileUtil"

    @staticmethod
    def load(root: str, file_names: List[str]) -> FileData:
        fd = FileData()
        for f in file_names:
            f2 = f.replace("./", root + "/")
            p = Path(f2.replace("\n", ""))
            if p.exists():
                fd.sources.append(f2)
            else:
                print(f"{FileUtil.me}: File is not present {f}")
        return fd

    @staticmethod
    def load_file_lines(file_name: str, clean_lf: bool = False) -> List[str]:
        f = open(file_name, "r", encoding='utf-8')
        file_list = []
        read = True
        while read:
            try:
                line = f.readline()
                if line:
                    if clean_lf:
                        line = line.replace("\n", "")
                    file_list.append(line)
                else:
                    read = False
            except:
                traceback.print_exc()
                print(f"Issue reading a file {file_name}")

        return file_list

    @staticmethod
    def write_lines(lines: List[str], file_name: str):
        f = open(file_name, "w", encoding="utf-8")
        f.writelines(lines)
        f.close()

    @staticmethod
    def backup_file(file_name: str, backup_root: str = "", ext: str = "bak"):
        rev_no = 1
        orig_root = Path(file_name).parent
        name = Path(file_name).name
        if backup_root == "":
            backup_root = orig_root
        backup_name = f"{backup_root}/{name}.{ext}"
        while Path(backup_name).exists():
            backup_name = f"{backup_root}/{name}.{rev_no}.{ext}"
            rev_no = rev_no + 1
            if rev_no > 10:
                raise Exception(f"Please cleanup backup files for {file_name}")
        backup_dir = Path(backup_name).parent
        if not Path.exists(backup_dir):
            os.makedirs(backup_dir)
        shutil.copy(file_name, backup_name)

