import subprocess
import sys
import os

DD_IN = sys.argv[1]
DD_OUT = "/dev/mmcblk2"
print("烧录文件：", DD_IN)
if not os.path.isfile(DD_IN):
    print("文件不存在")
    exit()
file_size=os.path.getsize(DD_IN)

def burn_progress(speed, total_burned):
    print(f"烧录速度: {speed} MB/s,  {total_burned}/{file_size} = {total_burned/file_size}")


process = subprocess.Popen(
    ["dd", f"if={DD_IN}", f"of={DD_OUT}", "status=progress"], stderr=subprocess.PIPE
)
process.stderr.read(1).decode()  # 第一个字符是\r，抛弃，防止下面的程序有bug
output = ""
while True:
    b = process.stderr.read(1).decode()
    output += b
    if b == "\r":
        data = output.split(" ")
        # 0 182032384
        # 1 bytes
        # 2 (182
        # 3 MB,
        # 4 174
        # 5 MiB)
        # 6 copied,
        # 7 2
        # 8 s,
        # 9 91.0
        # 10 MB/s
        total_burned = int(data[0])
        speed = float(output.split(" ")[9])

        # 调用进度函数
        burn_progress(speed, total_burned)
        output = ""

    if process.poll() is not None:
        print("end")
        print(output)
        break
