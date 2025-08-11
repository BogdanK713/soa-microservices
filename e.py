import os

root_dir = os.path.abspath(os.path.dirname(__file__))
output_file = "project_dump.txt"

# FOLDERE koje preskačemo (binarni / generirani)
skip_dirs = {
    "node_modules", "__pycache__", ".git", ".idea", ".vscode",
    "dist", "build", ".pytest_cache", ".coverage", ".DS_Store"
}

# Tekstualne EKSTENZIJE koje uključujemo
text_extensions = {
    ".js", ".ts", ".tsx", ".mjs", ".cjs",
    ".py",
    ".json",
    ".yml", ".yaml",
    ".txt", ".md",
    ".html", ".css",
    ".env", ".env.example",
    ".sql",
    ".sh", ".bash",
    ".ini", ".conf",
    ".dockerignore", ".gitattributes", ".gitkeep",
}

# TAČNA IMENA fajlova koji često nemaju ekstenziju
exact_filenames = {
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    ".gitignore",
    ".dockerignore",
    ".editorconfig",
    "Procfile",
}

def is_text_file(filename: str) -> bool:
    name = os.path.basename(filename)
    if name in exact_filenames:
        return True
    _, ext = os.path.splitext(name)
    return ext in text_extensions

with open(output_file, "w", encoding="utf-8") as out:
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # filtriraj foldere
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]

        # sortiraj za stabilan izlaz
        dirnames.sort()
        filenames.sort()

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            # preskoči sam output fajl
            if os.path.abspath(file_path) == os.path.abspath(os.path.join(root_dir, output_file)):
                continue

            # uključi samo relevantne tekstualne fajlove
            if not is_text_file(filename):
                continue

            rel_path = os.path.relpath(file_path, root_dir)

            out.write(f"\n{'='*80}\n")
            out.write(f"FILE: {rel_path}\n")
            out.write(f"{'='*80}\n\n")

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    out.write(f.read())
            except Exception as e:
                out.write(f"[Greška pri čitanju fajla: {e}]\n")

print(f"Svi fajlovi i putanje su sačuvani u: {output_file}")
