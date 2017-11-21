# ecop-shoreline
Shoreline delineation module developed in the framework of ECOPOTENTIAL H2020 project

# Shoreline detection module
The shoreline detection algorithm has been implemented by Starlab in python v2.7 as a separate module of the whole chain of processing.  This allows us to provide such module for its integration in the ECOPOTENTIAL virtual laboratory. 

## Dependencies 
For an easy installation of the necessary libraries:

```sh
pip install -r requirements.txt
```

## Input
The input data to the shoreline detection algorithm are Sentinel-1 Interferometric Wide (IW) GRDH dual polarization (VH and VV) images, which have ALREADY undergone the typical SAR pre-processing phase, including calibration and range doppler terrain correction. At Starlab we implemented our pre-processing chain but we will not provide it, since other ECOPOTENTIAL applications using Sentinel-1 data should also use such algorithms that therefore should be implemented separately and made available to all partners (and users) to run their modules.

## Shoreline module functions definitions
The shoreline detection module includes two callable functions.

#### Each Sentinel-1 band is firstly processed separately by using the function:

```sh
def waterbody(band, logarithmic = True, clipping = [5,98],  filter_kernel_size = 25, opening_kernel_size = 7, closing_kernel_size = 7, fill_holes = True, sand_max_gray_level = 5)
```

where:

* band: Sentinel-1 VV or VH polarization band, as float32 numpy array
	
The users can set up the parameters:
	
* logarithmic (example used for Curonian Lagoon: true): if true a logarithmic intensity rescaling is applied to the image;    otherwise a linear rescaling is applied.

* clipping (example used for Curonian Lagoon: [5, 98]): lower and upper limits used by the percentile function used in the intensity rescaling step.
	
* filter_kernel_size (example used for Curonian Lagoon: 21): size of the median filter applied for noise reduction.
	
* opening_kernel_size (example used for Curonian Lagoon: 5): size of the kernel used in the opening morphological operation.
	
* closing_kernel_size (example used for Curonian Lagoon: 5): size of the kernel used in the closing morphological operation.
	
* fill_holes (example used for Curonian Lagoon: true): if true the algorithm fills all gaps in land, regardless their size; otherwise only small gaps are closed.
	
* sand_max_gray_level (example used for Curonian Lagoon: 0): threshold used to label as land those sand banks pixels having a grey level below such value.

### waterbody output
The output of the waterbody function are, for each polarization:
 
* water mask (uint8 numpy array)
* water edges image (uint8 numpy array)
* ancillary data 

```sh
ancillary = {"scaled": img, "denoised": blur, "rawland": raw_land_mask}
```

where:

* Scaled: image after applying the intensity rescaling (byte numpy array)
* Denoised: image after applying the denoising filter (byte numpy array)
* Rawland: raw land mask before applying morphological operation (byte numpy array).

#### The Rawland images (one for each polarization) correspond to band 1 and band 2 in the second function:
 
```sh
def waterbodydp(band1, band2, opening_kernel_size = 7,  closing_kernel_size = 7, fill_holes = True)
```
	
The waterbodydp function combines the results obtained by processing each band in the previous step.
	
In order to run this function, the parameter "dual_pol" must be set to "true" in the configuration file.
	
The editable parameters are the same used in the first step. We keep the same values also for the second function.
	
### waterbodydp output
The output of the waterbodydp function are:
	
* water mask (uint8 numpy array)
* water edges image (uint8 numpy array)
	
## Note
Please note that the input and output of both waterbody and waterbodydp functions are numpy arrays which do not provide geographic information. A dedicated function attaching the geographic information should be made available in the virtual laboratory, and called at the end of the waterbody(dp) module processing.
