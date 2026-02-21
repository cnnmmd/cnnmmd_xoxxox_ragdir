import sys
import json
import argparse
from xoxxox.shared import Custom
from xoxxox.librag import OpeRag, OpePth

parser = argparse.ArgumentParser()
parser.add_argument("--config", default="")
parser.add_argument("--srcrag", default="")
parser.add_argument("--dirrag")
parser.add_argument("--namnod")
parser.add_argument("--extvec")
parser.add_argument("--exttxt")
objarg = parser.parse_args()
dicprm = {k: v for k, v in vars(objarg).items() if v is not None}
diccnf = Custom.update(dicprm["config"], dicprm)

dirrag = diccnf["dirrag"]
srcrag = diccnf["srcrag"]
namnod = diccnf["namnod"]
extvec = diccnf["extvec"]
exttxt = diccnf["exttxt"]

operag = OpeRag(diccnf["smodel"])
with open(srcrag, "r", encoding="utf-8") as f:
  dicsrc = json.load(f)

for i in dicsrc:
  print(i["n"]) # DBG
  print(i["c"]) # DBG
  c = i["c"].encode("utf-8")
  print(operag.vectxt(c)) # DBG
  t = dirrag + "/" + namnod + i["n"] + exttxt
  v = dirrag + "/" + namnod + i["n"] + extvec
  print(t) # DBG
  print(v) # DBG
  OpePth.putbyt(c, t)
  OpePth.putbyt(operag.vectxt(c), v)
