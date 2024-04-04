#!/bin/bash
echo "Please enter the lib/project names you want to analyze your code against (separated by space):"
read -a libnames
echo "Path of the repositories to be analysed"
read path

for libname in "${libnames[@]}"
do
    export PROJ=$libname
    export LXR_PROJ_DIR=/home/bsp_projects/elixir-data/projects/
    export LXR_REPO_DIR=$LXR_PROJ_DIR/$PROJ/repo
    export LXR_DATA_DIR=$LXR_PROJ_DIR/$PROJ/data
    # Provide necessary arguments for output, mrepo, compiler, api, and xrs
    # Be mindful of the spacing and line breaks
    echo "Please select the version for $libname:" 
    bash /home/bsp_projects/elixir/script.sh list-tags
    read -p "> " version
    ./query_sys.py  \
        --output=./output-$libname \
        --mrepo=$path \
        --compiler=/usr/include/ \
        --api \
        --sys \
        --version=$version
done    
