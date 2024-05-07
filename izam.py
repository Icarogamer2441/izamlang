import time
import random
import subprocess

variables = {}
functions = {}
ifs = []
pycodes = {}

def interpret(code):
    lines = code.split("\n")

    for checkline in lines:
        if checkline.startswith("start Main run"):
            for line in lines:
                if line.startswith("Output"):
                    outputtype = line.split(".")[1].strip("\"\'")
                    if outputtype.startswith("PrintMsg"):
                        message = line.split(" >> ")[1].split(" << ")[0].strip("\"\'")
                        endtype = line.split(" << ")[1].strip("\"\'")
                        if endtype == "unicline":
                            print(message, end="")
                        elif endtype == "newline":
                            print(message)
                        else:
                            print(f"uknown endtype={endtype}. use unicline or newline")
                    elif outputtype.startswith("Input"):
                        varname = line.split(" << ")[1].strip(" << ")[0].strip("\"\'")
                        question = line.split(" << ")[1].strip(" >>")[0].strip("\"\'")
                        variables[varname] = input(question)
                    elif outputtype.startswith("PrintVar"):
                        varname = line.split(" >> ")[1].split(" << ")[0].strip("\"\'")
                        endtype = line.split(" << ")[1].strip("\"\'")
                        if endtype == "unicline":
                            print(variables.get(varname), end="")
                        elif endtype == "newline":
                            print(variables.get(varname))
                        else:
                            print(f"uknown endtype={endtype}. use unicline or newline")
                elif line.startswith("func"):
                    funcname = line.split("(")[1].split(")")[0].strip("\"\'")
                    functions[funcname] = []
                    for code in lines:
                        if code.startswith(f"{funcname}"):
                            restcode = code.split("@ ")[1].split(" @codend")[0].strip("\"\'")
                            functions[funcname].append(restcode)
                        elif code.startswith(f"endfunc{funcname}"):
                            break
                elif line.startswith("int"):
                    name = line.split(" ")[1].split(" = ")[0].strip("\"\'")
                    value = line.split(" = ")[1].split(" << endvar")[0].strip()
                    variables[name] = int(value)
                elif line.startswith("string"):
                    name = line.split(" ")[1].split(" = ")[0].strip("\"\'")
                    value = line.split(" = ")[1].split(" << endvar")[0].strip()
                    variables[name] = value
                elif line.startswith("boolean"):
                    name = line.split(" ")[1].split(" = ")[0].strip("\"\'")
                    value = line.split(" = ")[1].split(" << endvar")[0].strip()
                    if value == "true":
                        variables[name] = True
                    elif value == "false":
                        variables[name] = False
                    else:
                        print("Unknown boolean type")
                elif line.startswith("float"):
                    name = line.split(" ")[1].split(" = ")[0].strip("\"\'")
                    value = line.split(" = ")[1].split(" << endvar")[0].strip()
                    variables[name] = float(value)
                elif line.startswith("callfunc"):
                    funcname = line.split("{")[1].split("}")[0].strip("\"\'")
                    funcarray = functions.get(funcname)
                    funccode = "\n".join(funcarray)
                    interpret(funccode)
                elif line.startswith("nifs"):
                    varname1 = line.split("(")[1].split(",")[0].strip("\"\'")
                    varname2 = line.split(",")[1].split(") >> ")[0].strip("\"\'")
                    ifname = line.split(") >> ")[1].strip("\"\'")
                    ifs = []
                    if variables.get(varname1) == variables.get(varname2):
                        for code in lines:
                            if code.startswith(f"{ifname}"):
                                restcode = code.split("$ ")[1].split(" $codend")[0].strip("\"\'")
                                ifs.append(restcode)
                            elif code.startswith(f"end{ifname}"):
                                interpret("\n".join(ifs))
                                break
                elif line.startswith("uifs"):
                    varname1 = line.split("(")[1].split(") >> ")[0].strip("\"\'")
                    ifname = line.split(") >> ")[1].strip("\"\'")
                    ifs = []
                    if variables.get(varname1):
                        for code in lines:
                            if code.startswith(f"{ifname}"):
                                restcode = code.split("$ ")[1].split(" $codend")[0].strip("\"\'")
                                ifs.append(restcode)
                            elif code.startswith(f"end{ifname}"):
                                interpret("\n".join(ifs))
                                break
                elif line.startswith("import"):
                    izamfilename = line.split("[")[1].split("]")[0].strip("\"\'")
                    with open(izamfilename + ".izam", "r") as fi:
                        interpret(fi.read())
                elif line.startswith("pyfunc"):
                    pyfuncname = line.split("(")[1].split(")")[0].strip("\"\'")
                    pycodes[pyfuncname] = []
                    for code in lines:
                        if code.startswith(f"{pyfuncname}"):
                            restcode = code.split("! ")[1].split(" !codend")[0].strip("\"\'")
                            pycodes[pyfuncname].append(restcode)
                        elif code.startswith(f"endpyfunc{pyfuncname}"):
                            break
                elif line.startswith("callpyfunc"):
                    pyfuncname = line.split("{")[1].split("}")[0].strip("\"\'")
                    pyfuncarray = pycodes.get(pyfuncname)
                    pyfunccode = "\n".join(pyfuncarray)
                    exec(pyfunccode)
                elif line.startswith("wait"):
                    times = line.split("(")[1].split(")")[0].strip("\"\'")
                    time.sleep(int(times))
                elif line.startswith("system"):
                    command = line.split("(")[1].split(")")[0].strip("\"\'")
                    subprocess.run(command, shell=True)
def execute_file(filename):
    if filename.endswith(".izam"):
        with open(filename, "r") as f:
            interpret(f.read())
    else:
        print("file extension not accepted, use .izam has file extension")

filename = input("what's your file? > ")
execute_file(filename)
