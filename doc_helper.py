#!/usr/bin/env python3
"""
Documentation Helper Tool
Automates common documentation tasks for the Clinical Supervision Chatbot project.

Usage:
    python doc_helper.py validate              # Validate documentation consistency
    python doc_helper.py generate-api          # Generate API docs from code
    python doc_helper.py add-topic "name"      # Create new knowledge topic with template
    python doc_helper.py add-endpoint "name"   # Create new API endpoint docs
    python doc_helper.py check-coverage        # Check documentation coverage
    python doc_helper.py changelog             # Generate changelog entry
    python doc_helper.py --help                # Show help
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple


class DocumentationHelper:
    """Helper class for documentation tasks"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.backend_file = self.project_root / "chatbot_backend.py"
        self.frontend_file = self.project_root / "chatbot.html"
        self.readme = self.project_root / "README.md"
        self.docs_dir = self.project_root / "docs"

    def validate_documentation(self) -> bool:
        """Validate that documentation is consistent with code"""
        print("🔍 Validating documentation...")
        issues = []

        # Check if key files exist
        if not self.backend_file.exists():
            issues.append("❌ Backend file not found: chatbot_backend.py")

        if not self.readme.exists():
            issues.append("❌ README.md not found")

        # Validate knowledge base consistency
        backend_topics = self._extract_knowledge_topics_backend()
        frontend_topics = self._extract_knowledge_topics_frontend()

        if backend_topics != frontend_topics:
            issues.append("⚠️  Knowledge base topics differ between backend and frontend")
            missing_in_frontend = backend_topics - frontend_topics
            missing_in_backend = frontend_topics - backend_topics

            if missing_in_frontend:
                issues.append(f"   - Missing in frontend: {missing_in_frontend}")
            if missing_in_backend:
                issues.append(f"   - Missing in backend: {missing_in_backend}")

        # Check for broken links in README
        broken_links = self._check_broken_links()
        if broken_links:
            issues.append("⚠️  Potential broken links found:")
            for link in broken_links:
                issues.append(f"   - {link}")

        # Check if API endpoints are documented
        endpoints = self._extract_api_endpoints()
        documented_endpoints = self._extract_documented_endpoints()

        undocumented = set(endpoints) - set(documented_endpoints)
        if undocumented:
            issues.append("⚠️  Undocumented API endpoints:")
            for endpoint in undocumented:
                issues.append(f"   - {endpoint}")

        # Report results
        if issues:
            print("\n".join(issues))
            print(f"\n❌ Validation failed with {len(issues)} issue(s)")
            return False
        else:
            print("✅ All documentation checks passed!")
            return True

    def generate_api_docs(self) -> None:
        """Generate API documentation from code"""
        print("📝 Generating API documentation...")

        if not self.backend_file.exists():
            print("❌ Backend file not found")
            return

        endpoints = self._extract_api_endpoints_detailed()

        api_doc_path = self.docs_dir / "API.md"
        api_doc_path.parent.mkdir(parents=True, exist_ok=True)

        with open(api_doc_path, 'w') as f:
            f.write("# API Documentation\n\n")
            f.write("This document describes all available API endpoints for the Clinical Supervision Chatbot.\n\n")
            f.write("## Base URL\n\n")
            f.write("```\nhttp://localhost:5000\n```\n\n")
            f.write("## Endpoints\n\n")

            for endpoint in endpoints:
                f.write(f"### `{endpoint['method']} {endpoint['path']}`\n\n")
                f.write(f"{endpoint.get('description', 'No description available')}\n\n")

                if endpoint.get('example'):
                    f.write("**Example Request:**\n\n")
                    f.write("```bash\n")
                    f.write(endpoint['example'])
                    f.write("\n```\n\n")

                f.write("---\n\n")

        print(f"✅ API documentation generated: {api_doc_path}")

    def add_knowledge_topic(self, topic_name: str) -> None:
        """Create a new knowledge topic from template"""
        print(f"📚 Creating new knowledge topic: {topic_name}")

        template_path = self.docs_dir / "templates" / "knowledge_topic_template.md"
        if not template_path.exists():
            print("❌ Template not found")
            return

        # Create safe filename
        safe_name = re.sub(r'[^a-z0-9]+', '_', topic_name.lower())
        output_path = self.docs_dir / "topics" / f"{safe_name}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy template and customize
        with open(template_path, 'r') as f:
            content = f.read()

        content = content.replace("[Topic Name]", topic_name)
        content = content.replace("[topic_key]", safe_name)
        content = content.replace("[topic_name]", safe_name)
        content = content.replace("YYYY-MM-DD", datetime.now().strftime("%Y-%m-%d"))

        with open(output_path, 'w') as f:
            f.write(content)

        print(f"✅ Knowledge topic created: {output_path}")
        print(f"\n📋 Next steps:")
        print(f"   1. Edit {output_path} and fill in the template")
        print(f"   2. Add keywords and responses")
        print(f"   3. Update chatbot_backend.py with the new topic")
        print(f"   4. Update chatbot.html with the new topic")
        print(f"   5. Test the new topic")

    def add_api_endpoint(self, endpoint_name: str) -> None:
        """Create API endpoint documentation from template"""
        print(f"🔌 Creating API endpoint documentation: {endpoint_name}")

        template_path = self.docs_dir / "templates" / "api_endpoint_template.md"
        if not template_path.exists():
            print("❌ Template not found")
            return

        # Create safe filename
        safe_name = re.sub(r'[^a-z0-9]+', '_', endpoint_name.lower())
        output_path = self.docs_dir / "api" / f"{safe_name}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(template_path, 'r') as f:
            content = f.read()

        content = content.replace("[METHOD]", "POST")
        content = content.replace("[endpoint-path]", f"/{endpoint_name}")
        content = content.replace("YYYY-MM-DD", datetime.now().strftime("%Y-%m-%d"))

        with open(output_path, 'w') as f:
            f.write(content)

        print(f"✅ API endpoint documentation created: {output_path}")
        print(f"\n📋 Next steps:")
        print(f"   1. Edit {output_path} and customize for your endpoint")
        print(f"   2. Add to docs/API.md summary")

    def check_documentation_coverage(self) -> None:
        """Check what is documented vs what exists in code"""
        print("📊 Checking documentation coverage...\n")

        # Check knowledge topics
        backend_topics = self._extract_knowledge_topics_backend()
        print(f"✅ Knowledge Topics: {len(backend_topics)} found")
        for topic in sorted(backend_topics):
            print(f"   - {topic}")

        # Check API endpoints
        endpoints = self._extract_api_endpoints()
        print(f"\n✅ API Endpoints: {len(endpoints)} found")
        for endpoint in sorted(endpoints):
            print(f"   - {endpoint}")

        # Check documentation files
        doc_files = list(self.docs_dir.glob("**/*.md")) if self.docs_dir.exists() else []
        print(f"\n✅ Documentation Files: {len(doc_files)} found")
        for doc_file in sorted(doc_files):
            print(f"   - {doc_file.relative_to(self.project_root)}")

        print("\n📈 Coverage Summary:")
        print(f"   - Code files: 2 (backend, frontend)")
        print(f"   - Knowledge topics: {len(backend_topics)}")
        print(f"   - API endpoints: {len(endpoints)}")
        print(f"   - Documentation files: {len(doc_files)}")

    def generate_changelog_entry(self) -> None:
        """Generate a changelog entry template"""
        print("📋 Generating changelog entry...\n")

        changelog_path = self.docs_dir / "CHANGELOG.md"

        today = datetime.now().strftime("%Y-%m-%d")
        version = "X.Y.Z"  # User should replace this

        entry = f"""
## [{version}] - {today}

### Added
-

### Changed
-

### Fixed
-

### Removed
-

"""

        print("📝 Changelog entry template:")
        print(entry)

        if changelog_path.exists():
            print(f"💡 Append this to: {changelog_path}")
        else:
            changelog_path.parent.mkdir(parents=True, exist_ok=True)
            with open(changelog_path, 'w') as f:
                f.write("# Changelog\n\n")
                f.write("All notable changes to this project will be documented in this file.\n\n")
                f.write("The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),\n")
                f.write("and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n\n")
                f.write(entry)
            print(f"✅ Created new changelog: {changelog_path}")

    # Helper methods

    def _extract_knowledge_topics_backend(self) -> Set[str]:
        """Extract knowledge topics from backend code"""
        if not self.backend_file.exists():
            return set()

        with open(self.backend_file, 'r') as f:
            content = f.read()

        # Look for knowledge_base dictionary keys
        pattern = r'"([^"]+)":\s*{[^}]*"keywords":'
        matches = re.findall(pattern, content)
        return set(matches)

    def _extract_knowledge_topics_frontend(self) -> Set[str]:
        """Extract knowledge topics from frontend code"""
        if not self.frontend_file.exists():
            return set()

        with open(self.frontend_file, 'r') as f:
            content = f.read()

        # Look for knowledge_base dictionary keys in JavaScript
        pattern = r'([a-zA-Z_][a-zA-Z0-9_]*):\s*{[^}]*keywords:'
        matches = re.findall(pattern, content)
        return set(matches)

    def _extract_api_endpoints(self) -> List[str]:
        """Extract API endpoints from backend code"""
        if not self.backend_file.exists():
            return []

        with open(self.backend_file, 'r') as f:
            content = f.read()

        # Look for Flask route decorators
        pattern = r'@app\.route\([\'"]([^\'"]+)[\'"],[^)]*methods=\[[\'"]([^\'"]+)[\'"]\]'
        matches = re.findall(pattern, content)
        return [f"{method} {path}" for path, method in matches]

    def _extract_api_endpoints_detailed(self) -> List[Dict]:
        """Extract API endpoints with details from backend code"""
        if not self.backend_file.exists():
            return []

        with open(self.backend_file, 'r') as f:
            lines = f.readlines()

        endpoints = []
        for i, line in enumerate(lines):
            if '@app.route' in line:
                # Extract route details
                path_match = re.search(r'@app\.route\([\'"]([^\'"]+)[\'"]', line)
                method_match = re.search(r'methods=\[[\'"]([^\'"]+)[\'"\]', line)

                if path_match:
                    endpoint = {
                        'path': path_match.group(1),
                        'method': method_match.group(1) if method_match else 'GET'
                    }

                    # Try to get function docstring
                    if i + 1 < len(lines) and 'def ' in lines[i + 1]:
                        func_start = i + 1
                        if func_start + 1 < len(lines) and '"""' in lines[func_start + 1]:
                            docstring_lines = []
                            for j in range(func_start + 1, min(func_start + 10, len(lines))):
                                if '"""' in lines[j]:
                                    docstring_lines.append(lines[j].replace('"""', '').strip())
                                    if lines[j].count('"""') == 2 or j > func_start + 1:
                                        break
                                else:
                                    docstring_lines.append(lines[j].strip())
                            endpoint['description'] = ' '.join(docstring_lines)

                    # Generate example
                    endpoint['example'] = f"curl -X {endpoint['method']} http://localhost:5000{endpoint['path']}"

                    endpoints.append(endpoint)

        return endpoints

    def _extract_documented_endpoints(self) -> List[str]:
        """Extract documented endpoints from README"""
        if not self.readme.exists():
            return []

        with open(self.readme, 'r') as f:
            content = f.read()

        pattern = r'`(GET|POST|PUT|DELETE)\s+([^`]+)`'
        matches = re.findall(pattern, content)
        return [f"{method} {path}" for method, path in matches]

    def _check_broken_links(self) -> List[str]:
        """Check for broken internal links in README"""
        if not self.readme.exists():
            return []

        with open(self.readme, 'r') as f:
            content = f.read()

        # Find markdown links
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(pattern, content)

        broken = []
        for text, link in matches:
            # Only check internal file links
            if not link.startswith(('http://', 'https://', '#')):
                file_path = self.project_root / link
                if not file_path.exists():
                    broken.append(f"{text} -> {link}")

        return broken


