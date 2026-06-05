# Pepkio Serial Dilution Planner

Container image bundling the Serial Dilution Planner CLI so pipelines and lab systems can call the Pepkio API without a local Python install.

# What It Does

The image runs `pepkio-serial-dilution-planner`, a client for the Pepkio Serial Dilution Planner REST API. It produces step-by-step dilution protocols with pipette-rounded transfer volumes, diluent amounts, per-step concentrations, optional 96/384-well plate maps, and shareable permalinks.

Serial dilution supports dose–response setup, standard curves, qPCR template series, inhibitor titrations, and antibody working dilutions. Calculator logic runs on Pepkio servers; provide a network connection and API key for `run` commands.

# Features

- Pipette-aware volume rounding and transfer warnings
- Economy mode and automatic step expansion for extreme concentration ratios
- Mass–molar conversion via molecular weight
- Named manifest examples (e.g. `standard_4step`, `plate_map_384`)
- Manifest inspection without an API key

# Quick Start

```bash
docker pull pepkio/serial-dilution-planner:0.1.2
docker run --rm -e PEPKIO_API_KEY="your-key" pepkio/serial-dilution-planner:0.1.2 \
  pepkio-serial-dilution-planner run --example standard_4step
```

Manifest only (no API key):

```bash
docker run --rm pepkio/serial-dilution-planner:0.1.2 \
  pepkio-serial-dilution-planner manifest --examples
```

# Quick Example

```bash
docker run --rm -e PEPKIO_API_KEY="$PEPKIO_API_KEY" pepkio/serial-dilution-planner:0.1.2 \
  pepkio-serial-dilution-planner run --input-json \
  '{"stock_concentration":10,"stock_unit":"mM","target_concentration":10,"target_unit":"uM","num_steps":4,"final_volume_ul":100}'
```

# Typical Use Cases

- Serial dilution from mM stock to µM working concentration
- ELISA and qPCR standard curve preparation
- Antibody dilution with mass-to-molar conversion
- 384-well plate mapping for high-throughput assays
- CI or workflow runners that need a fixed client environment

# Scientific Background

Constant-ratio serial dilution uses dilution factor DF = Cᵢ / Cᵢ₊₁ at each step; after n steps, Cₙ = C₀ / DFⁿ. Large total dilutions are split into multiple steps so transfers stay within pipette range. Volumes should match pipette resolution to avoid bench rounding error.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/serial-dilution-planner

The web UI adds bench mode, plate map CSV/PNG export, printable worksheets, and shareable links equivalent to API permalinks.

# Documentation and Resources

GitHub Repository (source and Dockerfile): https://github.com/pepkio/pepkio-serial-dilution-planner

Web Application: https://www.pepkio.com/tools/serial-dilution-planner

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services.
