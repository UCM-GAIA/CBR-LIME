# CBR-LIME

[![License](https://img.shields.io/badge/license-GNU_3-green)](https://www.gnu.org/licenses/gpl-3.0.html)

CBR-Lime is a Lime configuration recommender, which uses human perception to acquire knowledge of what is an explanation of good quality.

## Installation

To install the required libraries with pip  

```python
pip install -r requirements
```

## Flow

All the elements must be executed in order

- [00_image_resize](00_image_resize)
- [01_filter_images](01_filter_images)
- [02_calc_similitude](02_calc_similitude)
- [03_calc_explications](03_calc_explications)
- [04_adquire_information](04_adquire_information)
- [05_compute_acquired_information](05_compute_acquired_information)
- [06_compare_neighborhood](06_compare_neighborhood)
- [07_check_hypothesis](07_check_hypothesis)
- [08_process_experiment_data](08_process_experiment_data)

### 00_image_resize

(Optional) Script to resize the image dataset to the required dimensions.

### 01_filter_images

Filter and select the top image predictions.

For each image in the input folder recived obtain the top classification value, select the most accurate and copy it to the output folder.

### 02_calc_similitude

Calculate the similitude between images in the dataset.

Calculate the similitude comparing the neural net classification and generate two csv files one with all the dataset images and other with the top 3 related images for each one.

### 03_calc_explications

Calculate the perturbed image dataset for the experiment.

Calculate the perturbed image dataset to use in the experiemnt, generates nine perturbed images for each one in the original image dataset.

### 04_adquire_information

Application for adquire the users explication preferences.

Shows a windows with nine options, the user must choose based on her best
human perception explication.

### 05_compute_acquired_information

Process the results of the experiment.

Process the results generated in the LimeExperiment, generates a csv file with the information and returns the file path.

### 06_compare_neighborhood

Generates the similarty comparation.

Generate the similarity matrix between images and similar neighborhood.

### 07_check_hypothesis

Application for choose the best Lime configuration between the default configuration and the process configuration.

### 08_process_experiment_data

Process the results of the experiments.

Process the results generated in the check hypothesis experiment and generates a csv file with the information and returns the file path.

## Applications

Additionally two applications have been created to complement the software:

- [CBR-cycle](CBR-cycle)
- [Similitude-reviewer](Similitude-reviewer)

### CBR-cycle

This application implement the full CBR cycle. Shows the original image, its associated perturbation and the result explication, the configuration can be revised and modified by the user.

### Similitude-reviewer

Shows the three more similar images for each one in the dataset, the similarity value and the classification information.
