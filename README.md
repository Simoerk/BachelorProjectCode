BachelorProject 2024 - Magnus Asbjørn Thorsen, Simon August Mørk, Kasper Frahm Jensen

This project explores the applications of differential privacy for aggregating energy consumption data,
specifically addressing the challenges faced by Energinet, Denmark’s energy transmission system
operator, in releasing their data to either relevant parties or publicly. 
This github repoitory is an implementation of this. 

Specs: 
System: macos monterey
MacBook Air (13-inch, 2017)
processor:  1,8 GHz Dual-Core Intel Core i5
memory: 8 GB 1600 MHz DDR3
graphics: Intel HD Graphics 6000 1536 MB

Requirements:
python: Python 3.9.13
numpy 1.21.5
pandas 1.4.4
scipy 1.9.1
matplotlib 3.6.3

Folders:
data - all data used by the applications and utilities. 
DifferentialApplication: The different DifferentialApplications
experiments: experiments on differing aspects of the implementation
Mechanisms: implementations of differentially private mechanisms
Queries - simple query modules
results - folder that results of running anything ends in, apart from dataExtractor, as this saves to data.
utils - helping modules and different utilities.

If you are to run a command in the terminal make sure that BachelorProjectCode 
is the current working directory

Depending on what version of python you are running, the python command might be fx python3

To extract relevant data from Energinet run the following command using the util dataExtractor.py
python -m utils.dataExtractor

How to run individual Differential applications:
python -m DifferentialApplication.name

ex:
python -m DifferentialApplication.NumMunUnbGeoLoc

This is the same for running any file, such as experiments, utils or query.
python -m foldername.filename

To generate pure aggregate sum files, run the following commands

python -m utils.generatePureData
python -m utils.generatePureDataTree

