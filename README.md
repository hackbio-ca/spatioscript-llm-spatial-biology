# spatioscript-llm-spatial-biology

SpatioScript: LLM-powered spatial biology query model

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Abstract

A concise summary of the project's goals, the problem it addresses, and its intended audience. This section can include potential use cases and key features.

Single-cell RNA sequencing (scRNA-seq) has enabled the measurement of expression levels of thousands of genes across millions of individual cells. While scRNA-seq provides deep transcriptional profiles, it obscures critical information about each cell’s physical location within the tissue microenvironment. Spatial transcriptomics overcomes this limitation by mapping gene expression back onto tissue sections, offering a powerful view of both the molecular identity of cells and their spatial organization. Together, these technologies allow researchers to study how cells are organized and interactions within complex biological systems, such as tumours.
We present an interactive AI-powered application that enables natural language interrogation of spatial transcriptomics data, with a focus on the tumour microenvironment, where the physical arrangement of immune cells, stromal components, and malignant cells plays a critical role in disease progression and therapeutic response. Users can upload or select pre-processed public datasets and ask questions of their data such as “Are CD8+ T cells enriched in the tumour core?” or “Return the spatial proximity of CD8 cells next to blood vessels” or “How correlated are my spatial domains with pathology annotations?”. 
The system integrates preprocessed public spatial datasets with cell type annotations and a spatial graph (i.e. connectivity map), performs relevant neighbourhood and enrichment analyses, and generates concise, biologically contextualized summaries using a large language model (LLM). 
With an ultimate goal of enhancing multi-disciplinary research, our tool 1) lowers the barrier to explore high-dimensional spatial datasets and 2) facilitates integration of image-based annotations with high-dimensional molecular discoveries, serving as a valuable toolkit for biologists and clinicians. This project demonstrates how natural language interfaces can make complex high-dimensional omics data more accessible and actionable, augmenting biological insights and empowering the user’s scientific vision.


## Installation

Provide instructions on how to install and set up the project, such as installing dependencies and preparing the environment.

```bash
# Example command to install dependencies (Python)
pip install project-dependencies

# Example command to install dependencies (R)
install.packages("project-dependencies")
```

## Quick Start

Provide a basic usage example or minimal code snippet that demonstrates how to use the project.

```python
# Example usage (Python)
import my_project

demo = my_project.example_function()
print(demo)
```
```r
# Example usage (R)
library(my_project)

demo <- example_function()
print(demo)
```

## Usage

Add detailed information and examples on how to use the project, covering its major features and functions.

```python
# More usage examples (Python)
import my_project

demo = my_project.advanced_function(parameter1='value1')
print(demo)
```
```r
# More usage examples (R)
library(demoProject)

demo <- advanced_function(parameter1 = "value1")
print(demo)
```

## Contribute

Contributions are welcome! If you'd like to contribute, please open an issue or submit a pull request. See the [contribution guidelines](CONTRIBUTING.md) for more information.

## Support

If you have any issues or need help, please open an [issue](https://github.com/hackbio-ca/demo-project/issues) or contact the project maintainers.

## License

This project is licensed under the [MIT License](LICENSE).
