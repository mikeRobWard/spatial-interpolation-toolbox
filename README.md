<h1 align= "center">
Spatial Interpolation Toolbox
</h1>
<p align="center">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/mikeRobWard/spatial-interpolation-toolbox">
    <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/mikeRobWard/spatial-interpolation-toolbox">
    <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/mikeRobWard/spatial-interpolation-toolbox">
    <a href="https://github.com/mikeRobWard/spatial-interpolation-toolbox/issues">
        <img src="https://img.shields.io/github/issues/mikeRobWard/spatial-interpolation-toolbox"
            alt="Issues Open"></a>
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/mikeRobWard/spatial-interpolation-toolbox?style=social">
    <a href="https://twitter.com/intent/follow?screen_name=MWard_GIS">
        <img src="https://img.shields.io/twitter/follow/MWard_GIS?style=social&logo=twitter"
            alt="follow on Twitter"></a>
    <a href="https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2FmikeRobWard">
        <img alt="GitHub followers" src="https://img.shields.io/github/followers/mikeRobWard?style=social" alt="follow on GitHub">
        </a>
</p>


This is the home to Spatial Interpolation Toolbox, a graphical user-interface for interpolating geographic vector data.

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Installation and Setup](#installation-and-setup)
  - [Conda](#conda)
  - [Launching Spatial Interpolation Toolbox](#launching-spatial-interpolation-toolbox)
- [Description and Example Usage](#description-and-example-usage)
  - [Areal Weighting](#areal-weighting)
  - [Binary Method](#binary-method)
  - [Limiting Variable Method](#limiting-variable-method)
  - [N-Class Method](#n-class-method)
  - [Parcel Method](#parcel-method)
  - [Cadastral-Based Expert Dasymetric System](#cadastral-based-expert-dasymetric-system)
- [Troubleshooting](#troubleshooting)
- [Sources](#sources)
- [Special Thanks](#special-thanks)
- [License](#license)

## Introduction 

Spatial Interpolation Toolbox is a Python-based GUI that is able to interpolate spatial data in vector format. Spatial Interpolation Toolbox currently implements six different forms of spatial interpolation that are based on existing bodies of research

 Many forms of spatial interpolation are quite involved, and not easily accessible to GIS analyts. The goal of the Spatial Interpolation Toolbox is to offer a simplified and free way to interpolate spatial data.


## Installation and Setup 

Spatial Interpolation Toolbox depends on the following Python Packages:

- `geopandas`
- `pandas`
- `pyqt`

### Conda 

These packages depend on several low-level libraries for geospatial analysis, and can be challenging to install. For this reason, I recommend installing all of the dependencies using the [conda package manager](https://conda.io/en/latest/). Conda can be obtained by installing the [Anaconda Distribution](https://www.anaconda.com/products/individual) (A free Python distribution tailored for data science).

Once you have conda installed, launch Anaconda Prompt. Then, download this repo and change directory to the folder where you've downloaded the repo.

    git clone https://github.com/mikeRobWard/spatial-interpolation-toolbox

<!---->

    cd spatial-interpolation-toolbox

 Once there, create a new conda environment using the requirements.txt file, then activate the environment

    conda create --name spatial_toolbox --file requirements.txt

<!---->

    conda activate spatial_toolbox

### Launching Spatial Interpolation Toolbox

Now that you have the repo downloaded, conda installed, and your new environment running, you can launch Spatial Interpolation Toolbox from Anaconda Prompt using this command:

    python sp_int_toolbox.py

When you're finished, you can either close the GUI or press Ctrl+C in the Anaconda Prompt terminal.

## Description and Example Usage 

### Areal Weighting

The areal weighting method interpolates data into target polygons by using the ratio of intersected area to source area. It accepts two shapefiles – a source and target, a list of columns to be interpolated, and an optional suffix for the new name of the interpolated column in the target shapefile.  In the function, the source polygons are reindexed for summing later, and the areas of the source polygons are calculated.  The source and target are intersected, and the area of the intersected polygons is calculated.  Each intersected area is divided by the source area that encapsulates it for its areal weight.  The function then iterates through the selected columns and multiplies each value by the areal weight.  The target shapefile is returned with the interpolated columns.

For this example, we will be using open data from Philadelphia. The first shapefile is [crash data aggregated by Traffic Analysis zone (TAZ)](https://github.com/CityOfPhiladelphia/crash-data). The second shapefile is [Census Block Groups](https://www.opendataphilly.org/dataset/census-block-groups).

To begin, lets take a look at our two shapefiles in your preferred GIS viewer:

![aw_test](https://user-images.githubusercontent.com/67876029/139040847-80f13d49-a526-400a-928c-c0a3f422ac21.png)

In this example, we want to interpolate the number of crashes from TAZ in the source layer, to Census Block group in our target layer. We can see from the crash-data attributes that the field for aggregated crashes is named `Count_` 

Lets input the fields into Spatial Interpolation Toolbox:

![aw_inputs](https://user-images.githubusercontent.com/67876029/139040840-7d7aec91-edc9-4895-b095-d6454624fb91.JPG)

This will output a new shapefile to the directory that you chose. Lets open the new shapefile and compare it to our source shapefile, the crash data by TAZ:

![aw_output](https://user-images.githubusercontent.com/67876029/139040841-f38711a3-7b1d-4bdf-a709-4037d2f5eb70.png)

### Binary Method

This method accepts two shapefiles - a source shapefile which should contain the values that will be interpolated - and an ancillary shapefile containing a column with categorical geographic data such as land use types. The function also takes an input called `exclusion field` which allows the user to pass in the name of the column that contains the categorical data. Another input, `exclusion value(s)`, allows the user to pass in a list of values that appear within the `exclusion field` column. The values that are passed to `exclusion field` will be dropped from the ancillary shapefile before it is spatially intersected with the source shapefile so that the geography of the exclusionary values is not included in the intersected shapefile. This effectively turns the ancillary shapefile into a mask, which masks out the geography of all values that were passed to `exclusion value`. Returns a shapefile that has the masked areas clipped and the interpolation values disaggregated based on areal weight to the non-clipped zones.

In this example, we will use the [Philadelphia crash data](https://github.com/CityOfPhiladelphia/crash-data) again, but this time we will use a [land use shapefile](https://www.opendataphilly.org/dataset/land-use) as an ancillary data source. Let's take a look at our data:

![bm_test](https://user-images.githubusercontent.com/67876029/139185323-6125cfad-9faa-4032-8066-6e6bfc82d316.png)

This method will use the land use shapefile to mask out certain land use types from the crash data shapefile. Car crashes definitely don't happen on water, and there may be other land use types you'd want to mask out. For this example, let's assume that we want to interpolate the car crash data to just residential land use. Here's what our inputs will look like:

![bm_inputs](https://user-images.githubusercontent.com/67876029/139186210-63b601db-8ad1-4b18-8fda-75d803c3e0b7.JPG)

The field containing land use types is named `C_DIG1`, which contains a numbered value corresponding to the land use type. Residential corresponds to `1`, so we will exclude all other values. Land use shapefiles can contain hundreds of thousands of polygons, so be patient if you are processing a large area. The output of this interpolation should look similar to this:

![bm_output](https://user-images.githubusercontent.com/67876029/139191000-5ac637d4-0f8f-4959-877e-be3af21e4f7c.png)

### Limiting Variable Method

The limiting variable method interpolates data into disaggregated target polygons by setting thresholds to area-class categories.  It accepts two shapefiles – a source and ancillary (landuse most common), the area-class column in the ancillary shapefile, a dictionary for specifying thresholds to each area-class, a list of columns to be interpolated, an optional source identifier, and an optional suffix for the new name of the interpolated column.  Source polygons are reindexed and the area of each is calculated, an intersection is performed, and intersected areas are calculated.  The values of the dictionary are placed in a new threshold field and their keys are matched with the specified area-class category.  After the areal weight is found, a copy of the dictionary is made with values of none or 0 removed (these correspond to the class with no threshold).  Starting with the most restrictive, the specified columns are multiplied by their areal weight and clipped at the specified threshold per square unit.  The area that has been used is decremented from the source area and areal weight is recalculated.  The most restrictive class is then removed from the dictionary, and this process repeats until all the classes have been removed from the dictionary.  Finally, the remaining data is interpolated into the class with no restriction.  The target shapefile is returned with interpolated columns.

*Note: The thresholds for limiting variable are values per square unit. Your square units will vary depending on your projection.*

For this example, we can continue to use the [Philadelphia crash data](https://github.com/CityOfPhiladelphia/crash-data) and [Philadelphia land use data](https://www.opendataphilly.org/dataset/land-use). Our starting data will look like this:

![bm_test](https://user-images.githubusercontent.com/67876029/139185323-6125cfad-9faa-4032-8066-6e6bfc82d316.png)

And our inputs to Spatial Interpolation Toolbox will look something like this:

![lv_inputs](https://user-images.githubusercontent.com/67876029/139198079-bfdbef93-698d-4073-ad3b-71de6d4c384e.JPG)

And the output of the limiting variable function will look like this:

![lv_output](https://user-images.githubusercontent.com/67876029/139199364-c723ca5e-52c4-4a44-b4c8-2d6b7bf0daf6.png)

### N-Class Method

The n-class method interpolates data into disaggregated target polygons by assigning weights to area-class categories. It accepts two shapefiles – a source and ancillary (landuse most common), the area-class column in the ancillary shapefile, a dictionary for specifying percentages to each area-class, a list of columns to be interpolated, an optional source identifier, and an optional suffix for the new name of the interpolated column. Like areal weighting, source polygons are reindexed and the area of each is calculated.The dictionary values are placed into a new percentage field and their keys are matched with the specified area-class column. After intersecting, the areal weight for each new polygon is calculated and multiplied by its corresponding user-defined percentage. Each of those products is then divided by the sum of all the products per source polygon.  That fraction is called class_weight and is multiplied by column values for interpolation. The target shapefile is returned with interpolated columns.

For testing the n-class method, we can continue using the [Philadelphia crash data](https://github.com/CityOfPhiladelphia/crash-data) and [Philadelphia land use data](https://www.opendataphilly.org/dataset/land-use). Our starting data will look like this again:

![bm_test](https://user-images.githubusercontent.com/67876029/139185323-6125cfad-9faa-4032-8066-6e6bfc82d316.png)

The inputs for n-class method are very similar to the limiting variable method, but instead of passing in thresholds based on square units, we pass in percentages as a decimal for our thresholds. The percentages should add up to 100%, regardless of how many classes you are splitting between. For this example, we'll assign 75% to residential, 20% to commercial, and 5% to industrial:

![nc_inputs](https://user-images.githubusercontent.com/67876029/139210274-738327e1-6815-427f-846f-435e9a364eb6.JPG)

The output of this should look something like this:

![nc_output](https://user-images.githubusercontent.com/67876029/139212211-2f38b991-ef5a-4cbf-ab2e-bcb9f4e558a5.png)

### Parcel Method

The parcel based method disaggregates population from a large geography to the tax lot level by using residential area and number of residential units as proxies for population distribution. It accepts two shapefiles, a zone shapefile with `geography` and `population`, and a parcel shapefile which contain `geography`, `total units` per parcel, `residential units` per parcel, `building area` per parcel, and `residential area` per parcel. This method returns a shapefile at the tax lot level that has two calculated columns of disaggregated population, one based on residential area and one based on residential units.

### Cadastral-Based Expert Dasymetric System

The CEDS method works in conjunction with the parcel based method to determine whether adjusted residential area or number of residential units are a more accurate determinant when disaggregating population. The CEDS method accepts three shapefiles, two zone shapefiles that must nest with each other and contain `geometry` and `population`, and a parcel shapefile that contains `geometry`, `total units` per parcel, `residential units` per parcel, `building area` per parcel, and `residential area` per parcel. The parcel based method is called twice inside the CEDS method, once using the larger zone shapefile as an input, and once using the smaller nested zone shapefile as an input to the parcel method. The populations at the tax lot level that were derived from the large zone are then reaggregated back up to the small zone level. The absolute value of the difference between the large zone based populations and small zone estimated population are then calculated. Finally, for each parcel, if the absolute difference between the large zone based population and the small zone estimated population based on residential units is less than or equal to the absolute difference between the large zone population and small zone estimated population based on adjusted residential area, then the population estimate from the small zone based on residential units is determined to be the more accurate disaggregation. Otherwise, the population estimate from the small zone based on adjusted residential area is determined by the CEDS method to be the more accurate measure of disaggregation. This method returns one shapefile at the tax lot level with the parcel based method calculations, plus an additional column that contains the selected outcome of the CEDS method.

## Troubleshooting

Common issues:

- Projection - Spatial Interpolation Toolbox will not reproject shapefiles for you. You must ensure that your shapefiles are in the correct projections before using this tool.
- Field type - The fields that you interpolate must be stored numerically (int / float). If you pass in a field that's stored as a string it may fail, even if it actually only contains numerical values.
- Error Handling - In addition from some built-in error handling, Spatial Interpolation Toolbox will print exception messages to Anaconda prompt's terminal window. If the program fails during interpolation and the cause isn't clear, check the terminal for insight.

If you encounter a problem or bug that isn't answered here, please open an issue 👍

## Sources

- Mennis, Jeremy (2009). Dasymetric Mapping for Estimating Population in Small Areas.
    Geography Compass, pp 727-745

- Hultgren, T. and J. Mennis (2006). Intelligent Dasymetric Mapping and Its Application to Areal
    Interpolation. Cartography and Geographic Information Science 33, pp 179-194

- Maantay, Juliana Astrud, Andrew R. Maroko, and Christopher Herrmann. "Mapping population distribution in the urban environment: The cadastral-based expert dasymetric system (CEDS)." Cartography and Geographic Information Science 34.2 (2007): 77-102.

- Cory L. Eicher & Cynthia A. Brewer (2001) Dasymetric Mapping and ArealInterpolation: Implementation and Evaluation, Cartography and Geographic Information Science,28:2, 125-138, DOI: 10.1559/152304001782173727

## Special Thanks

- [John Fitzgibbons](https://github.com/jjfitzgib) - John contributed the code behind the Areal Weighting, Limiting Variable, and N-Class methods
- [Lee Hachadoorian](https://github.com/leehach) - Lee helped formulate the idea for this project, and provided great feedback along the way

## License

    Spatial Interpolation Toolbox
    Copyright (C) 2021 Michael Ward

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.