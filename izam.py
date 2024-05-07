import time
import subprocess
import platform

variables = {}
functions = {}
ifs = []
pycodes = {}
repeats = {}

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
                    with open(pyfuncname + ".py", "w") as fi:
                        fi.write(pyfunccode)
                    if platform.system() == "Windows":
                        subprocess.run(f"python {pyfuncname + '.py'}", shell=True)
                    else:
                        subprocess.run(f"python3 {pyfuncname + '.py'}", shell=True)
                elif line.startswith("wait"):
                    times = line.split("(")[1].split(")")[0].strip("\"\'")
                    time.sleep(int(times))
                elif line.startswith("File"):
                    filetype = line.split(".")[1].strip("\"\'")
                    if filetype.startswith("Read"):
                        filename = line.split("(")[1].split(",")[0].strip("\"\'")
                        varname = line.split(",")[1].split(")")[0].strip("\"\'")
                        with open(filename, "r") as fi:
                            content = fi.read()
                        variables[varname] = content
                    elif filetype.startswith("Write"):
                        filename = line.split("(")[1].split(",")[0].strip("\"\'")
                        varname = line.split(",")[1].split(")")[0].strip("\"\'")
                        with open(filename, "w") as fi:
                            fi.write(variables.get(varname))
                    elif filetype.startswith("Append"):
                        filename = line.split("(")[1].split(",")[0].strip("\"\'")
                        varname = line.split(",")[1].split(")")[0].strip("\"\'")
                        with open(filename, "a") as fi:
                            fi.write(variables.get(varname))
                    elif filetype.startswith("ReadPrint"):
                        filename = line.split("(")[1].split(")")[0].strip("\"\'")
                        with open(filename, "r") as fi:
                            content = fi.read()
                        print(content)
                elif line.startswith("repeat"):
                    times = line.split("(")[1].split(") >> ")[0].strip("\"\'")
                    repeatname = line.split(") >> ")[1].strip("\"\'")
                    repeats[repeatname] = []
                    for code in lines:
                        if code.startswith(f"{repeatname}"):
                            restcode = code.split("# ")[1].split(" #codend")[0].strip("\"\'")
                            repeats[repeatname].append(restcode)
                        elif code.startswith(f"end{repeatname}"):
                            interpret("\n".join(repeats[repeatname]))
                            break
                elif line.startswith("break"):
                    break
def execute_file(filename):
    if filename.endswith(".izam"):
        with open(filename, "r") as f:
            interpret(f.read())
    else:
        print("file extension not accepted, use .izam has file extension")

filename = input("what's your file? > ")
execute_file(filename)
