# ObjcProjectDependencyVisualisation
ObjcProjectDependencyVisualisation is a project designed to help iOS developers improve their project structure. This repository contains a script which shows all dependencies in a project provided in the form of a directed graph. 

## How do I use it? 
1. Clone the project
2. Install pip3 (run: brew install python3)
3. (Optional) Activate [virtualenv](https://virtualenv.pypa.io/en/latest/)
4. pip3 install -r requirements.txt
5. python3 visualisation.py [-h] [-i IOSPROJECTPATH] [-o OUTPUTDIR]
                        [-f OUTPUTFILENAME] [-e OUTPUTFILEEXTENSION]

   optional arguments:
   * -h, --help            show this help message and exit
    * -i IOSPROJECTPATH, --iosProjectPath IOSPROJECTPATH
                          
                          path to iOS project to parse
    * -o OUTPUTDIR, --outputDir OUTPUTDIR
                          
                          folder to save result file to
    * -f OUTPUTFILENAME, --outputFilename OUTPUTFILENAME
                          
                          output file name
    * -e OUTPUTFILEEXTENSION, --outputFileExtension OUTPUTFILEEXTENSION
                          
                          output file extension

## What graph output types are supported?
‘canon’, ‘cmap’, ‘cmapx’, ‘cmapx_np’, ‘dia’, ‘dot’, ‘fig’, ‘gd’, ‘gd2’, ‘gif’, ‘hpgl’, ‘imap’, ‘imap_np’, ‘ismap’, ‘jpe’, ‘jpeg’, ‘jpg’, ‘mif’, ‘mp’, ‘pcl’, ‘pdf’, ‘pic’, ‘plain’, ‘plain-ext’, ‘png’, ‘ps’, ‘ps2’, ‘svg’, ‘svgz’, ‘vml’, ‘vmlz’, ‘vrml’, ‘vtx’, ‘wbmp’, ‘xdot’, ‘xlib’

## What types of dependencies are shown?
Currently a graph distinguishes four types of dependencies:
1. Red arrow - .pch file dependancy
2. Blue double-sided arrow - dependency cycle
3. Half-transparent node - external dependency
4. A node without in- or outarrows - isolated class

## Give me an example! 
Here you are:
![Example graph](https://github.com/D3migod/ObjcProjectDependencyVisualisation/blob/master/Pictures/dependencyGraph.jpg?raw=true)
