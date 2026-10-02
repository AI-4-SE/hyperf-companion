#!/usr/bin/env python3
"""Download the third-party DaL helper modules used by the DaL baseline.

The DaL baseline of this replication package (``wluncert/dal/regressor.py``,
our own scikit-learn wrapper) builds on helper modules from DaL-ext by
J. Gong, T. Chen et al. (https://github.com/ideas-labo/DaL-ext). DaL-ext does
not come with a license, so we do not redistribute these modules. Instead,
this script

1. downloads DaL-ext and reads the files of a pinned commit (``git clone``;
   if git is not available or fails, the GitHub tarball of that commit),
2. checks the SHA-256 of every upstream file it uses,
3. copies the files into ``wluncert/dal/utils/`` (same names as upstream),
4. re-applies our small local changes as targeted string replacements
   (relative imports, ``tf.layers.dense`` -> ``tf.keras.layers.Dense`` for
   TensorFlow 2, and two bug fixes in the recursive tree division), and
5. checks the SHA-256 of every resulting file, so the result is exactly the
   code we used for the experiments.

Usage (from ``experiment-code/``)::

    python3 fetch_dal.py            # fetch, patch, verify
    python3 fetch_dal.py --check    # only verify an existing installation
    python3 fetch_dal.py --source /path/to/DaL-ext   # use a local copy

Only the Python standard library is needed. The fetched files are listed in
``.gitignore`` and are not covered by the license of this repository.
"""

import argparse
import hashlib
import io
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

REPO_URL = "https://github.com/ideas-labo/DaL-ext.git"
COMMIT = "0a510274cee46d08987a6cd2587d1135996e8167"
TARBALL_URL = "https://codeload.github.com/ideas-labo/DaL-ext/tar.gz/" + COMMIT

HERE = os.path.dirname(os.path.abspath(__file__))
DEST_DIR = os.path.join(HERE, "wluncert", "dal", "utils")

# SHA-256 of the files at COMMIT (upstream) and after our patches (result).
FILES = {
    "HINNPerf_args.py": (
        "fc5c98f6e918b49665cc5892a88b283aecb2ab7bb2efbbdd4ef8593ea738105a",
        "fc5c98f6e918b49665cc5892a88b283aecb2ab7bb2efbbdd4ef8593ea738105a",
    ),
    "HINNPerf_data_preproc.py": (
        "bae7468b00eea839d207755feeb199d91d3722312026e5004433b476a4148c35",
        "bae7468b00eea839d207755feeb199d91d3722312026e5004433b476a4148c35",
    ),
    "HINNPerf_model_runner.py": (
        "60feaa3da21f9fa28868bb81dca4f69d6c0b51c1ef2cf02f8042afbc761416f6",
        "e8c67ad0f41c5742097b9e871d9fc498dac201b8c8d5b62c63d8f594da4cb920",
    ),
    "HINNPerf_models.py": (
        "dff35274fc49247294f428e747613b257cb54e6e2040fa6950b4e1a8bf6ec713",
        "a56112bfdc27d607ec575382d5f67a42ebc79c8f7c7383d8c853a4aadb781f12",
    ),
    "adapting_depth.py": (
        "f2bca2fe689e566b0e85a7183b70adbf5ac1f70b8792d6132a9344447a521819",
        "027b8f3b4bffeb4c075f118986d345243a84d98468c87b58ae8504dce4a9b78f",
    ),
    "general.py": (
        "d4cd7c747197e5050c9967b1eb4b32386d49b9f31ca6aa3b6f508fbfe78c1782",
        "5e6c1216a6f7b0af5a805adc20c22f3ef4e93fe6090a476da0c3f879250d8712",
    ),
    "hyperparameter_tuning.py": (
        "fdfe2a2e4e85c1b5612cddc5926c6083958a57aefda3fb56506f687d4fa5bf05",
        "c1608e15671c8ba6438eca0e9ee5b421282ba007e526157c04f77a4cbcbc140d",
    ),
    "mlp_plain_model_tf2.py": (
        "67797164025f3602ead6886c7187c3badccb6850ef814e5ec3c02206a4dfba2c",
        "f3cfa5eae2a54afb8382b1622620d1cdd53845574b165d6e288c2fcf52aaf832",
    ),
    "mlp_sparse_model_tf2.py": (
        "9a6d6636e1c1c1a5f832e1f8fb3bd5d31004095fb3ca805f1945d45bf9a22a05",
        "3a11a7642b1682a70c2ba3b00f47ce7c8fb90d0f0b2fa855753847886bf53f42",
    ),
    "runHINNPerf.py": (
        "b49933f75dff408d06ff3d12e86189e8f7d92c31b389e2826af49f7da4546699",
        "cacf17444a585d301448945f0c7b78431d6599fb95b66e298005d7a76f3297f1",
    ),
}

