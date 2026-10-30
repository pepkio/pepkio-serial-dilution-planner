# Pepkio Serial Dilution Planner

Python client for the Pepkio Serial Dilution Planner API: pipette-aware multi-step protocols, standard curves, and optional 96/384-well plate layouts from scripts or notebooks.

# What It Does

Serial dilution prepares a geometric concentration series from one stock solution. Researchers use it for dose–response setups, ELISA and qPCR standard curves, inhibitor titrations, antibody working dilutions, and protein standards.

Planning by hand or in a spreadsheet often mixes unit conversions, total dilution ratio, and step count inconsistently. Transfer volumes that look correct on paper (for example 18.37 µL) may not match pipette increments. Mapping tubes to microplate wells adds separate bookkeeping.

This package calls the same Pepkio Tools calculation engine as the hosted web application. Use `PepkioClient.run()` from Python, Jupyter, or automation pipelines to obtain step-by-step protocols with pipette-rounded volumes, diluent amounts, concentrations per step, optional plate maps, and shareable run links.

Programmatic runs require a network connection and a Pepkio API key. Calculations are not bundled for offline use.

# Features

- Concentration units: molar (`M`, `mM`, `uM`, `nM`), mass per volume (`mg_per_mL`, `ug_per_uL`, `ng_per_uL`), and `percent`
- Pipette-aware volumes: declare pipettes (`min_ul`, `max_ul`, `resolution_ul`); receive rounded `transfer_ul` and `pipette_label` per step
- Step-by-step output: concentration display, transfer volume, diluent volume, and warnings
- Economy mode to reduce reagent use within pipette limits
- Automatic extra steps when a single-step dilution would exceed roughly 1000×
- Mass–molar conversion via `molecular_weight_g_per_mol`
- Optional `plate_map` for 96- or 384-well layouts
- Manifest and named examples: `get_manifest`, `list_examples`, `get_example_input`
- CLI: `pepkio-serial-dilution-planner manifest` and `run`
- Configuration via `PEPKIO_API_KEY` and `PEPKIO_API_BASE_URL`

# Installation

```bash
pip install pepkio-serial-dilution-planner
```

Set an API key with **tools:run** scope before calling `run()`:

```bash
export PEPKIO_API_KEY="your-key"
```

Create a key in your [Pepkio account API keys](https://www.pepkio.com/account/api-keys) settings.

# Quick Example

```python
from pepkio_serial_dilution_planner import PepkioClient

with PepkioClient() as client:
    inp = client.get_example_input("standard_4step")
    result = client.run(inp)
    for step in result.result["steps"]:
        print(step["step"], step["concentration_display"],
              step["transfer_ul"], step["pipette_label"])
```

CLI:

```bash
pepkio-serial-dilution-planner run --example standard_4step
```

Manifest inspection does not require an API key.

# Typical Use Cases

- Serial dilution planning (for example 10 mM to 10 µM in four steps)
- Standard curve preparation for ELISA and immunoassays
- qPCR template dilution and standard series
- Antibody dilution from mg/mL stock to molar working concentration
- 96- or 384-well plate layout for high-throughput assays
- Limited reagent volume with economy mode and small pipettes
- Large stock-to-target concentration span with automatic step expansion

# Scientific Background

In a constant-ratio serial dilution, each step uses the same dilution factor DF = Cᵢ / Cᵢ₊₁. After n steps from initial concentration C₀, the concentration is Cₙ = C₀ / DFⁿ.

When the total dilution is large, one step may need a transfer volume below the pipette minimum or above its maximum. Splitting into multiple serial steps keeps each transfer pipettable and improves mixing.

Standard curves for ELISA, qPCR, and binding assays are often built as a geometric (log-spaced) concentration series from a concentrated stock.

Protocols should use volumes rounded to the pipette you will use at the bench; otherwise the achieved concentration differs from the ideal calculated value.

# Web Application

For researchers who prefer a graphical interface, an interactive [Serial Dilution Planner](https://www.pepkio.com/tools/serial-dilution-planner) is available in the browser.

The web interface adds bench mode (check-off steps at the hood), economy mode, 96/384-well plate maps with CSV or PNG export, printable worksheets, and shareable links that restore the same plan as API `permalink` values.

# Documentation and Resources

Source code and issue tracking: [github.com/pepkio/pepkio-serial-dilution-planner](https://github.com/pepkio/pepkio-serial-dilution-planner)

# About Pepkio

Pepkio develops software tools and provides bioinformatics analysis services for life science research. See https://www.pepkio.com for additional tools and services.

# Keywords

serial dilution, serial dilution calculator, serial dilution planner, dilution factor, dilution series, logarithmic dilution, geometric dilution, C1V1=C2V2, concentration dilution, mM to uM dilution, micromolar dilution, standard curve preparation, ELISA standard curve, qPCR dilution, qPCR standard curve, dose response dilution, antibody dilution, protein dilution, pipette volume calculator, pipette-aware dilution, transfer volume, diluent volume, 96-well plate map, 384-well plate map, microplate dilution layout, laboratory dilution protocol, serial dilution protocol, ten-fold serial dilution, stock solution dilution, working solution preparation, molecular biology calculator, pepkio-serial-dilution-planner, Python dilution API, lab automation dilution, economy mode dilution, mass to molar conversion, mg/mL to uM, pipette rounding, high-throughput dilution plate, how to perform a serial dilution in the lab, how to calculate serial dilution step volumes, serial dilution from mM to uM calculator, how many steps for 1000 fold dilution, how to make a 10-fold serial dilution, how to prepare ELISA standard curve by serial dilution, qPCR template serial dilution protocol, how to map serial dilution to 96 well plate, 384 well serial dilution layout, pipette volume too small for serial dilution, round microliter volumes to P20 pipette, what is dilution factor in serial dilution, antibody serial dilution from mg/mL, convert mg per mL to micromolar for dilution, standard curve log spacing dilution factor, shareable lab protocol link dilution, printable serial dilution worksheet, minimize reagent use serial dilution, auto expand dilution steps large concentration range, Python script serial dilution protocol, API for laboratory dilution planning, serial dilution for inhibitor titration, immunoassay dilution series planning, dose response serial dilution 96 well, how to dilute stock for standard curve qPCR, export plate map CSV serial dilution
