import re
import json
from xoxxox.shared import Custom
from xoxxox.librag import OpeRag

#---------------------------------------------------------------------------

class RagPrc:

  def __init__(self, config="xoxxox/config_ragdir_000", **dicprm):
    diccnf = Custom.update(config, dicprm)
    self.operag = OpeRag(diccnf["smodel"])
    self.dirrag = ""

  def status(self, config="xoxxox/config_ragdir_000", **dicprm):
    diccnf = Custom.update(config, dicprm)
    self.txtres = ""
    if self.dirrag != diccnf["dirrag"]:
      dirrag = diccnf["dirrag"]
      namnod = diccnf["namnod"]
      extvec = diccnf["extvec"]
      exttxt = diccnf["exttxt"]
      numtop = diccnf["numtop"]
      self.strref = diccnf["strref"]
      self.usrref = diccnf["usrref"]
      self.usrcnt = diccnf["usrcnt"]
      self.operag.config(numtop, dirrag, namnod, extvec, exttxt)

  def infere(self, txtreq: str) -> str:
    dirres = {"txtusr": txtreq, "txtopt": ""}
    if re.search(self.usrref, txtreq):
      txtopt = self.strref + self.operag.getvec(txtreq)
      dirres = {"txtusr": txtreq, "txtopt": txtopt}
    if re.search(self.usrcnt, txtreq):
      dirres = {"txtusr": txtreq, "txtopt": self.txtres}
    self.txtres = json.dumps(dirres, ensure_ascii=False)
    return self.txtres
