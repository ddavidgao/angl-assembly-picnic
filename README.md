# Angl Assembly Picnic

A tiny public-safe demo of an Angl chapter compiling to a real ARM64 assembly
implementation that powers a browser UI.

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
visible, not to build a full Angl compiler backend in this demo repo.
