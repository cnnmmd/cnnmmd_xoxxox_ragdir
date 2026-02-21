import glob
import re
import heapq
import numpy as np
from sentence_transformers import SentenceTransformer

#---------------------------------------------------------------------------

class OpeRag:

  def __init__(self, smodel: str):
    self.mmodel = SentenceTransformer(smodel)

  def vectxt(self, byttxt: bytes) -> bytes:
    v = self.mmodel.encode([byttxt.decode("utf-8")], normalize_embeddings=True)
    return v.astype("float32").tobytes()

  def config(self, numtop: int, dirrag: str, namnod: str, extvec: str, exttxt: str):
    self.numtop = numtop
    self.dirrag = dirrag
    self.namnod = namnod
    self.extvec = extvec
    self.exttxt = exttxt

  def getvec(self, txtreq):
    # 取得：ベクターストア群（ファイル）
    lstdic = []
    lstpth = glob.glob(self.dirrag + "/" + self.namnod + "*" + self.extvec)
    # 比較
    for i in lstpth:
      s = OpePth.getbyt(i)
      d = self.vectxt(txtreq.encode("utf-8"))
      f = OpeRag.difcos(s, d)
      lstdic.append({"f": f, "v": i})
      #print(str(f) + " " + i, flush=True) # DBG
    # 抽出：上位Ｎコ
    txtopt = ""
    lsttop = heapq.nlargest(self.numtop, lstdic, key=lambda x: x["f"])
    for i in lsttop:
      #print(i["v"], flush=True) # DBG
      m = re.search(self.dirrag + "/" + self.namnod + "(.*?)" + self.extvec, i["v"])
      n = m.group(1)
      t = self.dirrag + "/" + self.namnod + n + self.exttxt
      #print(t, flush=True) # DBG
      #print(OpePth.getbyt(t).decode("utf-8"), flush=True) # DBG
      txtopt = txtopt + "\n" + OpePth.getbyt(t).decode("utf-8")
    # 出力
    return txtopt

  @staticmethod
  def difcos(vecsrc: bytes, vecdst: bytes) -> float:
    s = np.frombuffer(vecsrc, dtype=np.float32)
    d = np.frombuffer(vecdst, dtype=np.float32)
    return float(np.dot(s, d) / (np.linalg.norm(s) * np.linalg.norm(d)))

class OpePth:

  @staticmethod
  def putbyt(vecsrc: bytes, pthsrc: str):
    with open(pthsrc, "wb") as f:
      f.write(vecsrc)

  @staticmethod
  def getbyt(pthsrc: str) -> bytes:
    with open(pthsrc, "rb") as f:
      vecsrc = f.read()
      return vecsrc