# --- Local modifications ----------------------------------------------------
# Each entry is (old, new, expected number of occurrences of old).

# Upstream imports its helpers as top-level package "utils"; we use the
# package-relative form so that "wluncert/dal/utils" works as a subpackage.
def _relative_imports(n):
    return ("from utils.", "from .", n)


# The recursive division indexed X with the loop counter instead of the
# sample index.
_FIX_SAMPLE_INDEX = ("X[i_sample, name]", "X[samples[i_sample], name]", 1)


def _dense(indent, units, extra, dtype):
    """Build a tf.keras.layers.Dense(...)(layer) call in our formatting."""
    pad = " " * (indent + 4)
    args = [units] + extra + (["dtype=tf.float32"] if dtype else [])
    body = "".join("{}{},\n".format(pad, a) for a in args)
    return "tf.keras.layers.Dense(\n{}{})".format(body, " " * indent)


_RELU = "activation=tf.nn.relu"
_GLOROT = "kernel_initializer=tf2.initializers.GlorotUniform(seed=1)"
_L1_LAMDA = "kernel_regularizer=tf.keras.regularizers.l1(float(self.lamda))"
_L2_LAMDA = "kernel_regularizer=tf.keras.regularizers.l2(float(self.lamda))"
_L1_LAMBD = "kernel_regularizer=tf.keras.regularizers.l1(float(lambd))"

PATCHES = {
    "HINNPerf_args.py": [],
    "HINNPerf_data_preproc.py": [],
    "HINNPerf_model_runner.py": [_relative_imports(1)],
    # TensorFlow 2: tf.compat.v1.layers.dense -> tf.keras.layers.Dense
    "HINNPerf_models.py": [
        (
            "tf.layers.dense(linear_input, 1, " + _L2_LAMDA + ")",
            _dense(12, "1", ["activation=None", _L2_LAMDA], True) + "(linear_input)",
            1,
        ),
        (
            "tf.layers.dense(layer, self.num_neuron, tf.nn.relu,\n"
            + " " * 40 + _GLOROT + ",\n"
            + " " * 40 + _L1_LAMDA + ")",
            _dense(16, "self.num_neuron", [_RELU, _GLOROT, _L1_LAMDA], True) + "(layer)",
            1,
        ),
        (
            "tf.layers.dense(layer, self.num_neuron, tf.nn.relu,\n"
            + " " * 40 + _GLOROT + ")",
            _dense(16, "self.num_neuron", [_RELU, _GLOROT], True) + "(layer)",
            1,
        ),
        (
            "tf.layers.dense(layer, self.input_dim, tf.nn.relu)",
            _dense(8, "self.input_dim", [_RELU], True) + "(layer)",
            1,
        ),
        (
            "tf.layers.dense(layer, 1)",
            "tf.keras.layers.Dense(1, dtype=tf.float32)(layer)",
            1,
        ),
    ],
    "adapting_depth.py": [_relative_imports(4), _FIX_SAMPLE_INDEX],
    "general.py": [
        # avoid a mutable default argument that leaks clusters between calls
        (
            "min_samples=2, cluster_indexes_all=[]):\n"
            '    indent = "  " * depth\n',
            "min_samples=2, cluster_indexes_all=None):\n"
            '    indent = "  " * depth\n'
            "    if cluster_indexes_all is None:\n"
            "        cluster_indexes_all = []\n",
            1,
        ),
        _FIX_SAMPLE_INDEX,
    ],
    "hyperparameter_tuning.py": [_relative_imports(2)],
    "mlp_plain_model_tf2.py": [
        _relative_imports(1),
        (
            "tf.layers.dense(layer, n_neuron, tf.nn.relu,\n"
            + " " * 32 + _GLOROT + ")",
            _dense(8, "n_neuron", [_RELU, _GLOROT], False) + "(layer)",
            1,
        ),
        ("tf.layers.dense(layer, 1)", "tf.keras.layers.Dense(1)(layer)", 1),
    ],
    "mlp_sparse_model_tf2.py": [
        _relative_imports(1),
        (
            "tf.layers.dense(layer, n_neuron, tf.nn.relu,\n"
            + " " * 36 + _GLOROT + ",\n"
            + " " * 36 + _L1_LAMBD + ", name=str(i))",
            _dense(12, "n_neuron", [_RELU, _GLOROT, _L1_LAMBD, "name=str(i)"], False)
            + "(layer)",
            1,
        ),
        (
            "tf.layers.dense(layer, n_neuron, tf.nn.relu,\n"
            + " " * 36 + _GLOROT + ", name=str(i))",
            _dense(12, "n_neuron", [_RELU, _GLOROT, "name=str(i)"], False) + "(layer)",
            1,
        ),
        (
            "tf.layers.dense(layer, 1, name='o')",
            "tf.keras.layers.Dense(1, name='o')(layer)",
            1,
        ),
    ],
    "runHINNPerf.py": [_relative_imports(5)],
}


