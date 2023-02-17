# PBL

> Portable Balance Lab course material for students

The Portable Balance Lab (PBL) is a practical course that teaches people how to create their own balance lab from raw components and software. This repository contains all of the learner-facing course material.


# <a name="getting-started"></a> 🚀 Getting Started

In this course, we will work with Python. To get used to this, all lectures are delivered through Jupyter notebooks. This way, you can view, modify, and run all code samples in the Jupyter viewer (i.e. just like Matlab Livescripts).

To get started, follow these steps:

1. **Download a Copy of this Repository**:

    1. [Download link](https://github.com/PortableBalanceLab/PBLstaging/archive/adam_rearrangement.zip): TODO put into `releases`
    2. Unzip it somewhere - all course materials are inside it

2. **Get Jupyter**:

    1. Download and Install Anaconda: https://www.anaconda.com/products/distribution
    2. Boot the Anaconda Navigator (e.g. via the Start bar)
    3. Boot Jupyter through the navigator UI
    4. This should open Jupyter a browser window. Jupyter notebooks (`.ipynb` files) can be opened through this UI.

3. **Open a PBL Lecture**:

    1. In the Jupyter UI, browse to wherever you unzipped this repository:

        * e.g. #1 click `Downloads` then `pbl-main`
        * e.g. #2 click `Desktop` then `pbl-main`
        * e.g. #3 click `OneDrive` then `Desktop` then `pbl-main`

    2. Browse to a specific lecture `.ipynb` file

         * e.g. click `PBL start-up session (students) (21-22)` then `PBL_Lab0_Manual_2022.ipynb`

Once you are satisfied that you can load a Jupyter notebook, you can then go through the course materials.


# 👩‍🏫 Course Materials

The course material is split into lectures (`L`), sensor practicals (`S`), and extra content (`X`):

- You should go through all lectures (`L1`, `L2`, and `L3`)
- You will be assigned one of four possible practicals (`S1`, `S2`, `S3`, or `S4`)
- All practicals require setting up a Raspberry Pi (`S0`)
- Extra content (`X`) may contain helpful hints, such as code examples


## `L`: Lectures

It is recommended that you go through all of the lecture material (`L1`-`L3`). These ensure you know enough Python to get through the practical material (`S1`-`S5`).

> **⚠️ Warning ⚠️**: You should open the lecture's Jupyter notebooks (`.ipynb` files) in your own local copy of this repository (see: [Getting Started](#getting-started)). The preview links here don't let you *run* the example code.

| ID | Title |
| -- | ----- |
| L1 | [Python: Basics](L1_PythonBasics/L1_PythonBasics.ipynb) |
| L2 | [Python: functions, classes, and writing files](L2_PythonClassesAndWritingFiles/L2_PythonClassesAndWritingFiles.ipynb) |
| L3 | [Python: GUIs and Hardware Interfacing](L3_PythonGUIsAndHardware/L3_PythonGUIsAndHardware.ipynb) |


## `S`: Sensor Practicals

You will be asigned one of four possible lab practicals (`S1`-`S4`). All lab practicals require setting up the Raspberry Pi (`S0`). After setting up the Raspberry Pi, you only need to use the materials related to the practical you have been assigned (`S1`-`S4`).

| ID | Title | Notes |
| -- | ----- | ----- |
| S0 | [Set up the Raspberry Pi](S1_SetUpRaspberryPi/S1_SetUpRaspberryPi.ipynb) | **All lab practicals (`S2`-`S5`) require doing this first** |
| S1 | [Pose Estimation](S2_PoseEstimation/S2_PoseEstimation.ipynb) | |
| S2 | [IMU](S2_IMU/S2_IMU.ipynb) | |
| S3 | [Force Plate](S3_ForcePlate/S3_ForcePlate.ipynb) | |
| S4 | [EMG](S4_EMG/S4_EMG.ipynb) | |


## `X`: eXtra Content

These materials are extra notes/examples that parts of the course may refer to.

| ID | Title | Notes |
| -- | ----- | ----- |
| X1 | [Writing CSV Files](X1_WritingCSVFiles/X1_WritingCSVFiles.ipynb) | Explains how to write CSV data to a file |
| X2 | [Generating Timestamped Filenames](X2_GeneratingTimestampedFilenames/X2_GeneratingTimestampedFilenames.ipynb) | Explains how to generate timestamped filenames |


# F&Q

### Where is the Schedule?

This repository only contains core course materials. Schedules should be made available by your teachers via their teaching platform of choice (e.g. in TU Delft, Brightspace).
