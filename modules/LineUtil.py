from typing import List
import re

class LineUtil:

    @staticmethod
    def extract_function_calls(line: str, func: str) -> List[str]:
        exp = re.compile(f"({func}\\(.*?\\))")
        found = exp.findall(line)
        return found

    @staticmethod
    def extract_function_params(f: str) -> str:
        r = re.compile("\\(.*\\)")
        s = r.findall(f)
        if len(s):
            return s[0].replace("(", "").replace(")", "")
        else:
            return ""
