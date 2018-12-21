# sensor-clusterer

A project focused on clustering different buildings and identifying outliner within them from raw whole building data.

---
## Data collection and pre-processing
- Data sources: Currently two datasets are being used, the Building Genome Dataset (BDG) and the Washington Dataset (DGS)
- [Data Collection](Preprocessing/preprocessing.ipynb): Read temporal dataset and make sure readings are resambpled by the hour.
- [Context Extraction](Preprocessing/context_extraction.ipynb): Generate resampled datasets filtering observations based on the specify context.
- [Load Curve Generation](Preprocessing/load_cuve_generation.ipynb): Based on the given aggregation function, generate one load curve for each building.

The naming format for all generated files is `DatasetName_Context_LoadCurveFunction_TypeOfFile.extension`. Each section is decribed as follows:
- DatasetName: `BDG` for the Building Genome Dataset and `DGS` for the Washington Dataset
- Context: Currently implemented `weekday`, `weekend`, `fullweek`
- LoadCurveFunction: Aggregation function used. Currently implemented `average`, `median`
- TypeOfFile: The type of data that is stored in this file, most of the times is `dataset`
- Extension: Usually `.csv` but also `.png` or `pkl`

## Clustering and Validation
- [Clustering](ClusteringAnalysis/ExperimentUtils.ipynb): Generate building clusters based on daily profiles (formed from hourley read data) using the specified algorithm
- [Clustering Validation Metrics](ClusteringAnalysis/ClusteringValidationMetrics.ipynb): Calculate validation metrics for the clustering results for different choice of k and different algorithms

## Clustering Visualization 
TODO

## Experiments
- [Experiments](Experiments/ExperimentPlayground.ipyng): Sandbox to run all possible combinations of datasets, contexts, and load curve functions as experiments for clustering
<!-- ---
Currently, the interactive Cluster Heatmap Library (InCHlib) implementation on buildings' sensor data is running in the following server

```
ssh -i "sensor-cluster-er.pem" ec2-user@ec2-13-229-153-29.ap-southeast-1.compute.amazonaws.com
```

You can contact Matias for the keyfile. -->
