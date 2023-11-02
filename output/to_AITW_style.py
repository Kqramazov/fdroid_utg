import argparse

parser = argparse.ArgumentParser()

# 添加命令行参数
parser.add_argument("-check_js", type=bool, default=True)
parser.add_argument("-file_path", type=str, default="./bluepie.ad_silence.apk/")
parser.add_argument("-json_path", type=str, default=None)
parser.add_argument("-path", type=str, default="path.json")
# 解析命令行参数
args = parser.parse_args()

file_path = args.file_path
if args.check_js:
    content_to_check = "module.exports = utg;"

    with open(file_path+'utg.js', "r") as file:
        lines = file.readlines()

    last_line = lines[-1].strip()
    if last_line != content_to_check:
        # 如果最后一行不包含特定内容，则将其写入文件的最后一行
        with open(file_path+'utg.js', "a") as file:
            file.write("\n" + content_to_check)
        print("Content added to the last line of the file.")
    else:
        print("File already contains the 'module.exports = utg' in the last line.")


json_path = args.json_path
if not args.json_path:
    import subprocess

    node_command = [
        "node",
        "preprocess.js",
        file_path+'utg.js',
    ]
    process = subprocess.Popen(node_command, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    json_path = "info.json"

import json
import copy

all_paths = []
visited_nodes = {}
all_details = []


def dfs(utg, current_node_id, end_node_id, path, detail):
    path.append(current_node_id)
    current_node_idx = [index for index,node in enumerate(utg["nodes"]) if node["id"] == current_node_id][0]
    detail["nodes"].append(current_node_idx)
    if current_node_id == end_node_id and len(path) > 1:
        visited_nodes[current_node_id] = False
        all_paths.append(path.copy())
        all_details.append(copy.deepcopy(detail))
    elif current_node_id == end_node_id:
        visited_nodes[current_node_id] = False
    else:
        visited_nodes[current_node_id] = True

    outgoing_edges = [(index,edge) for index,edge in enumerate(utg["edges"]) if edge["from"] == current_node_id]
    for index, edge in outgoing_edges:
        neighbor_id = edge["to"]
        if not visited_nodes[neighbor_id]:
            detail["edges"].append(index)
            dfs(utg, neighbor_id, end_node_id, path, detail_format)

    path.pop()
    detail["nodes"].pop()
    if len(detail["edges"])>1:
        detail["edges"].pop()
    visited_nodes[current_node_id] = False


with open(json_path, "r", encoding="utf8") as file:
    utg = json.load(file)

for node in utg["nodes"]:
    visited_nodes[node["id"]] = False

first_node = next(node for node in utg["nodes"] if "FIRST" in node["label"])
first_node_id = first_node["id"]

last_node = next(node for node in utg["nodes"] if "LAST" in node["label"])
last_node_id = last_node["id"]

detail_format = {"nodes": [], "edges": []}
dfs(utg, first_node_id, last_node_id, [], detail_format)

# 保存到json文件中
if args.path:
    with open(file_path+args.path, "w") as file:
        json.dump(all_details, file,indent=4)
        print("paths saved.")

# 现在要写可视化了
# 你吗还是得写js
