import sys
from io import StringIO

class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # 确保立即输出
    def flush(self):
        for f in self.files:
            f.flush()

class CaptureMgt(list):
    def __enter__(self):
        self._stdout = sys.stdout
        self._temp_out = StringIO()
        # Tee对象会同时向原始stdout和临时StringIO对象写入，实现同时打印和捕获
        sys.stdout = Tee(self._stdout, self._temp_out)
        return self
    def __exit__(self, *args):
        # 捕获输出，恢复原始stdout
        sys.stdout = self._stdout
        self.extend(self._temp_out.getvalue().splitlines())
        self._temp_out.close()

# 示例函数
if __name__ == "__main__":
    def fun():
        print("Hello, world!")

    # 使用上下文管理器
    with CaptureMgt() as output:
        fun()

    # 输出被捕获且同时打印
    print("捕获的输出:", output)