#!/usr/bin/env python3
"""
AI Team Auto-Activator — v2.1.0
Automatically activates agents, analyzes workspace structure, and restores context.
"""

import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

# Ensure console supports UTF-8 for emoji characters on Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Ensure current script directory is in path for imports
sys.path.append(str(Path(__file__).parent))
from brain_manager import BrainManager


class AutoActivator:
    """Handles automatic activation sequence and context building on session start."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.brain_manager = BrainManager(self.project_root)

    def detect_project_type(self) -> dict:
        """Detect project type from files in the workspace."""
        indicators = {
            "frontend": [],
            "backend": [],
            "fullstack": [],
            "mobile": [],
            "data": []
        }

        checks = {
            "package.json": "frontend",
            "Cargo.toml": "backend",
            "requirements.txt": "backend",
            "go.mod": "backend",
            "pom.xml": "backend",
            "src/App.tsx": "frontend",
            "src/main.py": "backend",
            "App.tsx": "frontend",
            "main.go": "backend",
            "index.js": "frontend",
            "server.js": "backend",
            "app.js": "backend",
            "next.config.js": "fullstack",
            "nuxt.config.ts": "fullstack",
            "vite.config.ts": "frontend",
            "tailwind.config.js": "frontend",
            "docker-compose.yml": "fullstack",
            "Dockerfile": "fullstack"
        }

        detected = set()
        for filename, ptype in checks.items():
            if (self.project_root / filename).exists():
                detected.add(ptype)
                indicators[ptype].append(filename)

        return {
            "types": list(detected) if detected else ["unknown"],
            "indicators": indicators,
            "is_fullstack": "fullstack" in detected or (len(detected) >= 2)
        }

    def analyze_project_structure(self) -> dict:
        """Analyze files in the workspace and flag files exceeding 700 lines."""
        structure = {
            "total_files": 0,
            "by_type": {},
            "large_files": [],
            "directories": []
        }

        code_exts = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".rb", ".php", ".cs"}

        for root, dirs, files in os.walk(self.project_root):
            # Exclude directories
            dirs[:] = [
                d for d in dirs 
                if not d.startswith(".") 
                and d not in ["node_modules", "venv", "__pycache__", "dist", "build", "target"]
            ]

            rel_root = Path(root).relative_to(self.project_root)
            structure["directories"].append(str(rel_root))

            for f in files:
                structure["total_files"] += 1
                ext = Path(f).suffix

                if ext in code_exts:
                    if ext not in structure["by_type"]:
                        structure["by_type"][ext] = 0
                    structure["by_type"][ext] += 1

                    filepath = Path(root) / f
                    try:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                            line_count = sum(1 for _ in file)
                        if line_count > 700:
                            structure["large_files"].append({
                                "path": str(filepath.relative_to(self.project_root)),
                                "lines": line_count
                            })
                    except:
                        pass

        structure["large_files"].sort(key=lambda x: x["lines"], reverse=True)
        return structure

    def initialize_project(self) -> dict:
        """Initialize AI Team configuration and brain files for a new project workspace."""
        project_info = self.detect_project_type()
        structure = self.analyze_project_structure()

        state = {
            "schema_version": "2.1.0",
            "project_id": str(datetime.now(timezone.utc).timestamp()),
            "project_name": self.project_root.name,
            "phase": "initiation",
            "project_type": project_info["types"],
            "is_fullstack": project_info["is_fullstack"],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "components": {
                "product-owner": {"status": "pending", "progress": 0, "issues": [], "remaining": ["Analyze requirements"]},
                "architecture": {"status": "pending", "progress": 0, "issues": [], "remaining": ["Initial design"]},
                "ai-engineer": {"status": "pending", "progress": 0, "issues": [], "remaining": []},
                "backend": {"status": "pending", "progress": 0, "issues": [], "remaining": []},
                "frontend": {"status": "pending", "progress": 0, "issues": [], "remaining": []},
                "devops": {"status": "pending", "progress": 0, "issues": [], "remaining": []},
                "performance": {"status": "pending", "progress": 0, "issues": [], "remaining": []},
                "observability": {"status": "pending", "progress": 0, "issues": [], "remaining": []},
                "security": {"status": "pending", "progress": 0, "issues": [], "remaining": []},
                "privacy": {"status": "pending", "progress": 0, "issues": [], "remaining": []},
                "qa": {"status": "pending", "progress": 0, "issues": [], "remaining": []},
                "docs": {"status": "pending", "progress": 0, "issues": [], "remaining": []}
            },
            "blockers": [],
            "deployment_ready": False,
            "structure_analysis": {
                "total_files": structure["total_files"],
                "by_type": structure["by_type"],
                "large_files_count": len(structure["large_files"]),
                "large_files": structure["large_files"][:10]
            }
        }

        self.brain_manager.save_project_state(state)

        # Initialize team-lead brain
        team_lead_brain = {
            "agent": "team-lead",
            "version": "2.1.0",
            "last_update": datetime.now(timezone.utc).isoformat(),
            "state": {
                "status": "pending",
                "progress": 0,
                "deployment_blocked": False,
                "blocker_reason": None
            },
            "memory": {
                "active_tasks": [],
                "completed_tasks": [],
                "blockers": [],
                "key_decisions": [],
                "team_notes": [],
                "velocity": {
                    "sprints": [],
                    "average_velocity": 0.0,
                    "current_sprint": 1
                },
                "risk_matrix": []
            },
            "open_issues": [],
            "remaining": []
        }

        self.brain_manager.save_agent_brain("team-lead", team_lead_brain)

        # Initialize product-owner brain
        product_owner_brain = {
            "agent": "product-owner",
            "version": "2.1.0",
            "last_update": datetime.now(timezone.utc).isoformat(),
            "state": {
                "status": "pending",
                "progress": 0,
                "deployment_blocked": False,
                "blocker_reason": None
            },
            "sprint_metrics": {
                "current_sprint_goal": "",
                "planned_story_points": 0,
                "completed_story_points": 0,
                "blocked_story_points": 0
            },
            "backlog_summary": {
                "total_stories": 0,
                "ready_stories": 0,
                "in_progress_stories": 0,
                "blocked_stories": 0
            },
            "open_issues": [],
            "remaining": []
        }
        self.brain_manager.save_agent_brain("product-owner", product_owner_brain)

        # Initialize ai-engineer brain
        ai_engineer_brain = {
            "agent": "ai-engineer",
            "version": "2.1.0",
            "last_update": datetime.now(timezone.utc).isoformat(),
            "state": {
                "status": "pending",
                "progress": 0,
                "deployment_blocked": False,
                "blocker_reason": None
            },
            "models_used": {
                "generation": "claude-3-5-sonnet-20241022",
                "embeddings": "text-embedding-3-small",
                "reranking": "cohere-rerank-v3"
            },
            "vector_db": {
                "provider": "postgresql-pgvector",
                "index_type": "HNSW",
                "embedding_dimension": 1536,
                "distance_metric": "cosine"
            },
            "evaluations": {
                "last_evaluation_date": None,
                "faithfulness_avg": 0.0,
                "answer_relevance_avg": 0.0,
                "semantic_cache_hit_rate": 0.0
            },
            "open_issues": [],
            "remaining": []
        }
        self.brain_manager.save_agent_brain("ai-engineer", ai_engineer_brain)

        # Copy seed task queue if present
        seed_queue_path = Path(__file__).parent.parent / "brain" / "task-queue.toml"
        if seed_queue_path.exists():
            try:
                with open(seed_queue_path, "rb") as sf:
                    queue_data = tomllib.load(sf)
                self.brain_manager.save_task_queue(queue_data)
            except Exception as e:
                self.brain_manager.log_audit("seed_queue_error", {"error": str(e)})

        self.brain_manager.log_audit("initialization", {"project_name": state["project_name"]})
        return state

    def get_activation_prompt(self) -> str:
        """Generate a token-optimized dashboard prompt for session startup."""
        context = self.brain_manager.get_full_context()
        state = context["project_state"]
        analysis = self.analyze_project_structure()

        prompt_parts = [
            f"# AI Team Skills — Project Context Dashboard",
            f"",
            f"**Project**: {state.get('project_name', 'Unknown')}",
            f"**Phase**: {state.get('phase', 'Unknown')}",
            f"**Type**: {', '.join(state.get('project_type', ['Unknown']))}",
            f"",
        ]

        # Component statuses
        prompt_parts.append("## Component Status")
        for name, comp in state.get("components", {}).items():
            status_icon = "✅" if comp["status"] == "complete" else "🔄" if comp["status"] == "in_progress" else "⏳"
            progress = comp.get("progress", 0)
            prompt_parts.append(f"- {status_icon} **{name}**: {comp['status']} ({progress}%)")

        # Blockers
        blockers = state.get("blockers", [])
        if blockers:
            prompt_parts.append("")
            prompt_parts.append("## 🚫 Active Blockers")
            for b in blockers:
                if isinstance(b, dict):
                    prompt_parts.append(f"- [{b.get('source')}]: {b.get('message')}")
                else:
                    prompt_parts.append(f"- {b}")

        # Large files
        large_files = analysis["large_files"]
        if large_files:
            prompt_parts.append("")
            prompt_parts.append("## ⚠️ Files Exceeding 700 Lines (Refactoring Required)")
            for f in large_files[:5]:
                prompt_parts.append(f"- `{f['path']}`: {f['lines']} lines")

        return "\n".join(prompt_parts)

    def run(self) -> dict:
        """Run activation checks and return state."""
        state = self.brain_manager.get_project_state()

        if not state.get("project_id"):
            state = self.initialize_project()

        prompt = self.get_activation_prompt()
        print("\n" + prompt)

        return {
            "state": state,
            "activation_prompt": prompt
        }


def main():
    """CLI run helper."""
    project_root = Path.cwd() if len(sys.argv) < 2 or sys.argv[1].startswith("-") else Path(sys.argv[1])
    activator = AutoActivator(project_root)

    if len(sys.argv) >= 2 and "--prompt-only" in sys.argv:
        print(activator.get_activation_prompt())
    else:
        activator.run()


if __name__ == "__main__":
    main()