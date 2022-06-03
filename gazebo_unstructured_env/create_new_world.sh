#!/bin/sh

if [ $# -eq 0 ]; then
    echo "Usage"
    echo "  1. xp name "
    exit 0
fi

if [ $# -lt 1 ]; then
    echo "Bad number of arguments"
    exit 0
fi


xp_name=$1

model_dir=models/"$xp_name"


if  [ -d "$model_dir" ]; then
    echo "This experience already exists, choose another name."
    exit 0
else
    cp -r models/world_template $model_dir
    sed -i "s/world_template/$xp_name/g" "$model_dir"/model.config
    sed -i "s/world_template/$xp_name/g" "$model_dir"/model.sdf
    rm -f "$model_dir"/meshes/world_template.stl
    cp world/world_template.world world/$xp_name.world
    sed -i "s/world_template/$xp_name/g" world/$xp_name.world
    echo "new world create successfully, do not forget to put your stl file in
    "$model_dir"/meshes/"
fi


