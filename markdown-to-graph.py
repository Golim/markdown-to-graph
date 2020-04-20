#!/usr/bin/env python3

import subprocess
import sys

if len(sys.argv) < 2:
    print("USAGE: python markdown_to_graph.py input.md output.png")
    exit()

markdown = open(sys.argv[1], "r")
dot = open("/tmp/graph.dot", "w")

# Lines of the markdown file
lines = markdown.readlines()
markdown.close()

# The graph of the markdown file
graph = {
    0: []
}

# Titles of nodes
titles = {
    0: lines[0].split("# ")[1].replace('\n', '')
}

# Contains the previous father node for every title level
# Note that for simplicity I don't care that arrays starts at 0:
#   I just don't use the first element of the array
fathers = [0, 0, 0, 0, 0, 0, 0]

def read_line(line_number, count):
    global fathers, lines

    # Skip non-title lines
    while line_number < len(lines) and not lines[line_number].startswith('#'):
            line_number += 1

    # Check if in range
    if line_number >= len(lines):
        return

    line = lines[line_number]

    # If a line is a title
    if line.startswith('#'):
        count += 1

        # Check which level of title is this line
        level = len(line.split(" ")[0])

        # This is the previous father for this level
        fathers[level] = count

        # Save the title for 'count' node
        titles[count] = line.split("# ")[1].replace('\n', '')

        # Add 'count' node to level - 1 father
        #print("line", count, "is a child of", fathers[level - 1], " -> ", line)

        if count not in graph:
            graph[count] = []

        graph[fathers[level - 1]].append(count)

    read_line(line_number + 1, count)

# Converts my graph in a DOT (graph description language) file
def graph_to_dot():
    dot.write("digraph markdown {\n")

    # Iterate through keys in graph
    for key in graph:
        children = graph[key]

        for child in children:
            dot.write("    \"" + titles[key] + "\" -> \"" + titles[child] + "\";\n")
    
    dot.write("}")

# Read from line 1, because line 0 contains the only h1
read_line(1, 0)

# Write the dot file
graph_to_dot()
dot.close()

# Print the dot file to a png file
subprocess.run(["dot", "-Tpng", "/tmp/graph.dot", "-o", sys.argv[2]])