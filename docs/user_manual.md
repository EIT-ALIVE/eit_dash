# User manual for EIT dashboard

Note 1: If you have not installed the dashboard yet, please refer to our [README](../README.md) on instructions how to do
that.

Note 2: While the dashboard is rendered in a browser window, you are not working online. All data that you load into the
dashboard remains local on your machine.

Note 3: The Dashboard, this manual, and the (back end) software it is built around are works in progress. The images and
interaction procedures may be slightly off. Please bear with us.

## LOAD page

The dashboard should open on the **LOAD** page, but in case this does not happen, navigate there by clicking **LOAD** at
the top of the page. You should see something like this:

<kbd>
<img src=images/load_entry_point.png width="1200px">
</kbd>

Click on the dropdown menu to select the format of data to load, then click on the `Select Files` button. From here you
can navigate to the data and select it. Hit `Confirm` to pre-load and pre-view the selected data.

It could look something like this:

<kbd>
<img src=images/load_data_preview.png width="800px">
</kbd>

From here one or more pre-selection(s), termed "Datasets" in the software, of a portion of the data can be made by
selecting a time window from preview and clicking `Confirm`. Note that a number of additional signals can be co-loaded
with the data using the check boxes above the Pre selection window. If you want to use these in the following steps,
they _must_ be selected here already.

Note that on the following page more precise time selections can be made. This page is just intended to make a rough
pre-selection. Also, pre-selections cannot be undone at this point, but do not need to be used for further processing.

When all pre-selections are made, Click **`PRE-PROCESSING`** at the top of the page to proceed to the next stage.

## PRE-PROCESSING page

Currently the only pre-processing steps available are period selection and filtering. We plan to add other
pre-processing steps in the future, includeing ROI selection, resampling, etc.

#### Select data range(s).

First click on `Select data range(s)` and from the "Periods selection method", select `Manual` (we will add automated
selection methods, e.g. "Stabe period selection", in the future).

You can now select which periods to actually use from within each Dataset, and add them to your analysis list by
clicking on `Add selection`. Multiple selections from one or more preselected data ranges. These are termed "Periods" in
the software.

All Periods will appear in a darker shade. When you have finished selecting periods, close the "Periods slection" window by hitting the `X`.

<kbd>
<img src=images/preprocessing_add_selection.png width="800px">
</kbd>

#### Filter data

Click `Filter Data` and choose your favorite filter settings and then `Apply`. You can now select the period you want to
apply it to to preview the result. You can change settings or periods in this window and each time you click `Apply`,
the preview will update. When you are happy with a particular setting/selection, click `Confirm` to add it to your list.

<kbd>
<img src=images/preprocessing_filter.png width="800px" style="border: 1px solid black">
</kbd>
