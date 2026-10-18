#!/usr/bin/env bash
# Fetch Seshat data releases into data/raw/ (gitignored).
# Equinox2020 is scriptable (public GitHub mirror). Polaris2025/2026 is not yet: see README "Data".
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/raw
if [ ! -d data/raw/equinox_data ]; then
  git clone --depth 1 https://github.com/seshatdb/Equinox_Data data/raw/equinox_data
fi
git -C data/raw/equinox_data rev-parse HEAD > data/raw/equinox_data.COMMIT
sha256sum data/raw/equinox_data/*.xlsx | tee data/raw/equinox_data.SHA256
# Polaris2026 (+ an Equinox2020 May-2023 copy) from the official build repo
if [ ! -d data/raw/build_polaris_dataset ]; then
  GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/Seshat-Global-History-Databank/build_polaris_dataset data/raw/build_polaris_dataset
fi
git -C data/raw/build_polaris_dataset rev-parse HEAD > data/raw/build_polaris_dataset.COMMIT
sha256sum data/raw/build_polaris_dataset/*.xlsx | tee data/raw/build_polaris_dataset.SHA256
