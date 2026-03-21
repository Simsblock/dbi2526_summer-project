#[Windows]
#set shell := ["cmd", "/c"]
venv_dir := ".venv"
venv := if os() == "windows" { venv_dir / "Scripts/python" } else { venv_dir / "bin/python" }
python := "python3"
pip := venv_dir + "/bin/pip"
interpreter := venv_dir + "/bin/python"

export_pdf:
    asciidoctor-pdf ./docs/thesis.adoc

run-transform:
    {{venv}} src/main.py

[group('venv')]
[linux]
setup:
    @echo "Creating virtual environment in {{venv_dir}}..."
    {{python}} -m venv {{venv_dir}}
    @echo "Installing dependencies..."
    {{pip}} install --upgrade pip
    {{pip}} install -r requirements.txt
    @echo "Setup complete."

[group('venv')]
[linux]
run:
    @if [ ! -d "{{venv_dir}}" ]; then \
        echo "Venv not found. Running setup first..."; \
        just setup; \
    fi
    {{interpreter}} src/main.py

[group('venv')]
[windows]
setup:
    python -m venv {{venv_dir}}
    {{venv_dir}}\Scripts\pip install --upgrade pip
    {{venv_dir}}\Scripts\pip install -r requirements.txt

[group('venv')]
[windows]
run:
    {{venv_dir}}\Scripts\python src/main.py

[group('venv')]
clean:
    rm -rf {{venv_dir}}
    rm -rf src/__pycache__
    find . -type d -name "__pycache__" -exec rm -rf {} +
    @echo "Environment cleaned."