def main():
    parser = argparse.ArgumentParser(
        description="Documentation Helper for Clinical Supervision Chatbot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        'command',
        choices=['validate', 'generate-api', 'add-topic', 'add-endpoint', 'check-coverage', 'changelog'],
        help='Command to execute'
    )

    parser.add_argument(
        'name',
        nargs='?',
        help='Name for add-topic or add-endpoint commands'
    )

    parser.add_argument(
        '--project-root',
        default='.',
        help='Project root directory (default: current directory)'
    )

    args = parser.parse_args()

    helper = DocumentationHelper(args.project_root)

    try:
        if args.command == 'validate':
            success = helper.validate_documentation()
            sys.exit(0 if success else 1)

        elif args.command == 'generate-api':
            helper.generate_api_docs()

        elif args.command == 'add-topic':
            if not args.name:
                print("❌ Error: Topic name required")
                print("Usage: python doc_helper.py add-topic \"Topic Name\"")
                sys.exit(1)
            helper.add_knowledge_topic(args.name)

        elif args.command == 'add-endpoint':
            if not args.name:
                print("❌ Error: Endpoint name required")
                print("Usage: python doc_helper.py add-endpoint \"endpoint-name\"")
                sys.exit(1)
            helper.add_api_endpoint(args.name)

        elif args.command == 'check-coverage':
            helper.check_documentation_coverage()

        elif args.command == 'changelog':
            helper.generate_changelog_entry()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
