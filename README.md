<!-- Readme for Let7i Manuscript by Trent Neilson -->
<a name="readme-top"></a>

# Let7i Delivery Increases Activity of Antigen Presenting Cells, T Cell Infiltrates and Suppresses Ovarian Tumour Growth 

This repository contains supporting material for the manuscript:

> Authors, ["Let7i Delivery Increases Activity of Antigen Presenting Cells, T Cell Infiltrates and Suppresses Ovarian Tumour Growth "][paper-link], *Journal* (2023)

<br>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about">About</a>
    </li>
    <li><a href="#code-and-figures">Code and Figures</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About
This project entails getting the Gene Ontology (GO) terms used to filter and plot the data that was obtained from LinkedOmics.
<br /><br />
The data was gathered through running all 2002 miRNAs through the LinkedOmics platform, which conducts pearson corelation tests using miRNA seq data as search and target dataset in the TCGA_OV database. Furthermore, the LinkedInterpreter module of LinkedOmics conducts analysis using Gene Set Enrichment Analysis (GSEA) using the gene ontology enrichment analysis, ranking with FDR, min samples of 3 and 500 simulations. The data is gathered and filtered using the [Genetic-Screening-Web-Automation][web-auto] tool. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Code -->
## Code and Figures
The GO terms to filter the raw data obtained from LinkedOmics are obtained by using the ```/GeneOntology/getGoTerms.py``` script. The script works by taking comma separated search parameters in  ```/GeneOntology/GO_search_terms.txt``` and searching all known GO terms in the ```/GeneOntology/go-data/go.txt``` file. The desired immunological GO terms are then outputted to ```/GeneOntology/output_GO_terms.txt```, in this case 3877/51281 GO terms were determined immunologically related.
<br />
The ```linkedOmicsPlot.py``` file is responsible for creating the 3 plots that can be found below. The script used 3 main data files for constructing the plots:

1. The ```/data/microRNA formatted data.xlsx``` file has 2 sheets one for P-Value and the other for FDR. It contains the P-Value or FDR value for each immunological pathway for each miRNA. It is used to construct Supplementary Figure S2 and Figure 1.
2. The ```/data/microRNA GO Categories.txt``` contains the information from supplementary table, it sorts the significant GO terms into different categories. Figure 1 uses this file to categorize the GO terms for each miRNA.
3. The ```/data/microRNA Counts.csv``` contains data for the number of significant immunological pathways that are correlated with each miRNA, this data is used to generate Supplementary Figure S1. 

All the figures can be found below:
<details>
<summary>Figure 1 - Bubble Plot</summary>
<img src="plots/Fig1 - Bubble Plot.png"  width="40%" height="40%">
</details>

<details>
<summary>Supplementary Figure S1 - Bar Plot</summary>
<img src="plots/FigS1 - Histogram.png"  width="40%" height="40%">
</details>

<details>
<summary>Supplementary Figure S2 - Heatmap</summary>
<img src="plots/FigS2 - Heatmap.png"  width="80%" height="80%">
</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Trent Neilson - t.neilson@uq.net.au

Project Link: [https://github.com/secretx51/Let7i-Data-Figure-Generation](https://github.com/secretx51/Let7i-Data-Figure-Generation)

[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
* Wu lab - School of Biomedical Science at the University of Queensland
* [LinkedOmics](https://linkedomics.org/)
* [Genetic Screening Web Automation](https://github.com/secretx51/Genetic-Screening-Web-Automation)
* [NCBI Genes](https://www.ncbi.nlm.nih.gov/gene/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[paper-link]: placeholder
[web-auto]: https://github.com/secretx51/Genetic-Screening-Web-Automation
[forks-shield]: https://img.shields.io/github/forks/secretx51/Let7i-Data-Figure-Generation.svg?style=for-the-badge
[forks-url]: https://github.com/secretx51/Let7i-Data-Figure-Generation/network/members
[stars-shield]: https://img.shields.io/github/stars/secretx51/Let7i-Data-Figure-Generation.svg?style=for-the-badge
[stars-url]: https://github.com/secretx51/Let7i-Data-Figure-Generation/stargazers
[issues-shield]: https://img.shields.io/github/issues/secretx51/Let7i-Data-Figure-Generation.svg?style=for-the-badge
[issues-url]: https://github.com/secretx51/Let7i-Data-Figure-Generation/issues
[license-shield]: https://img.shields.io/github/license/secretx51/Let7i-Data-Figure-Generation.svg?style=for-the-badge
[license-url]: https://github.com/secretx51/Let7i-Data-Figure-Generation/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/trent-neilson
