 # 🧠 NeuroCortex: The Self-Evolving AI Framework

![NeuroCortex Logo](https://raw.githubusercontent.com/mohammedqaidamanlift-hub/-NEUROCORTEX/main/assets/neurocortex_logo.png)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16945431.svg)](https://doi.org/10.5281/zenodo.16945431)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A groundbreaking open-source framework for achieving autonomous self-evolution and self-management in artificial intelligence (AI). NeuroCortex moves beyond traditional AutoML by introducing the **Self-Reinforcing Development Framework (SRDF)**, enabling AI systems to re-engineer their own architecture and learning processes without human intervention.

## 🧠 The SRDF Architecture

The core of NeuroCortex is a closed-loop system composed of three integrated units:

1.  **The Trawler**: Continuously analyzes data and performance to identify improvement areas and anomalies.  
2.  **The Generator**: Proposes novel architectural modifications, training strategies, or entirely new sub-models.  
3.  **The Arbiter**: Validates and integrates only the most effective innovations against rigorous performance benchmarks.  

Together, these units form a self-reinforcing cycle of continuous improvement, aiming to achieve **Evolutive AI**.

## 🚀 Vision

To transition from static, human-dependent AI models to **"Evolutive AI"**—systems capable of managing their own lifecycle, adapting in real-time to novel data, and driving sustainable innovation autonomously.

## 📄 Whitepapers

- [English Whitepaper PDF](https://github.com/mohammedqaidamanlift-hub/-NEUROCORTEX/blob/main/Self_Evolving_AI_Whitepaper_EN_Final.pdf)  
- [Arabic Whitepaper PDF](https://github.com/mohammedqaidamanlift-hub/-NEUROCORTEX/blob/main/%20Self_Evolving_AI_Whitepaper_AR_Final.pdf)  

## 🔮 Applications

*   **Healthcare**: AI that redesigns itself to detect novel viruses within hours, not weeks.  
*   **Cybersecurity**: Autonomous systems that anticipate and counter emerging threats in real-time.  
*   **Engineering**: Accelerated discovery of new materials and products through autonomous simulation and design.  
*   **Industrial Automation**: Self-optimizing manufacturing processes and smart infrastructure without manual retuning.  

## 🚀 Quick Start

### Run on Google Colab
You can directly try the **Toy Example** in Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mohammedqaidamanlift-hub/-NEUROCORTEX/blob/main/notebooks/srdf_toy_colab.ipynb)

### Run Locally
Clone the repository and run the toy example:

```bash
# Clone the repository
git clone https://github.com/mohammedqaidamanlift-hub/-NEUROCORTEX.git
cd -NEUROCORTEX/examples/srdf_toy

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python run.py
-NEUROCORTEX/
├── assets/
│   └── neurocortex_logo.png
├── examples/
│   └── srdf_toy/
│       ├── run.py
│       ├── requirements.txt
│       └── output.json
├── notebooks/
│   └── srdf_toy_colab.ipynb
├── Self_Evolving_AI_Whitepaper_EN_Final.pdf
├── Self_Evolving_AI_Whitepaper_AR_Final.pdf
└── README.md
 # NeuroCortex SRDF - Core Dependencies
numpy>=1.21.0
scipy>=1.7.0
scikit-learn>=1.0.0
imbalanced-learn>=0.9.0
pandas>=1.3.0
matplotlib>=3.5.0
seaborn>=0.11.0
tqdm>=4.62.0
joblib>=1.1.0
