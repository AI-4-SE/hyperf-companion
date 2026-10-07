# License of the data in this folder

The files in this folder are **not** covered by the MIT License or the
CC BY 4.0 license of the rest of this repository.

They are taken from the supplementary material of

> S. Mühlbauer, F. Sattler, C. Kaltenecker, J. Dorn, S. Apel, N. Siegmund:
> "Analyzing the Impact of Workloads on Modeling the Performance of
> Configurable Software Systems". In *Proceedings of the 45th IEEE/ACM
> International Conference on Software Engineering (ICSE 2023)*, pp. 2085–2097.
> https://doi.org/10.1109/ICSE48619.2023.00176
>
> Supplementary material (version 1.2): https://doi.org/10.5281/zenodo.7658046

Copyright 2023 Stefan Mühlbauer, Florian Sattler, Christian Kaltenecker,
Johannes Dorn, Sven Apel, Norbert Siegmund.

## License

[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/),
full text in [`/LICENSES/CC-BY-SA-4.0.txt`](../../../../LICENSES/CC-BY-SA-4.0.txt).

The Zenodo record lists CC BY 4.0 in its metadata, while the license file
included in the record (`LICENCSE.md`) names CC BY-SA 4.0. We apply the more
restrictive CC BY-SA 4.0. If you share this data or adaptations of it, you
must give credit as above and share them under the same license.

## Changes

This folder contains a subset of `dashboard/resources/` from the archive
`artifact_excluding_raw_coverage.zip` of the Zenodo record, namely the
systems batik, dconvert, h2, jump3r, kanzi, lrzip, x264, xz and z3.

- 1,996 of the 1,997 files are byte-identical to the original files
  (checked on 2026-10-02 via CRC-32 and file size).
- `dconvert/measurements.csv`: an empty last row (`,,`, without a final line
  break) was appended.
- `z3/clean.py` is part of the original material. It reduces
  `z3/measurements.csv` to the rows with `partition == 5`; the
  `measurements.csv` in this folder is identical to the one on Zenodo.
