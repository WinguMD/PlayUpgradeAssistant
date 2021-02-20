import sys
from modules.FileUtil import FileUtil
from modules.TemplateFixer import TemplateFixer

if __name__ == '__main__':
    tf = TemplateFixer
    args = sys.argv
    work = args[1]
    files = FileUtil.load_file_lines(args[2], True)
    root = args[3]
    fd = FileUtil.load(root, files)
    fd.backup_root = args[4]
    if work == "templates":
        # tf.do_request_session_update(fd)
        # tf.do_messages(fd)
        # tf.do_main_messages(fd)
        pass
    if work == "session_get_or_else":
        tf.fix(work, fd)
    print(f"Done {work}")
