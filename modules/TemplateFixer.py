from modules.FileUtil import FileUtil
from models.FileData import FileData
from modules.LineUtil import LineUtil
from typing import List

import re


class TemplateFixer:

    @staticmethod
    def do_main_messages(fd: FileData):
        for f in fd.sources:
            fn = f.replace("./", fd.root)
            if TemplateFixer.do_main_messages_file(fn, fd.backup_root):
                fd.done.append(f)
            else:
                fd.not_done.append(f)

    @staticmethod
    def do_main_messages_file(file: str, backup_root: str) -> bool:
        changed = False
        lines = FileUtil.load_file_lines(file)
        lu = LineUtil
        eligible = False

        out1 = []
        for line in lines:
            if line.find("@main(") >= 0:
                fc = lu.extract_function_calls(line, "@main")
                for f in fc:
                    fp = lu.extract_function_params(f)
                    nf = f"@main({fp}, null, messages)"
                    rep = line.replace(f"@main({fp})", nf)
                    out1.append(rep)
                    eligible = True
                    changed = True
                    break;
            else:
                out1.append(line)

        out2 = []
        if eligible:
            for line in out1:
                if line.find("@(") >= 0 and line.find("messages:") == -1:
                    out2.append(line.replace(")", ", messages: play.i18n.Messages)", 1))
                    changed = True
                else:
                    out2.append(line)

        if changed:
            FileUtil.backup_file(file, backup_root)
            FileUtil.write_lines(out2, file)

        return changed

    @staticmethod
    def do_messages(fd: FileData):
        for f in fd.sources:
            fn = f.replace("./", fd.root)
            if TemplateFixer.do_message_file(fn, fd.backup_root):
                fd.done.append(f)
            else:
                fd.not_done.append(f)

    @staticmethod
    def do_message_file(file: str, backup_root: str) -> bool:
        changed = False
        lines = FileUtil.load_file_lines(file)
        eligible = False
        for line in lines:
            if line.find("Messages(") >= 0:
                eligible = True
                break

        if eligible:
            out = []

            done = False
            for line in lines:
                if line.find("@(") == 0 and not done:
                    out.append(line.replace(")", ", messages: play.i18n.Messages)"))
                    done = True
                else:
                    out.append(line)

            out2 = []
            for line in out:
                out2.append(line.replace("Messages(", "messages.at(", 100))

            FileUtil.backup_file(file, backup_root)
            FileUtil.write_lines(out2, file)

        return changed

    @staticmethod
    def do_request_session_update(fd: FileData):
        for f in fd.sources:
            fn = f.replace("./", fd.root)
            if TemplateFixer.update_request_session_file(fn):
                fd.done.append(f)
            else:
                fd.not_done.append(f)

    @staticmethod
    def update_request_session_file(file) -> bool:
        my = TemplateFixer
        lines = FileUtil.load_file_lines(file)
        has_session = False
        has_main = False
        for line in lines:
            if re.search(r"session\.get", line):
                print(f"Session: {line}")
                if line.find("session().getOrElse") >= 0:
                    has_session = False
                else:
                    has_session = True
                break

        for line in lines:
            if re.search(r"^@main\(", line):
                if line.find("(req") >= 0:
                    has_main = True
                break

        if has_session or has_main:
            print(f"+ {file}")
            lines2 = my.add_req(lines)
            out: List[str] = []
            for line in lines2:
                res = my.fix_session_get(line)
                out.append(res)
            FileUtil.backup_file(file)
            FileUtil.write_lines(out, file)
            return True
        else:
            return False

    @staticmethod
    def add_req(lines: List[str]) -> List[str]:
        i = 0
        done = False
        res = []
        for line in lines:
            if i > 10:
                # Don't go to far into the source, this should be the top part of the template
                done = True
            if line.find("@(") >= 0 and not done:
                res.append(line.replace("@(", "@(req: Http.Request, "))
                done = True
            else:
                res.append(line)
        return res

    @staticmethod
    def fix_session_get(line: str) -> str:
        u = LineUtil
        calls = u.extract_function_calls(line, "session.get")
        result = line
        for c in calls:
            p = u.extract_function_params(c)
            rep = f"req.session().getOrElse({p}, \"\")"
            result = result.replace(c, rep)
        return result
