# HEARTBEAT

HEARTBEAT is a Python project for checking configured web services. It reads a
JSON list of services, makes one HTTP check per valid entry, and reports what
each request observed.

## Run HEARTBEAT

Use Python 3.10 or newer. From the project root, create your local configuration
from the starter example:

```bash
cp services.example.json services.json
```

Edit `services.json` to set the names and URLs you want to check, then run:

```bash
python3 -m src.cli services.json
```

You can also inspect `services.lsu.example.json` for an LSU-focused example.
Your local `services.json` is ignored by Git.

`CHECK PASSED` means HEARTBEAT received a 2xx HTTP response. `NEEDS REVIEW`
means the request did not; it does not prove the service is unavailable to
users. A 403 means the request was refused. If no HTTP response arrived,
HEARTBEAT prints a short failure reason.

The command exits with:

- `0` when all configuration entries are valid and all checks pass.
- `1` when an entry is invalid or a check needs review.
- `2` when the configuration file cannot be read or parsed.

## Run tests

From the project root:

```bash
python3 -m unittest discover -s tests -v
```

## Current scope

Each run performs one check per valid service. Results are printed to the
terminal; check history and stable Service IDs across separate runs are not
saved yet.