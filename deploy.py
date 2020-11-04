import os
import subprocess
import time
import sys

CURRENT_DIRECTORY = os.getcwd()
ANGULAR_DIRECTORY = "dashboard-frontend"
FLASK_APP_DIRECTORY = os.path.join("dashboard-backend", "app")
ANGULAR_PROJECT_PATH = os.path.join(CURRENT_DIRECTORY, ANGULAR_DIRECTORY)

# Compiled Angular files
DIST_PATH = os.path.join(ANGULAR_PROJECT_PATH, "dist", ANGULAR_DIRECTORY)

# Copy Angular files in these
FLASK_STATIC_PATH = os.path.join(CURRENT_DIRECTORY, FLASK_APP_DIRECTORY, "static")
FLASK_TEMPLATES_PATH = os.path.join(CURRENT_DIRECTORY, FLASK_APP_DIRECTORY, "templates")

if sys.argv[1] == "dev":
    # Build Angular project for development
    subprocess.call(
        (f"cd {ANGULAR_PROJECT_PATH} && ng build --base-href /static/"), shell=True
    )
elif sys.argv[1] == "prod":
    # Build Angular project for production
    subprocess.call(
        (f"cd {ANGULAR_PROJECT_PATH} && ng build --prod --base-href /static/"),
        shell=True,
    )

compiled_files = os.listdir(DIST_PATH)
static_files = ""
html_files = ""
assets_directory = ""
for file in compiled_files:
    if "assets" in file:
        assets_directory += file
    if ".html" not in file and "assets" not in file:
        static_files += file + " "
    if ".html" in file:
        html_files += file + " "

# Delete exitsing files in static and templates
subprocess.call(
    (f"del /S /Q {FLASK_STATIC_PATH} && del /S /Q {FLASK_TEMPLATES_PATH}"), shell=True
)

# Copy static files to /static
subprocess.call(
    (f"cd {DIST_PATH} && for %I in ({static_files}) do copy %I {FLASK_STATIC_PATH}"), shell=True
)
print("Copied static files")

# Copy assets folder to /static/assets
subprocess.call(
    (f"cd {DIST_PATH} && Xcopy /E /I {assets_directory} {os.path.join(FLASK_STATIC_PATH, 'assets')}"), shell=True
)
print("Copied assets folder")

# Copy template files to /templates
subprocess.call(
    (f"cd {DIST_PATH} && copy {html_files} {FLASK_TEMPLATES_PATH}"), shell=True
)
print("Copied template files")

# Create requirements.txt
subprocess.call("pip freeze > requirements.txt", shell=True)
print("Created requirements.txt")

print(f"Build complete.")
