# Angl Assembly Picnic

A tiny public-safe prototype of an Angl chapter paired with a real ARM64
assembly implementation that powers a browser UI.

Important: this repo is not yet proof that the current Angl compiler can
generate ARM64 assembly. The assembly file is checked in as the implementation
shape Angl should eventually generate. The real compiler backend still needs to
be built before this should be described as "Angl generated assembly."

The source of truth is:

```text
specs/optimize_picnic_basket.angl
```

The generated implementation is:

```text
generated/picnic_kernel.s
```

The boring host adapter is:

```text
app/picnic_adapter.py
```

## Run

Requires macOS or another ARM64 environment with `clang`.

```bash
make test
make run
```

Open:

```text
http://127.0.0.1:8789
```

## What This Proves

- The `.angl` file reads like a chapter.
- The contract examples are black-box tests.
- The runtime implementation is real ARM64 assembly.
- The UI is normal app code.
- No local infrastructure, IP addresses, or model endpoints are committed.

This is intentionally small: the point is to make the source/build split
visible, not to claim a finished assembly compiler backend.
