# Main Heading

|                            |                                                                                                                                                                              |
|:--------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Date                       | 09/12/2024                                                                                                                                                                   |
| Tester                     | Jeff Osundwa                                                                                                                                                                 |
| Documentation              | [Link](https://)                                                                                                                                                             |
| Test System Specifications | [![image](https://github.com/user-attachments/assets/8794b899-272f-48cf-8b61-ead2e335b559)](https://github.com/user-attachments/assets/8794b899-272f-48cf-8b61-ead2e335b559) |
| Test Description           | Description of work required - Follow the API guide outlined in the documentation and perform the steps to see if the correct output is received                             |

### Result Key

🟢 = Pass / Output as expected  
🟡 = Output received but not what was expected / Process failed one or more times before pass  
🔴 = Fail / Could not process  
⚠️ = Error / Crash  

> *All images in the table below can be clicked on to get an enlarged view of the image*

### Tests Results

| No  | Description                          | Status | Notes                                                                                                                                         |
|:---:|:------------------------------------ |:------:|:--------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Coverage search**                  | 🟢     |                                                                                                                                               |
|     | `COLOR_COMPOSITION`<br/>`MASK`: Auto | 🟢     | ![](img/color_composition_1.png)                                                                                                              |
|     | Result:                              | 🟢     | Output `200 OK` <br> [![image](img/color_composition_2.png)](https://github.com/user-attachments/assets/cf2487ae-68ba-45e9-abab-c6e7280cc39a) |
|     | `MASK`: None                         | 🟢     | ![](img/color_composition_4.png)                                                                                                              |
|     | `MASK`: ACM                          | 🟢     | ![](img/color_composition_5.png)                                                                                                              |
|     | `MASK`: All                          | 🟢     | ![](img/color_composition_6.png)                                                                                                              |
|     | `MASK`: Native                       | 🟢     | ![](img/color_composition_7.png)                                                                                                              |
| 2   | **Coverage search**                  |        |                                                                                                                                               |
|     | CVI                                  | 🟢     | ![CVI error](img/cvi_1.png)                                                                                                                   |
|     | CVIN                                 | 🟢     | ![](img/CVIN_1.png)                                                                                                                           |
|     | Elevation                            | 🟢     | png: ![](img/elevation_1.png)                                                                                                                 |
|     | EVI                                  | 🟢     | ![](img/EVI_1.png)                                                                                                                            |
|     |                                      | 🔴     | Download EVI failed<br/>![](img/EVI_2.png)                                                                                                    |
|     | GNDVI                                | 🟢     | Coverage:<br/>![](img/GNVI_1.png)                                                                                                             |
|     |                                      | 🔴     | Download:<br/>![](img/GNVI_2.png)                                                                                                             |
|     | NDMI                                 | 🔴     | Download:<br/>![](img/GNVI_2.png)                                                                                                             |
| 3   | `SAMPLEMAP`                          | 🔴     | ![](img/samplemap_1.png)                                                                                                                      |
|     |                                      |        | Error handling. When Sample point is not selected. It throws the error.<br/><br/> ![Sample map error](img/samplemap_2.png)                    |
| 4   | YGM                                  | 🟢     | ![](img/YGM_1.png)                                                                                                                            |
| 5   | YPM                                  | 🔴     | ![](img/YPM_1.png)                                                                                                                            |
|     | SAMZ                                 | 🔴     | Download `.tiff`<br/>![](img/SAMZ_1.png)                                                                                                      |
|     |                                      | 🔴     | Download `.shp`<br/>![](img/SAMZ_2.png)                                                                                                       |
|     | RX                                   | 🟡     | Download looks odd<br/>![](img/RX_1.png)                                                                                                      |
|     |                                      |        |                                                                                                                                               |