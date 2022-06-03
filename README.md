# unstructured-env-simulator

The package gazebo_unstructured_env generates simulation environments for Gazebo.

Assets are implanted following a Poisson Cluster Point Process and can be either trees or geometrical shapes. A random scaling factor is applied on the asset scale and orientation.

<img title="Simu" src="pics/husky-in-simu.png" alt="Simu" width="600">

## Example

Two example environments are provided (unstructured_1 and structured_1), as well as a library of 15 trees.

Link: https://secure.georgiatech-metz.fr/owncloud/index.php/s/NySA2wZxaJa4kqb

The environments should be put here: `models/XP_WORLD_NAME/meshes/`

The trees here: `trees_models`

`roslaunch gazebo_unstructured_env world_from_stl.launch xp_name:=XP_WORLD_NAME`


## To create a new world

The list of asset can be generated as a csv with `draw_implantation.py`

Then, a single stl file can be generated with Blender (<=2.79) (example in `blender_script.py`)

Create a new world with `./create_new_world.sh XP_WORLD_NAME`
The stl generated with Blender should be `models/XP_WORLD_NAME/meshes/XP_WORLD_NAME.stl`

