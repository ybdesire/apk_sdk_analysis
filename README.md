# Introduction

Data mining for APK by cluster and machine learning.
Currently APK package features extraction has been completed.

# Code structure

## code design

The basic code design philosophy is 3 layers components:
   * low layer: Low level functions to contact with Androguard for single feature extraction.
   * med layer: Feature extraction control with config parsing. 
   * first layer: Application layer. Work with user input and result output.

## code files

|File                |Description                                     |layer|
|--------------------|------------------------------------------------|-----|
|api_list.p          |sensitive and system API list|  none |
|apkparser.py        |provide basic functions to get all features   |low|
|feature_extractor.py|feature extraction process control|med|
|main.py             |start of the project|first|
|pattern_parser.py   |parse pattern file and generate api_list.p|none|
|test.apk            |apk file for unit test|none|
|test.py             |unit test|none|

## unit test

Run command below to test the basic feature extraction functions at class apkparser.

```bash
python test.py
```
Currently xxx test cases have been provided.


# Extracted features


* package names at apk
* class count at each package
* package depth
* package name to array by FeatureHasher
* class size
* interface count for class
* method count for class
* virtual method count for class
* variable count for class
* instance variable count for class
* static variable count for class
* access flag sum for class
* class name to array by FeatureHasher
* super class name to array by FeatureHasher
* native function count for class
* method para count for class
* method access info array for class


