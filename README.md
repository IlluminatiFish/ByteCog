<p align="center">
  <img src="https://i.ibb.co/vBhNGtk/cooltext379795320651120.png">
</p>

<h4 align="center">
	A way to analyse how malware and/or goodware samples vary from each other using <a href="https://en.wikipedia.org/wiki/Entropy_(information_theory)">Shannon Entropy</a>, <a href="https://en.wikipedia.org/wiki/Hausdorff_distance">Hausdorff Distance</a> and <a href="https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance">Jaro-Winkler Distance</a>
</h3>


<p align="center">
  <img alt="Python version" src="https://img.shields.io/badge/Python-v3.5+-yellow">
  <img alt="Project version" src="https://img.shields.io/badge/Current%20Version-v0.2-yellow">
	<img alt="Codacy Grade" src="https://app.codacy.com/project/badge/Grade/06c8bdaa68414b7b84c096dbd47c0944">
  <img src="https://img.shields.io/github/languages/code-size/IlluminatiFish/ByteCog">
  <img src="https://img.shields.io/github/license/IlluminatiFish/ByteCog">
  <img src="https://img.shields.io/github/downloads/IlluminatiFish/ByteCog/total">
  <img src="https://img.shields.io/github/last-commit/IlluminatiFish/ByteCog">
</p>  

<p align="center">
	<strong>
		<a href="https://github.com/IlluminatiFish/ByteCog/blob/main/README.md#usage">Usage</a>
		•
		<a href="https://github.com/IlluminatiFish/ByteCog/releases">Download</a>
	</strong>
</p>

# Introduction

ByteCog is a python script that aims to help security researchers and others a like to classify malicious software compared to another sample depending on what is the known file is being tested against. This script be extended to use a machine learning model to classify malware in the future. ByteCog uses multiple methods of analyzing and classifying samples given to it, such as using <a href="https://en.wikipedia.org/wiki/Entropy_(information_theory)">Shannon Entropy</a> to give a visual aspect for the researchers to look at while analyzing the code and finding possible readable code/text in a sample. ByteCog also uses <a href="https://en.wikipedia.org/wiki/Hausdorff_distance">Hausdorff Distance</a> to calculate a 'raw similarity' value based on the difference in the entropy graphs of both samples, and finally ByteCog uses o-Winkler Distance</a> to calculate the 'true similarity' since the Hausdorff Distance will in most cases return a very high value if the sample is mostly the same entropy wise, so the Jaro-Winkler distance is used to 'adjust' the simliarity value for this case of a sample.

# Requirements

- A python installation above 3.5+, which you can download from the official python website <a href="http://www.python.org/download/">here</a>.

# Installation 
Clone this repository to your local machine by following these instructions layed out <a href="https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository">here</a>

Then proceed to download the dependencies file by running the following line in your console window
```
pip -U -r depend.txt
```

# Usage
```
======================================================
|      ____          __         ______               |
|     / __ ) __  __ / /_ ___   / ____/____   ____    |
|    / __  |/ / / // __// _ \ / /    / __ \ / __ \   |
|   / /_/ // /_/ // /_ /  __// /___ / /_/ // /_/ /   |
|  /_____/ \__, / \__/ \___/ \____/ \____/ \__, /    |
|         /____/                          /____/     |
|                                                    |
|                    Version: 0.2                    |
|               Author: IlluminatiFish               |
======================================================

usage: bytecog.py [-h] -k KNOWN -u UNKNOWN -i IDENTIFIER -v VISUAL

Determine whether an unknown provided sample is similar to a known sample

optional arguments:
  -h, --help            show this help message and exit
  -k KNOWN, --known KNOWN
                        The file path to the known sample
  -u UNKNOWN, --unknown UNKNOWN
                        The file path to the unknown sample
  -i IDENTIFIER, --identifier IDENTIFIER
                        The antivirus identifier of the known file
  -v VISUAL, --visual VISUAL
                        If you want to show a visual representation of the file entropy
 ```

# Features

- Calculates sample similarity
- Generates chunked entropy graph
- Able to *possibly* detect malicious and benign software samples

# Screenshots

Chunked Entropy Graph
<br>
![chunk_entropy_graph](https://user-images.githubusercontent.com/45714340/112214987-bdb7ae00-8c17-11eb-98c0-bebcda6fc1ba.png)

Output of ByteCog
<br>
![bytecog_output](https://user-images.githubusercontent.com/45714340/112215120-e475e480-8c17-11eb-908d-a2e4c205521c.png)

# License
ByteCog - A way to analyse how malware and/or goodware samples vary from each other using <a href="https://en.wikipedia.org/wiki/Entropy_(information_theory)">Shannon Entropy</a>, <a href="https://en.wikipedia.org/wiki/Hausdorff_distance">Hausdorff Distance</a> and <a href="https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance">Jaro-Winkler Distance</a> Copyright (c) 2021 IlluminatiFish

This program is free software; you can redistribute it and/or modify the code base under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but without ANY warranty; without even the implied warranty of merchantability or fitness for a particular purpose. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/

# Acknowledgements 
Using a modified version of venkat-abhi's Shannon Entropy calculator to work with my project script, you can find the original one <a href="https://github.com/venkat-abhi/Entropy-Calculator/blob/master/shanon-calc.py">here</a>.
<br>
Using the fastest method to get maximum key from a dictionary using this snippet <a href="https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary">here</a>.


# References
[Entropy Wiki](https://en.wikipedia.org/wiki/Entropy_(information_theory))
<br>
[Jaro-Winkler Distance Wiki](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance)
<br>
[Hausdorff Distance Wiki](https://en.wikipedia.org/wiki/Hausdorff_distance)
<br>
[Shannon Calculator](https://github.com/venkat-abhi/Entropy-Calculator/blob/master/shanon-calc.py)
<br>
[Referenced Article #1](https://www.talentcookie.com/2016/02/05/file-entropy-in-malware-analysis/)
<br>
[Referenced Paper #1](https://arxiv.org/ftp/arxiv/papers/1903/1903.10208.pdf)
<br>
[Referenced Paper #2](https://www.researchgate.net/publication/3437909_Using_Entropy_Analysis_to_Find_Encrypted_and_Packed_Malware)
<br>
[Referenced Paper #3](https://www.researchgate.net/publication/334686946_Machine_Learning_Based_File_Entropy_Analysis_for_Ransomware_Detection_in_Backup_Systems)

