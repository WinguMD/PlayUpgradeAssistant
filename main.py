import sys
from modules.FileUtil import FileUtil
from modules.TemplateFixer import TemplateFixer

if __name__ == '__main__':
    tf = TemplateFixer
    args = sys.argv
    # work = 'session_flash'
    work = 'migrate_messages'
    files = FileUtil.load_file_lines(args[2], True)
    root = args[3]
    fd = FileUtil.load(root, files)
    fd.backup_root = args[4]
    tf.fix("session_flash", fd)
    tf.fix(work, fd)
    print(f"Done")
