import sqlite3
from dabaseTool import *

diag ={0:'重症肺炎',1:'呼吸衰竭',2:'心力衰竭'}
a = Parameters()
b = a.refresh_diagnosis_values(diag)