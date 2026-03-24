set windows-powershell := true
venv_dir := ".venv"
venv     := if os() == "windows" { venv_dir / "Scripts/python" } else { venv_dir / "bin/python" }
pip      := if os() == "windows" { venv_dir / "Scripts/pip" } else { venv_dir / "bin/pip" }
python   := if os() == "windows" { "python" } else { "python3" }
interpreter := venv_dir + "/bin/python"

[group('exec')]
export_pdf:
    asciidoctor-pdf ./docs/thesis.adoc

[group('exec')]
run:
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
[windows]
setup:
    python -m venv {{venv_dir}}
    {{venv_dir}}\Scripts\python.exe -m pip install --upgrade pip
    {{venv_dir}}\Scripts\python.exe -m pip install -r requirements.txt

[group('venv')]
[unix]
clean:
    rm -rf {{venv_dir}}
    find . -type d -name "__pycache__" -exec rm -rf {} +
    @echo "Environment cleaned."

[group('venv')]
[windows]
clean:
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue {{venv_dir}}
    Get-ChildItem -Recurse -Filter __pycache__ -Directory | Remove-Item -Recurse -Force
    Write-Host "Environment cleaned."