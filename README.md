# Measurement of Wet Etching Rate
This program was developed based on our dear operator Dr. J. Yoon's requests 😊 and aims to streamline the measurement of the wet etching rate and surface uniformity of Si samples. 


<br>

<p align='center'> 
&lt;PROJECT OVERVIEW&gt;
</p>
<p align='center'> 
<img src="images/ocr_img2.png" alt="Alt text" width="600" />
</p>
<div align="center">Fig. 1. This program aims to effectively measure the wet etching rate and surface uniformity of Si samples. Courtesy of Dr. Yoon.</div> 
<br>

<p align='center'> 
&lt;BRIEF INTRODUCTION&gt;
</p>

<div align="justify"> 
This program operates on top of the etch rate measurement application and is designed to position itself over the area where the measurement data are logged as in Fig. 1. It first saves the area as an image file (.PNG) as a backup, read the figures with the optical character recognition engine Tesseract, and save them in an Excel file (.CSV). 
</div>
<br>
<p align='center'>
<img src="images/ocr_img.png" alt="Alt text" width="600" />
</p>
<br>
<div align="center">Fig. 2. Example of program execution screen, situated over the area where measurement data are logged. 
  <br>The UI in the figure is outdated and the latest version taks the form in the following firues.</div> 
<br>

<div align="justify">
  This program consists of two windows–measurement window and visualization window. While the buttons in the measurement window are designed to help arrange data in an Excel file or to take a screenshot of the area in cosideration, the visualization window allows users to easily plot the data, identify faulty points, and estimate the degree of surface flatness. 
</div>
<br>
<table>
  <tr>
    <td><img src="images/ocr_window1.png" width="400"/></td>
    <td><img src="images/ocr_window2.png" width="400"/></td>
  </tr>
</table>
<div align="center">Fig. 3. Measurement window (left) and visualization window (right)</div> 
<br>
* Detailed information on each button is available in the user guide.