class FetchError(Exception):
    pass


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def apply_patches(name, text):
    for i, (old, new, count) in enumerate(PATCHES[name], start=1):
        found = text.count(old)
        if found != count:
            raise FetchError(
                "{}: replacement #{} expected {} occurrence(s) of {!r}, found {}. "
                "Has the upstream file changed?".format(name, i, count, old, found)
            )
        text = text.replace(old, new)
    return text


def _run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)


def read_with_git(workdir):
    """Clone DaL-ext and read the files from the pinned commit."""
    if shutil.which("git") is None:
        raise FetchError("git is not installed")
    clone = os.path.join(workdir, "DaL-ext")
    print("Cloning {} ...".format(REPO_URL))
    _run(["git", "clone", "--quiet", "--no-checkout", REPO_URL, clone])
    _run(["git", "-C", clone, "rev-parse", "--quiet", "--verify", COMMIT + "^{commit}"])
    result = {}
    for name in FILES:
        # read the blobs of the pinned commit directly (no checkout needed),
        # independent of local line-ending settings
        result[name] = subprocess.run(
            ["git", "-C", clone, "cat-file", "blob", "{}:utils/{}".format(COMMIT, name)],
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
    return result


def read_with_tarball():
    """Download the GitHub tarball of the pinned commit."""
    print("Downloading {} ...".format(TARBALL_URL))
    with urllib.request.urlopen(TARBALL_URL, timeout=300) as response:
        payload = response.read()
    result = {}
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as tar:
        members = {m.name.split("/", 1)[-1]: m for m in tar.getmembers() if m.isfile()}
        for name in FILES:
            member = members.get("utils/" + name)
            if member is None:
                raise FetchError("utils/{} is missing in the tarball".format(name))
            result[name] = tar.extractfile(member).read()
    return result


def read_from_source(source):
    """Read the files from an existing DaL-ext checkout or extracted tarball."""
    result = {}
    for name in FILES:
        path = os.path.join(source, "utils", name)
        if not os.path.isfile(path):
            raise FetchError("{} not found".format(path))
        with open(path, "rb") as fh:
            result[name] = fh.read()
    return result


def download():
    with tempfile.TemporaryDirectory(prefix="dal-ext-") as workdir:
        try:
            return read_with_git(workdir)
        except (FetchError, OSError, subprocess.CalledProcessError) as error:
            print("git download failed ({}); trying the tarball.".format(error))
    return read_with_tarball()


def check_upstream(files):
    bad = [n for n, data in files.items() if sha256(data) != FILES[n][0]]
    if bad:
        raise FetchError(
            "Upstream files differ from DaL-ext commit {}: {}".format(COMMIT, ", ".join(bad))
        )


def installed_state():
    """Return (missing, modified) lists for the files in DEST_DIR."""
    missing, modified = [], []
    for name, (_, expected) in FILES.items():
        path = os.path.join(DEST_DIR, name)
        if not os.path.isfile(path):
            missing.append(name)
            continue
        with open(path, "rb") as fh:
            if sha256(fh.read()) != expected:
                modified.append(name)
    return missing, modified


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="only verify the installed files")
    parser.add_argument("--force", action="store_true", help="overwrite locally modified files")
    parser.add_argument("--source", help="use an existing DaL-ext checkout instead of downloading")
    args = parser.parse_args()

    missing, modified = installed_state()
    if args.check or (not missing and not modified and not args.force):
        if missing or modified:
            print("DaL files missing: {}; modified: {}".format(missing or "-", modified or "-"))
            print("Run: python3 fetch_dal.py" + (" --force" if modified else ""))
            return 1
        print("DaL files in {} are present and verified (DaL-ext {}).".format(DEST_DIR, COMMIT[:7]))
        return 0
    if modified and not args.force:
        print("Locally modified DaL files: {}. Use --force to overwrite.".format(", ".join(modified)))
        return 1

    try:
        upstream = read_from_source(args.source) if args.source else download()
        check_upstream(upstream)
        patched = {}
        for name, data in upstream.items():
            text = apply_patches(name, data.decode("utf-8"))
            patched[name] = text.encode("utf-8")
            if sha256(patched[name]) != FILES[name][1]:
                raise FetchError("{}: unexpected result after patching".format(name))
    except (FetchError, OSError, subprocess.CalledProcessError) as error:
        print("ERROR: {}".format(error), file=sys.stderr)
        return 1

    os.makedirs(DEST_DIR, exist_ok=True)
    init_file = os.path.join(DEST_DIR, "__init__.py")
    if not os.path.exists(init_file):
        open(init_file, "w").close()
    for name, data in patched.items():
        with open(os.path.join(DEST_DIR, name), "wb") as fh:
            fh.write(data)
    print("Installed {} DaL files into {} (DaL-ext {}, verified).".format(len(patched), DEST_DIR, COMMIT[:7]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
