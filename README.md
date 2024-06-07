# README
This repository provides additional content for the paper "Bayesian Multi-Level Performance Models for Multi-Factor
Variability of Configurable Software Systems"

## Paper
PDF: <a href="/material/paper.pdf">Bayesian Multi-Level Performance Models for Multi-Factor
Variability of Configurable Software Systems</a>

<details open>
  <summary><h3>ABSTRACT</h3></summary>
<p>Configuring a software system for a specific environment and use
case is challenging. Beyond functionality, configuration options can
have a substantial influence on performance. Due to combinatorics,
it is often unclear in practice how to configure a system to yield
certain performance guarantees. Hence, established approaches aim
at learning a model that estimates performance given a configura-
tion. However, multiple factors, such as varying the workload, can
affect a configuration’s performance in various ways, limiting gen-
eralizability model-based performance estimations. There are two
principal approaches in the literature to address this multi-factor
variability: (1) measure a subset of configurations for varying envi-
ronments to learn a single, generalized model or (2) learn a distinct
model for every single environment of the system. We introduce
a third approach to this mix: Bayesian Multi-level models, called
HyPerf. In a nutshell, HyPerf builds a single model with multiple
levels, in which the upper level captures the common influences of
options across all environments, while the lover level captures the
environment-specific influences of configuration options. Through
a large-scale empirical analysis, we assess the prediction accuracy
of all three approaches on 10 real-world software systems across up
to 35 environments. Our findings demonstrate HyPerf’s competi-
tive predictive performance among interpretable models. Moreover,
we demonstrate that HyPerf allows reasoning on its multiple lev-
els that enables novel insights, e.g., into which options’ influence
varies substantially across environments. For the first time, HyPerf
enables the selection of a representative set of environments that
covers most option’s variance across environments while disregard-
ing non-informative environments.</p>
</details>

<details>
  <summary><h2>SUP Material</h2></summary>
  
  <details>
    <summary><h3>Software Systems</h3></summary>
  </details>
  <details>
    <summary><h3>RQ1</h3></summary>
  </details>
  <details>
    <summary><h3>RQ2</h3></summary>
  </details>
  <details>
    <summary><h3>RQ3</h3></summary>
  </details>
</details>
<details>
  <summary><h2>Experiment Code</h2></summary>
  <details>
    <summary><h3>Run as Docker (Replication)</h3></summary>
    To run the full experiment via Docker, follow these steps:

1. **Install Docker:** 
   - Refer to the [Docker Documentation](https://docs.docker.com/) for installation instructions.

2. **Clone the Repository:**
   - Navigate to the directory where you want to clone the repository and run:

   ```sh
   git clone https://github.com/anonym458551495/multilvl-models-multi-factor-variab
   cd path-of-repo/multilvl-models-multi-factor-variab/experiment-code
   ```
3. **Build the Docker Image:**
   - Open a terminal.
   - Change your directory to `path-of-repo/multilvl-models-multi-factor-variab/experiment-code`.
   - Run the following command:
     ```sh
     docker build ./
     ```
     
4. **Run the Docker Container:**
   - After the build is complete, run your Docker container with:
     ```sh
     docker run <image-id>
     ```
   - Explore the Streamlit dashboard.
     
5. **Copy the results:**
   - To copy the results outside the docker use:
     ```sh
     docker create --name temp-container <image-id>
     docker cp temp-container:/app/wluncert/results /local/path
     docker rm temp-container
     ```

  </details>
  <details>
    <summary><h3>Running the Experiment Locally Without Docker (Replication)</h3></summary>

    

This guide will help you set up and run the experiment locally on your machine without using Docker. Follow the steps below to get everything up and running.

#### Prerequisites

Ensure you have the following installed on your system:
- Ubuntu 22.04 or equivalent Linux distribution
- Python 3.9
- Git

#### Step-by-Step Instructions

1. **Install Common Software:**

   Open a terminal and run the following commands to update your package list and install the necessary software:

   ```sh
   sudo apt-get update
   sudo apt-get install -y software-properties-common git
   ```

2. **Set Up the Environment:**

   Add the necessary repository and install Python 3.9 along with development tools:

   ```sh
   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt-get update
   sudo apt-get install -y python3.9 python3.9-dev python3-pip python3-wheel build-essential
   ```

3. **Clone the Repository:**

   Navigate to the directory where you want to clone the repository and run:

   ```sh
   git clone https://github.com/anonym458551495/multilvl-models-multi-factor-variab
   cd path-of-repo/multilvl-models-multi-factor-variab/experiment-code
   ```

4. **Install Python Dependencies:**

   Use pip to install the required Python packages:

   ```sh
   python3.9 -m pip install --no-cache-dir -r requirements.txt
   ```

   Reinstall specific versions of JAX and JAXLIB to avoid version conflicts:

   ```sh
   python3.9 -m pip install jax==0.4.14
   python3.9 -m pip install jaxlib==0.4.13
   ```

5. **Run the Experiment:**

   Change directory to `wluncert` and execute the experiment:

   ```sh
   cd wluncert
   python3.9 main.py --experiment multitask --jobs 1 --reps 30 --store
   ```

6. **Run the Analysis:**

   After the experiment completes, run the analysis:

   ```sh
   python3.9 modelinsights.py
   ```

7. **Start the Streamlit Dashboard:**

   Finally, start the Streamlit dashboard to visualize the insights:

   ```sh
   streamlit run playground/insights-dashboard.py
   ```

#### Summary

By following these steps, you should be able to set up and run the experiment locally on your machine without the need for Docker. This setup replicates the environment and steps defined in the Dockerfile.

#### Troubleshooting

If you encounter any issues:
- Ensure all dependencies are correctly installed.
- Check for typos or errors in the commands.




    
  </details>
    <details>
    <summary><h3>Changes for Reproduktion</h3></summary>
To change the software systems, the easiest way is to bring the data from your new software system into the same format as one of the existing software systems. You can find the data in [Training-Data](/experiment-code/wluncert/training-data).

After that, you need to modify `main.py` in the [wluncert](/experiment-code/wluncert/) directory:

- Add your software system's name to the `selected-data` list (line 216).
- Add your software system to the `get_datasets` function (line 511) using the `DataAdapter` from the software system with the same data format.
  </details>
</details>

