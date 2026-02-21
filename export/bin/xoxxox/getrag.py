import argparse
from xoxxox.shared import Custom
from xoxxox.librag import OpeRag

#---------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("arg1")
parser.add_argument("--config", default="")
parser.add_argument("--dirrag")
parser.add_argument("--namnod")
parser.add_argument("--extvec")
parser.add_argument("--exttxt")
parser.add_argument("--numtop", type=int)
objarg = parser.parse_args()
dicprm = {k: v for k, v in vars(objarg).items() if v is not None}
diccnf = Custom.update(dicprm["config"], dicprm)

operag = OpeRag(diccnf["smodel"])
operag.config(diccnf["numtop"], diccnf["dirrag"], diccnf["namnod"], diccnf["extvec"], diccnf["exttxt"])
print(operag.getvec(objarg.arg1))
