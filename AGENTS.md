# Repository Guidelines

## Project Structure & Module Organization
The root `Dockerfile` builds the `andgineer/allure` image and defines the pinned Allure release, Java runtime, and supporting Python utilities. Keep sample result assets under `allure-results/`; generated HTML belongs in `allure-report/` and can be cleared safely. Document usage updates in `README.md` and agent-specific context in `CLAUDE.md` whenever behaviour or dependencies change.

## Build, Test, and Development Commands
Use the Docker CLI for build and smoke-test workflows. Build the image locally with:
```bash
docker build -t andgineer/allure .
```
Regenerate a report from the provided fixtures by mounting results and reports:
```bash
docker run --rm -v ${PWD}/allure-results:/allure-results -v ${PWD}/allure-report:/allure-report andgineer/allure allure generate /allure-results -o /allure-report --clean
```
Verify the container serves output correctly:
```bash
docker run --rm -p 8800:80 -v ${PWD}/allure-results:/allure-results andgineer/allure allure serve -h 0.0.0.0 -p 80 /allure-results
```

## Coding Style & Naming Conventions
Keep Dockerfile instructions ordered: package installation, environment setup, runtime defaults. Use lowercase, dash-separated filenames for helper scripts and reserve uppercase snake case for environment variables such as `ALLURE_VERSION`. Shell snippets should be POSIX-compatible and linted with `shellcheck` when practical. Avoid trailing whitespace and prefer two-space indentation in YAML or Compose examples.

## Testing Guidelines
No automated tests run in CI; rely on functional checks. After modifying the Dockerfile or dependencies, rebuild the image and rerun the `allure generate` and `allure serve` commands with the bundled fixtures to confirm Java, Python, and Allure executables resolve correctly. Capture any non-zero exit codes or warnings in the PR description.

## Commit & Pull Request Guidelines
Follow the existing history: short, imperative commit subjects (e.g., `upgrade allure runtime`). Group related changes per commit and avoid WIP messages. PRs should explain the motivation, outline test evidence, and link issues when applicable; attach screenshots of the generated report UI if output changes.

## Security & Configuration Tips
Respect the pinned Maven URL and `ALLURE_VERSION`; bump both together and describe the reason in the PR. Do not add secrets to the image—prefer runtime environment variables or mounted credentials. Review base image CVEs before release by running `docker scout cves andgineer/allure`.
