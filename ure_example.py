import pyb
import ure

text = ("NNMI how are you\r\n")
p = ure.search("NN(.+?)\r\n", text)
print(p.group(0))
