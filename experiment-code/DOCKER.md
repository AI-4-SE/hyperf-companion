# Docker image: contents and relation to the paper's environment

The experiments in the paper were **not** run in this image but directly on
a server (two AMD EPYC 7302, 256 GB RAM): the 2024 runs (RQ1.1) and the 2025
runs (RQ1.2, RQ1.3). The image reproduces the software environment of the
2025 runs as closely as possible, without a GPU. How to build and run it is
described in the main README; this file explains what is in the image.

## Contents

- Base image `ubuntu:22.04` with its system Python **3.10** (3.10.12; the
  paper used 3.10.4) and pip from Ubuntu.
- The Python packages of [`requirements.txt`](requirements.txt), installed
  in the exact versions of [`requirements-lock.txt`](requirements-lock.txt).
- The DaL helper modules, downloaded and verified by
  [`fetch_dal.py`](fetch_dal.py) during the build.
- CPU only, `linux/amd64`. On ARM hosts (e.g. Apple Silicon), build and run
  with `--platform linux/amd64`.
- Size about 4.9 GB; the first build downloads about 1 GB.

Main package versions:

| Package | Paper | 2024 runs (RQ1.1) | 2025 runs (RQ1.2, RQ1.3) | Docker image |
|---|---|---|---|---|
| Python | 3.10.4 | – | 3.10 | 3.10.12 |
| NumPyro | 0.12.1 | 0.12.1 | 0.12.1 | 0.12.1 |
| JAX / jaxlib | – | 0.4.14 | 0.4.20 | 0.4.20 |
| ArviZ | 0.16.1 | not pinned | `~=0.15.1` | 0.16.1 |
| NumPy | – | 1.25.0 | 1.24.3 | 1.24.3 |
| SciPy | – | not pinned | 1.11.4 | 1.11.4 |
| scikit-learn | – | not pinned | 1.2.2 | 1.2.2 |
| pandas | – | not pinned | not pinned | 2.3.1 |
| TensorFlow | – | – | 2.13.1 (`tensorflow[and-cuda]`) | 2.13.1 (`tensorflow-cpu`) |
| PyTorch | – | not pinned (via pyro-ppl) | 2.1.0 | 2.1.0 (CPU wheel) |
| Streamlit | – | 1.30.0 | `>=1.30.0` | 1.47.0 |

The 2024 and 2025 columns are the versions pinned in `requirements.txt` of
the development repository at the time of the runs (May 2024 and July
2025; Python 3.10 is the version the 2025 requirements were adapted to). Which versions of the unpinned packages were installed on the server
is not recorded. For the image, they are resolved as of 22 July 2025 (the
day after the final 2025 update of this repository), see below.

## Changes compared with the earlier Dockerfile

The earlier Dockerfile (June 2024, unchanged in July 2025) installed Python
3.9 from the deadsnakes PPA and then replaced JAX by `jax[cpu]==0.4.18`.
That matched neither the paper (Python 3.10) nor `requirements.txt`
(JAX 0.4.20). Changes:

- **Python 3.10** from Ubuntu instead of 3.9 from the deadsnakes PPA (and
  without `software-properties-common`, which was only needed for the PPA).
- **No JAX override**: JAX/jaxlib 0.4.20 as in `requirements.txt`.
- **CPU builds of the same versions**: `tensorflow-cpu==2.13.1` instead of
  `tensorflow[and-cuda]==2.13.1`, and the PyTorch CPU wheel `2.1.0+cpu`
  instead of `torch==2.1.0` with CUDA libraries. `tensorrt==10.0.1` is
  dropped: nothing imports it, and TensorFlow 2.13 expects TensorRT 8. The
  experiments use no GPU, and the CUDA packages would add several GB.
- **ArviZ 0.16.1**, the version reported in the paper (the 2025
  requirements had `arviz~=0.15.1`).
- **pycosa-toolbox dropped**: no code imports it; it was installed from git
  and pulled in further packages (z3-solver, pyeda, statsmodels, ...).
- **Lock file**: `requirements-lock.txt` pins every package, so that the
  image no longer depends on the day it is built. The unpinned packages of
  `requirements.txt` are taken as of 22 July 2025 instead of their newest
  releases. (Resolving `requirements.txt` against the newest releases with
  the pip of Ubuntu 22.04 was still backtracking after 10 minutes in our
  test, mainly because `typing-extensions==4.5.0`, which TensorFlow 2.13
  requires, conflicts with recent releases of MLflow's dependencies.)
- Packages are installed before the code is copied (code changes do not
  trigger a reinstall), `.dockerignore` keeps local results, caches and
  downloaded third-party files out of the image, `mkdir -p` no longer fails
  if the folders exist, and the output of the scripts is unbuffered
  (`docker logs` shows it immediately).
- `entrypoint.py`: uses the image's Python instead of a hard-coded
  `python3.9`, no longer passes `--reps None` (which crashed `main.py`)
  when `--reps` is not given (`main.py` then uses its default of 3
  repetitions), and passes `--browser.gatherUsageStats false` to Streamlit
  as an option (before, it was passed on to the dashboard script and had no
  effect).

`requirements-frozen.txt` (2022: NumPyro 0.9, JAX 0.3, pandas 1.4) was
removed. It was used neither by the image nor for the paper's runs and is
superseded by `requirements-lock.txt`.

## Regenerating `requirements-lock.txt`

After changing `requirements.txt`, resolve it again in a clean Ubuntu 22.04
container (from `experiment-code/`). `--uploaded-prior-to` (pip 26 or
newer) only considers releases up to the given date; to use the newest
releases instead, remove it.

```sh
docker run --rm -v "$PWD/requirements.txt:/src/requirements.txt:ro" -w /src ubuntu:22.04 bash -c '
  set -e
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -qq
  apt-get install -y -qq git python3 python3-dev python3-venv build-essential pkg-config libhdf5-dev > /dev/null
  python3 -m venv /venv && . /venv/bin/activate
  pip install -q pip==26.2.1
  pip install -q --no-deps --index-url https://download.pytorch.org/whl/cpu torch==2.1.0+cpu
  pip install -q --uploaded-prior-to 2025-07-22T00:00:00Z -r requirements.txt >&2
  pip check >&2
  pip freeze --all --exclude pip' > requirements-lock.new
```

Then replace the package lines of `requirements-lock.txt` with those of
`requirements-lock.new` (keep the header comment), rebuild the image and
check that `python3 -m pip check` passes.

## Installing without Docker

On Linux x86_64 with Python 3.10, the same versions can be installed into a
virtual environment:

```sh
python3.10 -m venv venv && . venv/bin/activate
pip install --no-deps --index-url https://download.pytorch.org/whl/cpu torch==2.1.0+cpu
pip install -r requirements-lock.txt
python fetch_dal.py
```
