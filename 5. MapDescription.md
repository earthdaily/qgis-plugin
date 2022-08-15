# Map Description

## NDVI Map

The in-season NDVI map assess crop conditions variablity within the field. The Normalized Difference Vegetation Index (NDVI) quantifies vegetation by measuring the difference between near-infrared (which vegetation strongly reflects) and red light (which vegetation absorbs). 

<br>
<p align="center">
  <img width="400" height="300" src="https://raw.githubusercontent.com/GEOSYS/qgis-plugin-doc/master/pictures/Capture%20d’écran%202022-05-16%20112454.png">
</p>

NDVI is the most common index that analysts use in remote sensing. NDVI is a standardized way to measure healthy vegetation. When you have high NDVI values, you have healthier vegetation. When you have low NDVI, you have less or no vegetation. 

With the NDVI map API you can adjust the min and max values of the map;

----------------------
### EVI map

<br>
<p align="center">
  <img width="400" height="300" src="https://raw.githubusercontent.com/GEOSYS/qgis-plugin-doc/master/pictures/EVI.png">
</p>



----------------------
### CVI map


<br>
<p align="center">
  <img width="400" height="300" src="https://raw.githubusercontent.com/GEOSYS/qgis-plugin-doc/master/pictures/Capture%20d’écran%202022-05-16%20112530.png">
</p>


----------------------
### GNDVI map


<br>
<p align="center">
  <img width="400" height="300" src="https://raw.githubusercontent.com/GEOSYS/qgis-plugin-doc/master/pictures/GNDVI.png">
</p>


----------------------
### CVIN 
The in-season Chlorophyll Vegetation Normalized indexed map is a vegetation index correlated to plant chlorophyll activity. It is used for late-cycle nitrogen management advice on cereals that aim to improve the protein content of the crop.

<br>
<p align="center">
  <img width="400" height="300" src="https://raw.githubusercontent.com/GEOSYS/qgis-plugin-doc/master/pictures/CVIN.png">
</p>

### S2REP map 
The in-season Sentinel2 Red-Egde Position indexed map is used to estimate the rate of nitrogen uptake by cereals.

<br>
<p align="center">
  <img width="400" height="300" src="https://raw.githubusercontent.com/GEOSYS/qgis-plugin-doc/master/pictures/S2REP_map.png">
</p>

With the rate of nitrogen uptake and the biomass of the crop (estimated using LAI), the user can calculates the nitrogen nutrition index (NNI) and the nitrogen requirement of the crop at T time. 


## Yield Goal Map

The Yield Goal Map is used to define the yield goal distribution inside the field, based on the field variability. User defines the yield he wants to target for the coming season. The legend is dynamic (going from red to blue), this means the minimum and maximum of the legend is adapted for each field.

<br>
<p align="center">
  <img width="400" height="300" src="https://raw.githubusercontent.com/GEOSYS/qgis-plugin-doc/master/pictures/YGM.png">
</p>

This information is used by the grower during the establishment of the inputs plan prior to the season: he can push areas with high potential and decrease areas with low potential. The YGM is used to create variable rates application maps. Based on the yield potential variability of the field, the user can modulate the inputs application on the field.

The user has access to past images of vegetation peak period and will choose an archive map with same crop.  The user can choose between different weather context to build a scenario and define his yield goal map.

## Yield Variability Map

The Yield Variability Map shows the yield variability of the field based on an historic average yield. The legend is dynamic (going from red to blue), this means the minimum and maximum of the legend is adapted for each field.

<br>
<p align="center">
  <img width="400" height="300" src="https://raw.githubusercontent.com/GEOSYS/qgis-plugin-doc/master/pictures/YPM.png">
</p>


This information is used by the grower during the establishment of the inputs plan prior to the season: he can push areas with high potential and decrease areas with low potential. The YVM is used to create variable rates application maps. Based on the yield potential variability of the field, the user can modulate the inputs application on the field.

The user has access to past images of vegetation peak period and will choose an archive map with same crop.  The user can choose between different weather context to build a scenario and define his yield map.

## Organic Matter Map

The Organic Matter Variability Map is used to represent the relative organic matter distribution in the field (i.e. the nitrogen available within the soil).

The legend is dynamic (going from red to blue), this means the minimum and maximum of the legend is adapted for each field.

<br>
<p align="center">
  <img width="400" height="300" src="https://raw.githubusercontent.com/GEOSYS/qgis-plugin-doc/master/pictures/OM_part2.png">
</p>

This information is used by the grower during the establishment of the <Strong>fertilization strategy</Strong>, to plan and modulate the nitrogen fertilization.

The Organic Matter Variability Map, combined with a Yield Variability or Yield Goal Map, is used to create <Strong>variable rate nitrogen application map</Strong>. The yield goal map allows setting the nitrogen needs in each area of the field.  By taking into account the nitrogen needs to reach the yield goal and the nitrogen already available in the soil, the user can <Strong>modulate the nitrogen fertilization</Strong> to be applied in the field.

## SAMZ Map

The SAMZ API allows to automatically create a 5 zones SAMZ map based on the most relevant archive imagery of vegetation images:  

- The 2 last context
- The 2 last wet context images
- The last one bare soil image

<br>
<p align="center">
  <img width="400" height="300" src="https://raw.githubusercontent.com/GEOSYS/qgis-plugin-doc/master/pictures/SAMZ.png">
</p>

SAMZ analyzes the crops’ vegetation behavior from satellite imagery archives representing multiple years of variable weather patterns and delineates areas with a different behavior.

The SAMZ map represents the permanent variability of the field, derived from multiple crop seasons. It shows a spatial representation of the limiting factors of soil through the analysis of the crop-weather-soil interaction.

The SAMZ map is comparable to the classification of several years of yield maps.

The SAMZ maps uses are numerous because they depend on the production limiting factors of the field: 

- The baseline inputs modulation (P, K, CaO...) and the seeds modulation are the first uses as they directly related to the "quality" of the soil.
- The nitrogen variable fertilization plan also allows to take into account the variability of the nitrogen restitution of soil before the crop season and in-season due to better sampling of leaf analyzes to assess the index of nitrgoen nutrition of plants and thus to adjust the provided application dose.

The SAMZ map is sent with the following statistics values on the zones:
- Productivity index for the map and by zone. It corresponds to the average, for each zone, of NDVI calculated on all vegetation images*100.
- Field variability level (low, medium, or high) for the map and by zone
- The most variable class: the class that has the higher NDVI values variability.
- The two classes with the highest inter-class variability: for each class, the Euclidean distance from each of the other class is calculated; then the two farthest classes are identified. 

### Soil Map

The soil map provides soil data and information produced by the National Cooperative Soil Survey.

----------------------



### Elevation and Slope map

the elevation map provide additional element to analyse the fields. Elevations are usually measured in meters or feet with reference to the sea level. It can be either above the sea level or below the sea level. Elevation in a map is shown using contour lines, bands of same colours or by numerical values giving the exact elevation details. The slope map is a topographic map showing changes in elevation on a highly detailed level.

![elevation.png](https://stoplight.io/api/v1/projects/cHJqOjE0OTYw/images/rXGwpJnZNkY)
