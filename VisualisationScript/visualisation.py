#!/usr/bin/env python3

import sys
import os
import re
from os.path import basename
import argparse
from functional import seq
import pygraphviz as pgv

class ProjectParser:
    def __init__(self, path: str):
        self.path = path
    
    def parseFile(path):
        importsRegex = re.compile("^\s*#(?:import|include)\s+\"(?P<filename>\S*)(?P<extension>\.(?:h|hpp|hh))?\"")
        for fileLine in open(path):
            imports = re.search(importsRegex, fileLine)
            if imports:
                filenames = imports.group('filename')
                extensions = imports.group('extension') if imports.group('extension') else ""
                yield (filenames + extensions) if extensions else filenames
    
    def findCertainTypeDependencies(path, certainType):
        dependencies = {}

        for root, dirs, files in os.walk(path):
            certainTypeFiles = (file for file in files if file.endswith(certainType))

            for file in certainTypeFiles:
                filename = os.path.splitext(file)[0]

                if filename not in dependencies:
                    dependencies[filename] = set()

                path = os.path.join(root, file)

                for importFilename in ProjectParser.parseFile(path):
                    if importFilename != filename and '+' not in importFilename and '+' not in filename:
                        importFilename = os.path.splitext(importFilename)[0]
                        dependencies[filename].add(importFilename)

        return dependencies
    
    def findProjectDependencies(self, types):

        dependencies = {}

        for cirtainType in types:
            cirtainTypeDependencies = ProjectParser.findCertainTypeDependencies(self.path, cirtainType)
            for (parent, children) in cirtainTypeDependencies.items():
                if not parent in dependencies:
                    dependencies[parent] = set()
                dependencies[parent] = dependencies[parent].union(children)

        return dependencies
    
    def findPchDependencies(self):
        return ProjectParser.findCertainTypeDependencies(self.path, '.pch')
    
    
    def findDependencyCicles(dependencies):
        dependencyCicles = set()

        for parent, children in dependencies.items():
            for child in children:
                if child in dependencies and parent in dependencies[child]:
                    if (parent, child) not in dependencyCicles and (child, parent) not in dependencyCicles and parent != child:
                        dependencyCicles.add((parent, child))

        return dependencyCicles
    
    def findUntraversedFiles(dependencies):
        untraversedFiles = set()

        for parent, children in dependencies.items():
            for child in children:
                if not child in untraversedFiles and not child in dependencies:
                    untraversedFiles.add(child)

        return untraversedFiles

class GraphDrawer:
    def __init__(self, path):
        self.path = path
    
    def drawGraph(self, nodes, edges, untraversedNodes, pchNodes, referenceCycleNodes):
        graph = pgv.AGraph(directed=True, strict=True, rankdir='TD', name="ContainerView")
        graph.node_attr['shape'] = 'rectangle'

        seq(nodes).for_each(lambda n: graph.add_node(n))
        seq(untraversedNodes).for_each(lambda n: graph.add_node(n, color='grey', style='dashed', fontcolor='gray'))
        seq(edges).for_each(lambda e: graph.add_edge(e[0], e[1]))
        seq(pchNodes).for_each(lambda e: graph.add_edge(e[0], e[1], color = 'red'))
        seq(referenceCycleNodes).for_each(lambda e: graph.add_edge(e[0], e[1], color='blue', dir='both'))

        graph.layout('dot')
        graph.draw(self.path)

class DependenciesVisualizer:
    def __init__(self, inputPath: str, outputPath: str, name: str, extension: str):
        output = os.path.join(outputPath, name + extension)
        self.path = output
        self.projectParser = ProjectParser(inputPath)
        self.graphDrawer = GraphDrawer(output)
    
    def visualizeDependencies(self):
        searchTypes = ['.h', '.hh', '.hpp', '.m', '.mm', '.c', '.cc', '.cpp']
        dependencies = self.projectParser.findProjectDependencies(searchTypes)
        dependencyCicles = ProjectParser.findDependencyCicles(dependencies)
        untraversedFiles = ProjectParser.findUntraversedFiles(dependencies)
        pchFiles = self.projectParser.findPchDependencies()

        nodes = []
        edges = []

        for parent, children in dependencies.items():
            if children:
                children.discard(parent)

            if len(children) == 0:
                nodes.append(parent)

            for child in children:
                if not ((parent, child) in dependencyCicles or (child, parent) in dependencyCicles):
                    edges.append((parent, child))
        self.graphDrawer.drawGraph(nodes, edges, untraversedFiles, pchFiles, dependencyCicles)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--iosProjectPath", required=False, default='../GraphSampleProject/ContainerView/DemoContainerView', help="path to iOS project to parse")
    parser.add_argument("-o", "--outputDir", required=False, default='.', help="folder to save result file to")
    parser.add_argument("-f", "--outputFilename", required=False, default='dependencyGraph', help="output file name")
    parser.add_argument("-e", "--outputFileExtension", required=False, default='.pdf', help="output file extension")
    args= parser.parse_args()

    dependenciesVisualizer = DependenciesVisualizer(args.iosProjectPath, args.outputDir, args.outputFilename, args.outputFileExtension)
    dependenciesVisualizer.visualizeDependencies()