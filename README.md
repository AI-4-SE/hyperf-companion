# README

This repository provides additional content for the paper "Bayesian Multi-Level Performance Models for Multi-Factor
Variability of Configurable Software Systems".

## Paper

Johannes Dorn, Stefan Mühlbauer, Stefan Jahns, Sven Apel, and Norbert Siegmund.
*Bayesian Multi-Level Performance Models for Multi-Factor Variability of Configurable Software Systems.*
In Proceedings of the 48th IEEE/ACM International Conference on Software Engineering (ICSE 2026), April 12–18, 2026, Rio de Janeiro, Brazil.

- PDF (author version): [hyperf-icse-2026.pdf](https://sws.informatik.uni-leipzig.de/wp-content/uploads/2025/11/hyperf-icse-2026.pdf)
- DOI: [10.1145/3744916.3773131](https://doi.org/10.1145/3744916.3773131)

## Citation

If you refer to this work, please cite:

```bibtex
@inproceedings{dorn2026hyperf,
  author    = {Dorn, Johannes and M{\"u}hlbauer, Stefan and Jahns, Stefan and Apel, Sven and Siegmund, Norbert},
  title     = {Bayesian Multi-Level Performance Models for Multi-Factor Variability of Configurable Software Systems},
  booktitle = {Proceedings of the 48th IEEE/ACM International Conference on Software Engineering (ICSE '26)},
  year      = {2026},
  address   = {Rio de Janeiro, Brazil},
  publisher = {ACM},
  doi       = {10.1145/3744916.3773131}
}
```

## ABSTRACT

Tuning a software system’s configuration is essential to meet performance requirements.
However, not only do configuration options affect performance, but also the system’s interaction with external factors such as the workload.
Hence, tuning requires understanding how a specific *setting* of external factors (e.g., a specific workload) in combination with the system configuration influences performance.
To address this issue, we propose HyPerf, a *Bayesian multi-level performance modeling approach* that systematically distinguishes between *setting-invariant* and *setting-variant* influences, that is, influences that remain consistent across settings versus those that exhibit substantial variation.
With HyPerf, we aim at *balancing accuracy and efficiency*, achieving robust performance predictions with significantly fewer training samples.
Unlike the state of the art, HyPerf is able to *identify a minimal set of settings* that captures essential performance variations, so that developers can approximate whether all setting-variant influences have been accounted for.
Empirical evaluations on ten real-world software systems across up to 35 workloads and scalability experiments on the Linux kernel demonstrate that HyPerf matches or outperforms state-of-the-art approaches while requiring fewer measurements.
Notably, HyPerf is indeed capable of *interpretable performance reasoning* and can identify minimal workload subsets that capture essential performance variations.


## Supplementary Material

  <details>
    <summary><h3>RQ1</h3></summary>

[![pMAPE plot](supplementary-material/RQ1/RQ1-1/rq1-results.png)](supplementary-material/RQ1/RQ1-1/rq1-results.pdf)

You can view the pMAPE values in [the respective sub-folder](supplementary-material/RQ1/).
We also provide detailed training results for the TuxKConfig dataset in the sub-folder for [RQ1.3](supplementary-material/RQ1/RQ1-3).

  </details>
  <details>
    <summary><h3>RQ2</h3></summary>

[![rq2-informativeness-per-option](supplementary-material/RQ2/rq2-informativeness-per-option.png)](supplementary-material/RQ2/rq2-informativeness-per-option.pdf)
[![rq2-ratio-of-informative-options](supplementary-material/RQ2/rq2-ratio-of-informative-options.png)](supplementary-material/RQ2/rq2-ratio-of-informative-options.pdf)

Extending Figure 3 in the paper, you can compare all general influences against their workload-specific influences by
navigating [the respective sub-folder](supplementary-material/RQ2).


  </details>
  <details>
    <summary><h3>RQ3</h3></summary>


Extending Figure 5 in the paper, you can view all representation matrices for all options by
navigating [the respective "representation-matrices" subfolder for each software system](supplementary-material/RQ3).


Extending Figure 6 in the paper, you can view all representative set building protocols and plots by
navigating [the root subfolders for each software system](supplementary-material/RQ3).


Example for Z3:

[![set building for Z3](supplementary-material/RQ3/z3/rq3-set-building-z3.png)](supplementary-material/RQ3/z3/rq3-set-building-z3.pdf)


  </details>
<details open>
  <summary><h2>Replication Package</h2></summary>
   <h3>Experiment Parameters</h3>

  For running the experiments with any of the ways explained below, there are different parameters to be adjusted:
  - `--jobs` defines how many models are trained in parallel. Increasing it reduces the total run time without altering the results. Each job employs 3 MCMC chains, resulting in 3 required threads per job. E.g., for 6 available threads, choose `--jobs 2`.
  - `--store` should only be used if insights into posterior distributions are needed, e.g., when replicating the paper's plots through the provided dashboards.
  - `--reps` defines the number of repetitions. While the paper used 30 repetitions, we recommend reducing to 1 to check if everything works.
    If `--reps` is not given, `main.py` runs only 3 repetitions, so pass `--reps 30` to match the paper.
    The Docker `rq1` command below already defaults to 30 repetitions, whereas the `rq23` command always runs a single repetition.
  - `--training-set-size` disables the sweep over different training set sizes and, instead, only uses the given size. Passing 0.5 will train on 0.5N training data for all software systems listed in the main.py.
  - To replicate the RQs in the paper, use the commands for running the docker container as outlined below.

[//]: # (     - To replicate RQ1, use the rq1 command running the docker choose `--reps 30` and do not set the `--store` flag because it will likeliy fill up the hard disk.)

[//]: # (     - To replicate RQ2 and RQ3, choose `--reps 1 --store --training-set-size 3`, as posterior distributions must be stored, while only models the first random seed `0` were analyzed.)


<details>
    <summary><h3>Run as Docker (Replication)</h3></summary>

To run the full experiment via Docker, follow these steps:

1. **Install Docker:**
    - Refer to the [Docker Documentation](https://docs.docker.com/) for installation instructions.

2. **Clone the Repository:**
    - Navigate to the directory where you want to clone the repository and run:

   ```sh
   git clone https://github.com/AI-4-SE/hyperf-companion
   cd hyperf-companion/experiment-code
   ```
3. **Build the Docker Image:**
    - Open a terminal.
    - Change your directory to `path-of-repo/hyperf-companion/experiment-code`.
    - Run the following command:
      ```sh
      docker build ./ -t hyperf/repl
      ```

4. **Run RQ1 with the Docker Container:**
    - After the build is complete, run your Docker container with:
      ```sh
      docker run -it -p 8083:8083 --name hyperf-rq1 hyperf/repl rq1 --reps 5 --jobs 5
      ```
        - Adjust the number of jobs to your CPU; five repetitions should suffice to see robust trends, but do choose 30
          to replicate the paper's experiment (omitting `--reps` also runs 30 repetitions)
    - If you want to detach from the container during the experiment or after, without losing experiment data and the running dashboard, press `Ctrl + p` `Ctrl + q`
      - re-attach using your container name: `docker attach hyperf-rq1`
    - When the job is *finished*, explore the Streamlit dashboard at http://localhost:8083. You can change the port by
      replacing the port before the colon, i.e., `OUTERPORT:8083`.
    - To copy the results outside the docker use:
      ```sh
      docker cp hyperf-rq1:/app/wluncert/results /local/path
      ```
    - Optionally, once you no longer need the dashboard, stop and remove the container with
      `docker stop hyperf-rq1` and `docker rm hyperf-rq1`.

5. **Run RQ2 and RQ3 with the Docker Container:**
    - After the build is complete, run your Docker container with:
      ```sh
      docker run -it -p 8084:8084 --name hyperf-rq2-and-3 hyperf/repl rq23 --jobs 5
      ```
        - Adjust the number of jobs to your hardware; calling the rq23 command automatically only runs 1 repetition

    - Explore the Streamlit dashboard at http://localhost:8084.
    - To copy the results outside the docker use:
      ```sh
      docker cp hyperf-rq2-and-3:/app/wluncert/results /local/path
      ```
    - Optionally, once you no longer need the dashboard, stop and remove the container with
      `docker stop hyperf-rq2-and-3` and `docker rm hyperf-rq2-and-3`.


6. **Run custom experiments with the Docker Container:**
    - To set own parameters, use the custom-experiment command or start a bash in the new container:
      ```sh
      docker run -it -p 8083:8083 -p 8084:8084 --name hyperf-custom-experiment hyperf/repl custom-experiment --jobs 5 --reps 1 --training-set-size 5
      ```
      or
      ```sh
      docker run -it -p 8083:8083 -p 8084:8084 --name hyperf-custom-session --entrypoint bash hyperf/repl
      ```

  </details>

<details>
    <summary><h3>Changes for Reproduction</h3></summary>

To change the software systems, the easiest way is to bring the data from your new software system into the same format as one of the existing software systems. You can find the data in [Training-Data](experiment-code/wluncert/training-data).

After that, you need to modify `main.py` in the [wluncert](experiment-code/wluncert/) directory:

- Add your software system's label to the `selected_data` tuple in `main()` (in the non-debug branch), which determines the software systems used in the experiment.
- Add your software system to the `get_datasets()` function: load its data with the data loader and `DataAdapter` of the software system with the same data format, and add the result to `data_providers` under the same label as in `selected_data`.

If your software system has the same data layout as an existing one, you can reuse the existing adapter instead of writing a new one.
For example, x265 reuses `DataAdapterVP9` together with `DataLoaderStandard`, because both come as a single CSV file with the options, a `workload` column, and the same performance metrics as columns.
Software systems stored as a folder with a `sample.csv` (configurations) and a `measurements.csv` (measurements per workload, joined via `config_id`) are loaded with `DataLoaderDashboardData`, as for H2 or z3.
For this layout, `DataAdapterZ3` is an unchanged subclass of `DataAdapterX264`, which shows how an existing adapter can be reused.

  </details>

</details>

## License

This repository contains parts under different licenses. [REUSE.toml](REUSE.toml) assigns a license to every file, and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) lists all third-party material.

| Part | Location | License |
|---|---|---|
| Code, scripts and documentation by the authors | everything not listed below (e.g., `experiment-code/`) | [MIT](LICENSE) |
| Measurements and results by the authors | `supplementary-material/`; in `experiment-code/wluncert/training-data/`: `measurements_VP9_*.csv`, `measurements_x265_*.csv`, `performance-across-workloads-and-evolution/`, `artificial/` | [CC BY 4.0](LICENSES/CC-BY-4.0.txt) |
| Workload performance data of Mühlbauer et al. (ICSE 2023) | `experiment-code/wluncert/training-data/dashboard-resources/` | [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt), see [its LICENSE.md](experiment-code/wluncert/training-data/dashboard-resources/LICENSE.md) |
| Measurement files of unclear provenance | in `experiment-code/wluncert/training-data/`: `batik.csv`, `dconvert.csv`, `h2.csv`, `jadx.csv`, `jump3r.csv`, `kanzi.csv`, `measurements_lrzip-0.651.csv`, `measurements_xz-5.2.0.csv` | **Not covered by our licenses**; provenance to be clarified ([details](LICENSES/LicenseRef-Unclear-Provenance.txt)) |

Copyright of the parts by the authors: 2024–2025 Johannes Dorn, Stefan Mühlbauer, Stefan Jahns, Sven Apel, Norbert Siegmund.

**Third-party material**

- `dashboard-resources/` contains data from S. Mühlbauer, F. Sattler, C. Kaltenecker, J. Dorn, S. Apel, N. Siegmund: "Analyzing the Impact of Workloads on Modeling the Performance of Configurable Software Systems", ICSE 2023, https://doi.org/10.5281/zenodo.7658046 (CC BY-SA 4.0).
- **DaL:** The DaL baseline (`model_dal_no_pooling`, `model_dal_cpooling`) uses helper modules from [DaL-ext](https://github.com/ideas-labo/DaL-ext) by J. Gong, T. Chen et al. DaL-ext has no license, so these modules are not part of this repository. To download them at the pinned commit, run `python3 fetch_dal.py` in `experiment-code/` (the Docker build does this automatically). The downloaded files are not covered by our license. Without them, everything else works; only the two DaL models are unavailable.
- `experiment-code/wluncert/deepperf.py` is our own re-implementation of DeepPerf (H. Ha, H. Zhang, ICSE 2019, https://doi.org/10.1109/ICSE.2019.00113).
- The TuxKConfig data is not included. `experiment-code/wluncert/training-data/getTuxKConfig.py` downloads it from OpenML. Original dataset: M. Acher et al., https://doi.org/10.5281/zenodo.7433623 (CC BY 4.0).
- [pycosa-toolbox](https://github.com/smba/pycosa-toolbox) (AGPL-3.0) is a Python dependency in `requirements.txt`. pip installs it; it is not part of this repository.

The paper is published under CC BY-NC-ND 4.0. That license applies only to the paper, not to this repository.

**Please cite** our paper if you use this repository; see [Citation](#citation) and [CITATION.cff](CITATION.cff).
