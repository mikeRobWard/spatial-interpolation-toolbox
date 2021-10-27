# Spatial Interpolation Toolbox

Graphical user-interface for interpolating geographic vector data

## Introduction
---------------

Spatial Interpolation Toolbox is a Python-based GUI that is able to interpolate spatial data in vector format. Spatial Interpolation Toolbox currently implements six different forms of spatial interpolation that are based on existing bodies of research

 Many forms of spatial interpolation are quite involved, and not easily accessible to GIS analyts. The goal of the Spatial Interpolation Toolbox is to offer a simplified and free way to interpolate spatial data.

 ## Installations & Setup
 ------------------

Spatial Interpolation Toolbox depends on the following Python Packages:

- `geopandas`
- `pandas`
- `pyqt`

### Conda 
------

These packages depend on several low-level libraries for geospatial analysis, and can be challenging to install. For this reason, I recommend installing all of the dependencies using the [conda package manager](https://conda.io/en/latest/). Conda can be obtained by installing the [Anaconda Distribution](https://www.anaconda.com/products/individual) (A free Python distribution tailored for data science).

Once you have conda installed, launch Anaconda Prompt. Then, download this repo and change directory to the folder where you've downloaded the repo.

>git clone https://github.com/mikeRobWard/spatial-interpolation-toolbox

>cd spatial-interpolation-toolbox

 Once there, create a new conda environment using the requirements.txt file, then activate the environment

>conda create --name spatial_toolbox --file requirements.txt

>conda activate spatial_toolbox

### Launching Spatial Interpolation Toolbox
------------------------------------

Now that you have the repo downloaded, conda installed, and your new environment running, you can launch Spatial Interpolation Toolbox from Anaconda Prompt using this command:

> python sp_int_toolbox.py

When you're finished, you can either close the GUI or press Ctrl+C in the Anaconda Prompt terminal.

## Example Usage
----------------

### Areal Weighting


For this example, we will be using open data from Philadelphia. The first shapefile is [crash data aggregated by Traffic Analysis zone (TAZ)](https://github.com/CityOfPhiladelphia/crash-data). The second shapefile is [Census Block Groups](https://www.opendataphilly.org/dataset/census-block-groups).

To begin, lets take a look at our two shapefiles in your preferred GIS viewer:

![aw](testing_data/aw/aw_test.png)

In this example, we want to interpolate the number of crashes from TAZ in the source layer, to Census Block group in our target layer. We can see from the crash-data attributes that the field for aggregated crashes is named `Count_` 

Lets input the fields into Spatial Interpolation Toolbox:


![aw_inputs](testing_data/aw/aw_inputs.jpg)

This will output a new shapefile to the directory that you chose. Lets open the new shapefile and compare it to our source shapefile, the crash data by TAZ:

![aw_output](testing_data/aw/aw_output.png)

## Troubleshooting
------------------

Common issues:

- Projection - Spatial Interpolation Toolbox will not reproject shapefiles for you. You must ensure that your shapefiles are in the correct projections before using this tool
- Field types - The fields that you interpolate must be stored numerically (int / float). If you pass in a field that's stored as a string it may fail, even if it actually only contains numerical values.

If you encounter a problem or bug that isn't answered here, please open an issue 👍


## More Usage Documentation Coming Soon!

