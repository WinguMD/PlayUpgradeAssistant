from modules.FileUtil import FileUtil
from models.FileData import FileData
from modules.LineUtil import LineUtil
from typing import List

import re


class TemplateFixer:

    @staticmethod
    def fix(work, fd: FileData):
        my = TemplateFixer

        for f in fd.sources:
            did_work = False
            fn = f.replace("./", fd.root)
            print(f"Processing: {fn}")
            if work == "session_flash":
                did_work = my.session_flash_symbol(fn, fd.backup_root)
            if work == "migrate_messages":
                did_work = my.migrate_messages(fn, fd.backup_root)
            if did_work:
                fd.done.append(f)
            else:
                fd.not_done.append(f)

    @staticmethod
    def session_flash_symbol(file: str, backup_root: str):
        my = TemplateFixer
        out = []
        changed = False
        lines = FileUtil.load_file_lines(file)
        if len(lines) == 0:
            # likely a top of dir
            return

        lines2 = my.add_req(lines)

        for line in lines2:
            line2 = line
            line2 = my.fix_symbol(line2)
            line2 = my.fix_session_flash(line2)
            out.append(line2)
            if line2 != line:
                changed = True

        out2 = my.add_implicit_messages(out)

        FileUtil.backup_file(file, backup_root)
        FileUtil.write_lines(out2, file)

        return changed

    @staticmethod
    def migrate_messages(file: str, backup_root: str) -> bool:
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
                if line.find("@(") == 0 and line.find("messages:") < 0 and not done:
                    out.append(line.replace(")", ")(implicit messages: play.api.i18n.Messages)"))
                    done = True
                else:
                    out.append(line)

            out2 = []
            for line in out:
                out2.append(line.replace("Messages(", "messages(", 100))

            FileUtil.backup_file(file, backup_root)
            FileUtil.write_lines(out2, file)

        return changed

    @staticmethod
    def add_implicit_messages(lines: List[str]) -> List[str]:
        i = 0
        done = False
        res = []
        for line in lines:
            i = i + 1
            if not done and i < 10 and line.find("@(") >= 0 and line.find(
                    "(implicit messages: play.api.i18n.Messages)") < 0:
                l2 = line.replace("\n", "") + "(implicit messages: play.api.i18n.Messages)\n"
                res.append(l2)
                done = True
            else:
                res.append(line)
        return res

    @staticmethod
    def add_req(lines: List[str]) -> List[str]:
        i = 0
        done = False
        eligible = False

        for line in lines:
            if line.find("main(") >= 0:
                eligible = True
            if line.find("session") >= 0 or line.find("flash") >= 0:
                eligible = True

        if not eligible:
            return lines

        res1 = []
        add_param = True
        line_no = 0
        for line in lines:
            if line_no < 10 and line.find("@(") >= 0:
                add_param = False
            if line.find("main(") >= 0 and line.find("main(req") < 0:
                res1.append(line.replace("main(", "main(req, ").replace("req, )", "req)"))
            else:
                res1.append(line)
            line_no = line_no + 1

        res2 = []
        for line in res1:
            if i > 10:
                # Don't go to far into the source, this should be the top part of the template
                done = True
            else:
                if add_param:
                    res2.append("@(req: Http.Request)(implicit messages: play.api.i18n.Messages)")
                    add_param = False
            if line.find("@(") >= 0 and line.find("(req") < 0 and not done:
                res2.append(line.replace("@(", "@(req: Http.Request, ").replace(", )", ")"))
                done = True
            else:
                res2.append(line)
        return res2

    @staticmethod
    def fix_session_flash(line: str) -> str:
        lu = LineUtil
        if line.find("session.get(") >= 0 and line.find("req.session") < 0:
            fcs = lu.extract_function_calls(line, "session.get")
            if len(fcs) > 0:
                for fc in fcs:
                    p = lu.extract_function_params(fc)
                    nf = f'req.session.get({p}).orElse("")'
                    of = f'session.get({p})'
                    line = line.replace(of, nf)

        if line.find("flash.get(") >= 0 and line.find("req.flash") < 0:
            fcs = lu.extract_function_calls(line, "flash.get")
            if len(fcs) > 0:
                for fc in fcs:
                    p = lu.extract_function_params(fc)
                    nf = f'req.flash.get({p}).orElse("")'
                    of = f'flash.get({p})'
                    line = line.replace(of, nf)

        return line

    @staticmethod
    def fix_symbol(line) -> str:
        founds = re.findall("('.*?->)", line)
        for found in founds:
            a = found.replace("->", "")
            b = a.replace("'", "")
            c = b.strip()
            line = line.replace(found, f"Symbol(\"{c}\") ->")
        return line
