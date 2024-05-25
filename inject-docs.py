#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import json5

#
# Try to figure out what the extension name is from CMakeLists.txt in the root
# folder
#

extension_name = None

with open("CMakeLists.txt", "r") as f:
    for line in f.readlines():
        m = re.match(r"project\((\w+)\)", line)
        if m:
            extension_name = m.group(1)
            break

if extension_name is None:
    print("ERROR: Could not find extension name in CMakeLists.txt")
    exit(1)

print("Found extension name", extension_name)

#
# Traverse source directory and collect exported functions
#

docs = {} # Mapping from "function_name" to JSDoc
funcs = [] # List of found "YYEXPORT void" functions
src_dir = "src" # Folder containing the extension's .cpp files

for fname in os.listdir(src_dir):
    if not fname.endswith(".cpp"):
        continue
    fpath = os.path.join(src_dir, fname)
    print("Parsing file", fpath)
    docs_current = ""
    with open(fpath, "r") as f:
        func_name = None
        for line in f.readlines():

            # Found function definition
            m = re.match(r"YYEXPORT void (\w+)", line)
            if m:
                fname = m.group(1)
                funcs.append(fname)
                print("Found function", fname)

            # Found docs for a function
            m = re.match(r"/// @func (\w+)", line)
            if m:
                func_name = m.group(1)
                print("Found JSDoc for", func_name)

            # Collect docs
            if line.startswith("///") and not line.startswith("////"):
                docs_current += line
            elif docs_current != "":
                if func_name is not None:
                    docs[func_name] = docs_current
                docs_current = ""

    if docs_current != "":
        docs[func_name] = docs_current

#
# Load the .yy extension file
#

ext_path = os.path.join("extensions", extension_name, f"{extension_name}.yy")
print(f"Loading {ext_path}...")
with open(ext_path) as f:
    ext_str = f.read()
    ext_json = json5.loads(ext_str)

functions = []
order = []
total = 0

for f in funcs:
    if f == "YYExtensionInitialise":
        continue

    print("Injecting function", f)

    help_line = ""
    d = ""

    if f in docs:
        d = docs[f]
        m = re.findall(r"/// @func ([^\n]+)", d)
        if m:
            help_line = m[0]

    functions.append({
      "$GMExtensionFunction": "",
      "%Name": f,
      "argCount": 0,
      "args": [],
      "documentation": d,
      "externalName": "",
      "help": help_line,
      "hidden": False,
      "kind": 1,
      "name": f,
      "resourceType": "GMExtensionFunction",
      "resourceVersion": "2.0",
      "returnType": 1
    })

    # order.append({
    #   "name": f,
    #   "path": f"extensions/{extension_name}/{extension_name}.yy"
    # })

    total += 1

#
# Insert collected functions to the .yy file
#

for f in ext_json["files"]:
    if f["filename"] in [f"{extension_name}.dll", f"lib{extension_name}.dylib", f"lib{extension_name}.so"]:
        f["functions"] = functions
        f["order"] = order
        f["usesRunnerInterface"] = True
        break

with open(ext_path, "w") as f:
    json5.dump(ext_json, f, quote_keys=True, indent=2)

print("Total functions injected:", total)
