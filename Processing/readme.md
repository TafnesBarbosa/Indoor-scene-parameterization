# Help

The code `run_videos.py` is used to preprocess using colmap, directly from Nerfstudio, and also for processing the data using Nerfstudio's nerfacto and splatfacto models.

You need to create the folders that will be used for source and destination before using the code. Destination folder must be:

```
<destination>/
|
|--colmap/
|  |
|  |--GPU/
|  |--RAM/
|
|--nerfacto/
|  |
|  |--GPU/
|  |--RAM/
|
|--splatfacto/
|  |
|  |--GPU/
|  |--RAM/
|
|--Evaluations/
|
|--Evaluations_splatfacto/
```

The current code works only with one folder inside the experiments for the evaluation step, since `get_evaluations` method use `*` for the folders inside used model folders. So, if we train more than once for the same dataset, make sure you remove all the older outputs before getting evaluation. 

The `requirements.txt` file should not be used to install dependecies, but only for knowledge. Installing the dependecies should be done by the user manually.