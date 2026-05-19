EXT_LANG = {
    ".py":"python", ".js":"javascript", ".jsx":"javascript",
    ".ts":"typescript", ".tsx":"typescript", ".java":"java",
    ".go":"go", ".rb":"ruby", ".rs":"rust", ".c":"c", ".cpp":"cpp",
}
def detect(path: str):
    import os
    _, ext = os.path.splitext(path.lower())
    return EXT_LANG.get(ext)
