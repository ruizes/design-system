#!/usr/bin/env python3
import json
import os

# Define all files to serialize with their source and target paths
files_to_serialize = [
    {
        "header": "index.html",
        "source": "/Users/tal/Downloads/testbed 45/json-viewer/design-system/index.html",
        "target": "/testbed/project-folder/index.html"
    },
    {
        "header": "package.json",
        "source": "/Users/tal/Downloads/testbed 45/json-viewer/design-system/package.json",
        "target": "/testbed/project-folder/package.json"
    },
    {
        "header": "vite.config.js",
        "source": "/Users/tal/Downloads/testbed 45/json-viewer/design-system/vite.config.js",
        "target": "/testbed/project-folder/vite.config.js"
    },
    {
        "header": "playwright.config.js",
        "source": "/Users/tal/Downloads/testbed 45/json-viewer/design-system/playwright.config.js",
        "target": "/testbed/project-folder/playwright.config.js"
    },
    {
        "header": "src/main.js",
        "source": "/Users/tal/Downloads/testbed 45/json-viewer/design-system/src/main.js",
        "target": "/testbed/project-folder/src/main.js"
    },
    {
        "header": "src/App.vue",
        "source": "/Users/tal/Downloads/testbed 45/json-viewer/design-system/src/App.vue",
        "target": "/testbed/project-folder/src/App.vue"
    },
    {
        "header": "src/styles/main.css",
        "source": "/Users/tal/Downloads/testbed 45/json-viewer/design-system/src/styles/main.css",
        "target": "/testbed/project-folder/src/styles/main.css"
    },
    {
        "header": "src/pages/Home.vue",
        "source": "/Users/tal/Downloads/testbed 45/json-viewer/design-system/src/pages/Home.vue",
        "target": "/testbed/project-folder/src/pages/Home.vue"
    },
    {
        "header": "src/pages/Components.vue",
        "source": "/Users/tal/Downloads/testbed 45/json-viewer/design-system/src/pages/Components.vue",
        "target": "/testbed/project-folder/src/pages/Components.vue"
    },
    {
        "header": "src/pages/Products.vue",
        "source": "/Users/tal/Downloads/testbed 45/json-viewer/design-system/src/pages/Products.vue",
        "target": "/testbed/project-folder/src/pages/Products.vue"
    },
    {
        "header": "src/pages/About.vue",
        "source": "/Users/tal/Downloads/testbed 45/json-viewer/design-system/src/pages/About.vue",
        "target": "/testbed/project-folder/src/pages/About.vue"
    },
    {
        "header": "tests/project-folder.spec.js",
        "source": "/Users/tal/Downloads/testbed 45/json-viewer/design-system/tests/design-system.spec.js",
        "target": "/testbed/project-folder/tests/app.spec.js"
    }
]

# Build the output content
output_sections = []

for file_info in files_to_serialize:
    source_path = file_info["source"]
    
    if os.path.exists(source_path):
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Special handling for package.json to update the name
        if file_info["header"] == "package.json":
            try:
                pkg_data = json.loads(content)
                pkg_data["name"] = "project-folder"
                content = json.dumps(pkg_data, indent=4)
            except:
                pass
        
        file_data = {
            "content": content,
            "file_path": file_info["target"]
        }
        
        # Format as: header\n{json}\n
        json_str = json.dumps(file_data, ensure_ascii=False, indent=2)
        section = f"{file_info['header']}\n{json_str}"
        output_sections.append(section)
        print(f"Serialized: {file_info['header']}")
    else:
        print(f"Warning: File not found: {source_path}")

# Write to output file
output_file = "/Users/tal/Downloads/testbed 45/json-viewer/design-system/serialized_files.json"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(output_sections))

print(f"\nSuccessfully regenerated serialized_files.json with {len(output_sections)} files")
