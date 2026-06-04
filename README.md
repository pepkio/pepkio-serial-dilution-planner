# Pepkio Serial Dilution Planner

Python client for the Pepkio Serial Dilution Planner API: pipette-aware serial dilution protocols, standard curves, and 96/384-well plate layouts.

# Overview

Serial dilution is a standard laboratory technique for preparing a logarithmic or geometric concentration series from a single stock solution. Researchers use serial dilutions for dose–response curves, ELISA and immunoassay standard curves, qPCR template dilutions, inhibitor titrations, antibody working dilutions, and protein standard preparation. Each step transfers a fraction of the previous tube into fresh diluent, so concentrations decrease in a predictable ratio—the dilution factor—rather than by arbitrary one-off dilutions.

Planning a series by hand or in a spreadsheet introduces several practical problems. Unit conversions (for example millimolar to micromolar), total dilution ratio, and number of steps must be consistent. Transfer volumes must fit available pipettes and their resolution (0.1 µL on a P2, 1 µL on a P200). Values that look correct on paper—18.37 µL—are not pipettable without rounding, and manual rounding at the bench is a common source of error. Mapping tubes to microplate wells for triplicates or high-throughput layouts adds another layer of bookkeeping.

The [Pepkio Serial Dilution Planner](https://www.pepkio.com/tools/serial-dilution-planner) web application computes step-by-step protocols with pipette-rounded transfer volumes, diluent volumes, concentration at each step, and optional 96- or 384-well plate maps. This repository provides the **Python client** (`pepkio-serial-dilution-planner`) that calls the same calculation engine through the Pepkio Tools REST API, so you can generate protocols from scripts, Jupyter notebooks, or automated pipelines.

If you prefer a graphical interface, use the hosted tool at [https://www.pepkio.com/tools/serial-dilution-planner](https://www.pepkio.com/tools/serial-dilution-planner). If you need reproducible, programmatic access, install the package from [PyPI](https://pypi.org/project/pepkio-serial-dilution-planner/) and follow the Quick Start below.

# Features

## Dilution planning (API-backed)

- **Concentration units:** molar (`M`, `mM`, `uM`, `nM`), mass per volume (`mg_per_mL`, `ug_per_uL`, `ng_per_uL`), and `percent`
- **Pipette-aware volumes:** define available pipettes (`id`, `min_ul`, `max_ul`, `resolution_ul`); receive rounded `transfer_ul` and recommended `pipette_label` per step
- **Step-by-step protocol:** concentration display, transfer volume, diluent volume, and warnings per step
- **Warnings:** flags transfers below a pipette minimum; automatic expansion of step count when a single-step dilution would exceed roughly 1000×
- **Economy mode:** reduce total reagent use while keeping transfers within pipette limits
- **Mass–molar conversion:** `molecular_weight_g_per_mol` when mixing mass/volume stock with molar targets (for example antibody mg/mL to nM working concentration)
- **Plate maps:** optional `plate_map` for 96- or 384-well layout with orientation and replicates
- **Shareable runs:** each API run returns a `permalink` that restores the exact plan

## Python package

- Fetch the tool manifest and list named examples (`get_manifest`, `list_examples`, `get_example_input`)
- Run planning synchronously (`run`) with custom JSON or manifest examples
- Poll runs for async tools (`get_run`, `wait_for_run`)
- CLI for manifest inspection and one-off runs (`pepkio-serial-dilution-planner`)
- Configurable API base URL and API keys via environment variables

# Common Use Cases

### Four-step mM to µM series (`standard_4step`)

Prepare a four-step serial dilution from 10 mM stock to 10 µM final concentration with 100 µL per tube—typical for small-molecule dose–response setup or qPCR template dilution before standard curve validation.

### Limited reagent with small pipettes (`economy_small_pipette`)

Use economy mode with P2 and P10 pipettes when sample volume is scarce and you want the planner to minimize per-tube volume while still producing pipettable transfers.

### 384-well plate layout (`plate_map_384`)

Map the dilution series onto a 384-well plate with column orientation for high-throughput screening or multiplex assay setup.

### Antibody dilution by mass (`antibody_mass`)

Start from mg/mL stock, target a molar working concentration, and supply molecular weight so the engine converts between mass and molar units consistently.

### Very large concentration span (`extreme_ratio_split`)

When stock and target concentrations differ by many orders of magnitude, the tool can add steps so no single transfer requires an impractical dilution factor.

# Why This Tool Exists

Spreadsheets and single-step dilution calculators often output exact microliter values that do not match pipette increments. Rounding by hand at the bench changes the effective dilution factor and can shift standard curve or dose–response results.

Manual plate mapping and protocol sharing add separate spreadsheets or notes that are easy to misalign with the volumes actually pipetted.

The Pepkio Serial Dilution Planner computes pipette-rounded transfer volumes, optional 96/384-well plate mapping, warnings for out-of-range transfers, and economy mode when reagent volume is limited. Shareable permalinks record the parameters used for a given plan. The Python package in this repository calls the same API for scripted or automated workflows.

# Installation

Install from PyPI:

```bash
pip install pepkio-serial-dilution-planner
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add pepkio-serial-dilution-planner
```

PyPI package: [https://pypi.org/project/pepkio-serial-dilution-planner/](https://pypi.org/project/pepkio-serial-dilution-planner/)

## API key

Programmatic runs require a Pepkio API key with **tools:run** scope. Create one at [https://www.pepkio.com/account/api-keys](https://www.pepkio.com/account/api-keys).

```bash
export PEPKIO_API_KEY="your-key"
```

| Variable | Description |
|----------|-------------|
| `PEPKIO_API_KEY` | Production (or default) API key |
| `LOCAL_PEPKIO_API_KEY` | Local dev key when base URL points to `tools.localtest.me` |
| `PEPKIO_API_BASE_URL` | Override API host (default: `https://tools.pepkio.com`) |
| `PEPKIO_SSL_VERIFY` | Set to `0` or `false` to disable TLS verify (local dev disables verify for `localtest.me` by default) |

Local development against a staging stack:

```bash
export PEPKIO_API_BASE_URL=https://tools.localtest.me
export PEPKIO_API_KEY="$LOCAL_PEPKIO_API_KEY"
```

Web UI (local): [https://www.localtest.me/tools/serial-dilution-planner](https://www.localtest.me/tools/serial-dilution-planner)

# Quick Start

Manifest inspection does **not** require an API key. Running the tool does.

### Python: manifest example

```python
from pepkio_serial_dilution_planner import PepkioClient

with PepkioClient() as client:
    inp = client.get_example_input("standard_4step")
    result = client.run(inp)
    print(result.status, result.permalink)
    print(result.result["summary"])
    for step in result.result["steps"]:
        print(step["step"], step["concentration_display"], step["transfer_ul"], step["pipette_label"])
```

### Python: custom input with pipettes

```python
from pepkio_serial_dilution_planner import PepkioClient

inp = {
    "stock_concentration": 10,
    "stock_unit": "mM",
    "target_concentration": 10,
    "target_unit": "uM",
    "num_steps": 4,
    "final_volume_ul": 100,
    "economy_mode": False,
    "pipettes": [
        {"id": "P20", "label": "P20", "min_ul": 2, "max_ul": 20, "resolution_ul": 1},
        {"id": "P200", "label": "P200", "min_ul": 20, "max_ul": 200, "resolution_ul": 1},
    ],
}

with PepkioClient() as client:
    result = client.run(inp)
    assert result.status == "completed"
```

### Python: 384-well plate map

```python
from pepkio_serial_dilution_planner import PepkioClient

with PepkioClient() as client:
    inp = client.get_example_input("plate_map_384")
    result = client.run(inp)
    plate = result.result.get("plate_map")
    print(plate["format"])  # "384"
```

### CLI

```bash
# Manifest (no API key)
pepkio-serial-dilution-planner manifest
pepkio-serial-dilution-planner manifest --examples

# Run a named example (API key required)
pepkio-serial-dilution-planner run --example standard_4step

# Run custom JSON input
pepkio-serial-dilution-planner run --input-json '{"stock_concentration":10,"stock_unit":"mM","target_concentration":10,"target_unit":"uM","num_steps":4,"final_volume_ul":100}'
```

Options: `--api-key`, `--base-url`, `--label`, `--idempotency-key`.

# Example Output

A completed run for the `standard_4step` manifest example (10 mM → 10 µM, four steps, 100 µL per tube) returns a structure similar to:

```json
{
  "run_id": "b3e5dd40-7218-4032-8065-6954322a6005",
  "status": "completed",
  "permalink": "https://tools.pepkio.com/r/b3e5dd40-7218-4032-8065-6954322a6005",
  "result": {
    "steps": [
      {
        "step": 1,
        "concentration_display": "1.778 mM",
        "transfer_ul": 18,
        "diluent_ul": 82,
        "pipette_label": "P20",
        "warnings": []
      },
      {
        "step": 2,
        "concentration_display": "316.2 µM",
        "transfer_ul": 18,
        "diluent_ul": 82,
        "pipette_label": "P20",
        "warnings": []
      },
      {
        "step": 3,
        "concentration_display": "56.23 µM",
        "transfer_ul": 18,
        "diluent_ul": 82,
        "pipette_label": "P20",
        "warnings": []
      },
      {
        "step": 4,
        "concentration_display": "10.00 µM",
        "transfer_ul": 18,
        "diluent_ul": 82,
        "pipette_label": "P20",
        "warnings": []
      }
    ],
    "summary": {
      "step_count": 4,
      "total_volume_ul": 400,
      "warning_count": 0
    },
    "notes": []
  }
}
```

The `permalink` field links to a saved run that colleagues can open in the browser to review the same parameters and protocol.

# Scientific Background

## Single dilution and C1V1 = C2V2

For a single dilution, mass of solute is conserved:

**C₁V₁ = C₂V₂**

where C is concentration and V is volume. If you know any three of initial concentration, final concentration, initial volume, and final volume, you can solve for the fourth. This relation applies to one mixing step, not an entire multi-tube serial series without accounting for each transfer.

## Dilution factor

In a **constant-ratio serial dilution**, each step uses the same dilution factor DF (often 10 for a “10-fold serial dilution”):

**DF = Cᵢ / Cᵢ₊₁**

After n identical serial steps from initial concentration C₀:

**Cₙ = C₀ / DFⁿ**

The total fold-change from stock to final tube is DFⁿ. For a 1000× total dilution with DF = 10 per step, you need n = 3 serial transfers (10³ = 1000).

## Why use multiple serial steps?

When the required total dilution is large, a single step may need a transfer volume that is below the pipette minimum or above its maximum. Splitting into serial steps keeps each transfer within pipette range and improves mixing at each concentration. The Pepkio planner can increase the number of steps automatically when a per-step dilution would exceed roughly 1000×.

## Standard curves

ELISA, qPCR, and many binding assays use a **standard curve**: a set of known concentrations (often log-spaced) used to interpolate unknown sample values. Serial dilution from a concentrated stock is the usual way to produce those standards. Log spacing of concentrations is equivalent to a constant dilution factor between adjacent standards.

## Molar and mass units

Molar concentration (mol/L) relates to mass concentration through the compound’s molar mass Mᵣ (g/mol):

**C_molar = C_mass / Mᵣ**

(with consistent units). When stock is in mg/mL and targets are in molar units, provide `molecular_weight_g_per_mol` so the planner converts consistently.

## Pipette resolution

Pipettes deliver discrete increments (for example 1 µL on a P200). Protocols should use rounded volumes that match the pipette you will use; otherwise the achieved concentration differs from the calculated ideal value.

# Frequently Asked Questions

### What is serial dilution?

Serial dilution is a method where each step dilutes the previous solution into fresh solvent, producing a geometric (constant-ratio) decrease in concentration across tubes or wells. It is widely used when you need many concentrations spanning orders of magnitude from one stock.

### How do I calculate dilution factor?

For one serial step, dilution factor DF = C_before / C_after. For constant-ratio series, DF is the same at every step. Total fold-change after n steps is DFⁿ. Example: 10 mM to 10 µM is a 1000× total change; with DF = 10 per step, three serial steps achieve 10³ = 1000×.

### What is C1V1 = C2V2?

It is the conservation-of-mass equation for a single dilution: initial concentration × initial volume = final concentration × final volume. Use it to compute how much stock to add to a known diluent volume, or what final concentration results from a chosen transfer volume.

### How do I prepare a standard curve?

Start from a concentrated stock at a known concentration. Choose the number of standards, final volume per tube, and desired highest and lowest concentrations. A serial dilution with constant dilution factor yields evenly spaced points on a log concentration axis—standard for ELISA and qPCR standard curves. The [Pepkio Serial Dilution Planner](https://www.pepkio.com/tools/serial-dilution-planner) prints a pipette-ready table you can follow at the bench.

### How do I design a dilution series for qPCR?

Dilute purified template or plasmid across a range that brackets expected sample Ct values (often spanning 10⁶–10¹ copies or equivalent). Use consistent final volume per tube, document dilution factor, and avoid inhibitors from over-concentrated stock. Pipette-rounded volumes reduce pipetting error that widens qPCR replicate spread.

### How do I dilute antibody from mg/mL to a working concentration?

Convert between mass and molar units using the antibody’s molecular weight. Enter stock in mg/mL, target in nM or µM, and supply `molecular_weight_g_per_mol` in the planner or API. The `antibody_mass` manifest example illustrates this workflow.

### How do I map a dilution series to a 96-well or 384-well plate?

Enable plate map generation in the web tool or pass a `plate_map` object in the API (`format`: `96` or `384`, plus orientation and replicates). The output assigns dilution steps to well addresses for plate setup and export (CSV or PNG in the web UI).

### Why are my calculated volumes not pipettable?

Ideal arithmetic volumes (for example 18.37 µL) may not match pipette increments or range. Pepkio rounds to your declared pipettes and warns when a volume is below the pipette minimum.

### What units does Pepkio Serial Dilution Planner support?

Molar: `M`, `mM`, `uM`, `nM`. Mass per volume: `mg_per_mL`, `ug_per_uL`, `ng_per_uL`. Also `percent`. Mixed molar and mass inputs require molecular weight.

### What is economy mode?

Economy mode minimizes reagent use per tube while keeping transfers at or above the smallest enabled pipette minimum, after rounding. It helps when sample or compound is limited.

### Does the tool add extra dilution steps automatically?

Yes. If the concentration ratio requested for a single step would exceed roughly 1000×, the planner can increase `num_steps` so each transfer remains practical for pipetting and mixing.

### Do I need an API key for the Python client?

No key is required for `get_manifest()` or the CLI `manifest` command. `run()` and the CLI `run` command require an API key with tools:run scope.

### Can I run the tool offline?

The Python package calls the hosted Pepkio Tools API; an internet connection and valid API key are required for runs. Calculations are not bundled for fully offline use in this package.

### How do I share a dilution protocol with a colleague?

Open the web tool and use the shareable link feature, or share the `permalink` returned from an API run. The link restores the same stock, target, steps, pipettes, and plate settings.

### What is the difference between serial dilution and doubling dilution?

Serial dilution usually means a fixed dilution factor between steps (for example 10-fold or 3.16-fold for half-log spacing). Doubling dilution means each step is half the previous concentration (2-fold dilution per step). Both are geometric series; only the dilution factor differs.

### What are common mistakes in serial dilution?

Mixing up transfer volume and total tube volume; using uncorrected spreadsheet µL values; changing pipettes mid-series without updating the plan; skipping mixing between steps; and contaminating stock when returning pipette tips to the stock tube. Following a printed step table with check-off bench mode reduces execution errors.

### How many steps do I need for a 1000× dilution?

With a 10-fold dilution per step, three serial steps give 1000× total (10³). With a 3.16-fold step (~half-log), you need more steps for the same total span. The planner chooses step volumes and can adjust step count when ratios are extreme.

### Is this the same as a dilution calculator?

A basic dilution calculator typically solves C1V1 = C2V2 for one step. Pepkio Serial Dilution Planner plans multi-step serial series with pipette constraints, optional plate maps, and saved run links.

# Web Application

For interactive planning without writing code, use the hosted Pepkio Serial Dilution Planner.

The web interface accepts stock and target concentrations in supported units, available pipettes, and step count. It returns a step-by-step table with concentration at each step, transfer volume rounded to pipette resolution, recommended pipette, and diluent volume. It warns when transfers are below pipette minimums and can add steps when a single dilution would exceed roughly 1000×.

The web UI also supports:

- **Bench mode** — large, check-off steps for use at the hood
- **Economy mode** — reduced reagent volume when samples are limited
- **96/384-well plate maps** — well assignment with CSV or PNG export
- **Copy and print** — protocol table and worksheet for the lab notebook
- **Shareable link** — restores the exact plan for collaborators

**Web Application:** [https://www.pepkio.com/tools/serial-dilution-planner](https://www.pepkio.com/tools/serial-dilution-planner)

# Related Resources

- **GitHub Repository:** [https://github.com/pepkio/pepkio-serial-dilution-planner](https://github.com/pepkio/pepkio-serial-dilution-planner)
- **PyPI Package:** [https://pypi.org/project/pepkio-serial-dilution-planner/](https://pypi.org/project/pepkio-serial-dilution-planner/)
- **Web Application:** [https://www.pepkio.com/tools/serial-dilution-planner](https://www.pepkio.com/tools/serial-dilution-planner)

# About Pepkio

[Pepkio](https://www.pepkio.com) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (RNA-seq, single-cell RNA-seq, spatial transcriptomics, functional enrichment, and custom workflows).

# Citation

If you use Pepkio Serial Dilution Planner in a publication or protocol, cite the web tool and optionally the Python package version:

```bibtex
@misc{pepkio_serial_dilution_planner,
  title        = {Pepkio Serial Dilution Planner},
  author       = {Pepkio},
  year         = {2026},
  howpublished = {\url{https://www.pepkio.com/tools/serial-dilution-planner}},
  note         = {Python client: pepkio-serial-dilution-planner on PyPI}
}
```

# License

See the [GitHub repository](https://github.com/pepkio/pepkio-serial-dilution-planner) for license terms.

# Keywords

serial dilution, serial dilution calculator, serial dilution planner, dilution factor, dilution series, logarithmic dilution, geometric dilution, C1V1=C2V2, concentration dilution, mM to uM dilution, micromolar dilution, standard curve preparation, ELISA standard curve, qPCR dilution, qPCR standard curve, dose response dilution, IC50 dilution series, antibody dilution, protein dilution, pipette volume calculator, pipette-aware dilution, transfer volume, diluent volume, 96-well plate map, 384-well plate map, microplate dilution layout, laboratory dilution protocol, bench protocol, serial dilution protocol, ten-fold serial dilution, half-log dilution, stock solution dilution, working solution preparation, molecular biology calculator, Pepkio, pepkio-serial-dilution-planner, Python dilution API, lab automation dilution, reagent sparing dilution, economy mode dilution, mass to molar conversion, mg/mL to uM, pipette rounding, dilution warning, high-throughput dilution plate

how to perform a serial dilution in the lab, how to calculate serial dilution step volumes, serial dilution from mM to uM calculator, how many steps for 1000 fold dilution, how to make a 10-fold serial dilution, how to prepare ELISA standard curve by serial dilution, qPCR template serial dilution protocol, how to map serial dilution to 96 well plate, 384 well serial dilution layout, pipette volume too small for serial dilution, round microliter volumes to P20 pipette, C1V1 C2V2 dilution calculator explained, what is dilution factor in serial dilution, difference between serial and simple dilution, antibody serial dilution from mg/mL, convert mg per mL to micromolar for dilution, standard curve log spacing dilution factor, serial dilution mistakes to avoid, shareable lab protocol link dilution, printable serial dilution worksheet, minimize reagent use serial dilution, auto expand dilution steps large concentration range, Python script serial dilution protocol, API for laboratory dilution planning, Pepkio serial dilution planner, serial dilution for inhibitor titration, protein standard serial dilution BSA, immunoassay dilution series planning, dose response serial dilution 96 well, how to dilute stock for standard curve qPCR, serial dilution bench checklist, export plate map CSV serial dilution

# Contributing

Clone [https://github.com/pepkio/pepkio-serial-dilution-planner](https://github.com/pepkio/pepkio-serial-dilution-planner), run `uv sync`, and execute `uv run pytest` for unit and integration tests. Integration tests require `PEPKIO_API_KEY` or `LOCAL_PEPKIO_API_KEY` in the environment.
