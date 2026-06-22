#!/usr/bin/env python3
"""
AI Team Brain Manager — v2.1.0
Centralizes agent memory, configuration validation, schema enforcement, and audit logs.
"""

import json
import os
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Tuple, List, Dict

# Ensure console supports UTF-8 for emoji characters on Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

class BrainManager:
    """Centralized manager for AI Team memory state, schemas, and audit trails."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.brain_dir = self.project_root / ".ai-team" / "brain"
        self.brain_dir.mkdir(parents=True, exist_ok=True)
        self.audit_log_path = self.brain_dir / "audit-log.jsonl"

    # ==================== Audit Trail Logging ====================

    def log_audit(self, event_type: str, details: Dict[str, Any]) -> None:
        """Log events to the JSONL audit trail."""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "details": details
        }
        with open(self.audit_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    # ==================== Schema Validation ====================

    def validate_project_state(self, state: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate project-state schema against v2.1.0 requirements."""
        errors = []
        required_keys = ["project_id", "project_name", "phase", "components", "blockers", "deployment_ready"]
        for key in required_keys:
            if key not in state:
                errors.append(f"Missing required key: '{key}'")

        if "components" in state:
            expected_components = [
                "product-owner", "architecture", "ai-engineer", "backend", "frontend", "devops", 
                "performance", "observability", "security", "privacy", "qa", "docs"
            ]
            for comp in expected_components:
                if comp not in state["components"]:
                    errors.append(f"Missing component: '{comp}' in state['components']")
                else:
                    comp_keys = ["status", "progress", "issues", "remaining"]
                    for ck in comp_keys:
                        if ck not in state["components"][comp]:
                            errors.append(f"Component '{comp}' missing required key: '{ck}'")
        return len(errors) == 0, errors

    def validate_agent_brain(self, agent_name: str, brain: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate agent brain schema against v2.1.0 requirements."""
        errors = []
        required_keys = ["agent", "version", "last_update", "state"]
        for key in required_keys:
            if key not in brain:
                errors.append(f"Agent '{agent_name}' missing key: '{key}'")
        if "state" in brain:
            state_keys = ["status", "progress", "deployment_blocked"]
            for sk in state_keys:
                if sk not in brain["state"]:
                    errors.append(f"Agent '{agent_name}' state missing key: '{sk}'")
        return len(errors) == 0, errors

    # ==================== Migration Engine ====================

    def migrate_v1_to_v2(self) -> dict:
        """Migrate v1.0.0 flat JSON database structures to versioned v2.1.0 schemas."""
        state_file = self.brain_dir / "project-state.json"
        
        # 1. Migrate task-queue.json to task-queue.toml if exists
        old_queue = self.brain_dir / "task-queue.json"
        new_queue = self.brain_dir / "task-queue.toml"
        if old_queue.exists() and not new_queue.exists():
            try:
                with open(old_queue, "r") as f:
                    tasks_list = json.load(f)
                meta = {"version": "2.1.0", "queue_updated": datetime.now(timezone.utc).isoformat(), "next_task_id": len(tasks_list) + 1}
                toml_content = self.serialize_toml({"meta": meta, "tasks": tasks_list})
                with open(new_queue, "w", encoding="utf-8") as f:
                    f.write(toml_content)
                old_queue.unlink()
                self.log_audit("migration_task_queue", {"status": "success", "from": "json", "to": "toml"})
            except Exception as e:
                self.log_audit("migration_task_queue", {"status": "failed", "error": str(e)})

        # 2. Update project-state schema version and new components
        state = self._default_state()
        if state_file.exists():
            try:
                with open(state_file, "r") as f:
                    old_state = json.load(f)
                
                # Copy old fields
                state["project_id"] = old_state.get("project_id", state["project_id"])
                state["project_name"] = old_state.get("project_name", state["project_name"])
                state["phase"] = old_state.get("phase", state["phase"])
                state["created_at"] = old_state.get("created_at", state["created_at"])
                state["blockers"] = old_state.get("blockers", state["blockers"])
                state["deployment_ready"] = old_state.get("deployment_ready", state["deployment_ready"])
                
                # Merge existing components status
                if "components" in old_state:
                    for k, v in old_state["components"].items():
                        if k in state["components"]:
                            state["components"][k].update(v)

                self.log_audit("migration_project_state", {"status": "success", "from": "v1.0.0", "to": "v2.1.0"})
            except Exception as e:
                self.log_audit("migration_project_state", {"status": "failed", "error": str(e)})
        
        state["schema_version"] = "2.1.0"
        self.save_project_state(state)
        return state

    # ==================== I/O Handling ====================

    def get_project_state(self) -> Dict[str, Any]:
        """Load and return the project state. Auto-migrates if outdated."""
        state_file = self.brain_dir / "project-state.json"
        if not state_file.exists():
            state = self._default_state()
            self.save_project_state(state)
            return state

        with open(state_file, "r", encoding="utf-8") as f:
            state = json.load(f)
        
        # Check if migration is needed
        if state.get("schema_version") != "2.1.0":
            state = self.migrate_v1_to_v2()

        return state

    def save_project_state(self, state: Dict[str, Any]) -> None:
        """Validate and save project state with audit logging."""
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        state["schema_version"] = "2.1.0"
        
        valid, errors = self.validate_project_state(state)
        if not valid:
            raise ValueError(f"Invalid project state schema: {', '.join(errors)}")

        state_file = self.brain_dir / "project-state.json"
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        self.log_audit("save_project_state", {"project_name": state.get("project_name")})

    def get_agent_brain(self, agent_name: str) -> Dict[str, Any]:
        """Load specific agent brain."""
        brain_file = self.brain_dir / f"{agent_name}-brain.json"
        if brain_file.exists():
            with open(brain_file, "r", encoding="utf-8") as f:
                brain = json.load(f)
            # Ensure v2 compatibility
            if "state" not in brain:
                brain["state"] = {
                    "status": brain.get("status", "pending"),
                    "progress": brain.get("progress", 0),
                    "deployment_blocked": brain.get("deployment_blocked", False)
                }
            return brain
        return self._default_agent_brain(agent_name)

    def save_agent_brain(self, agent_name: str, brain: Dict[str, Any]) -> None:
        """Validate and save agent brain with audit logging."""
        brain["last_update"] = datetime.now(timezone.utc).isoformat()
        brain["version"] = "2.1.0"
        
        valid, errors = self.validate_agent_brain(agent_name, brain)
        if not valid:
            raise ValueError(f"Invalid agent brain schema for '{agent_name}': {', '.join(errors)}")

        brain_file = self.brain_dir / f"{agent_name}-brain.json"
        with open(brain_file, "w", encoding="utf-8") as f:
            json.dump(brain, f, indent=2, ensure_ascii=False)
        self.log_audit("save_agent_brain", {"agent": agent_name, "status": brain["state"]["status"]})

    def get_task_queue(self) -> Dict[str, Any]:
        """Load and return task queue from TOML file."""
        queue_file = self.brain_dir / "task-queue.toml"
        if not queue_file.exists():
            return {"meta": {"version": "2.1.0", "queue_updated": "", "next_task_id": 1}, "tasks": []}

        with open(queue_file, "rb") as f:
            return tomllib.load(f)

    def save_task_queue(self, queue: Dict[str, Any]) -> None:
        """Save task queue to TOML file with audit logging."""
        queue["meta"]["queue_updated"] = datetime.now(timezone.utc).isoformat()
        queue_file = self.brain_dir / "task-queue.toml"
        toml_content = self.serialize_toml(queue)
        with open(queue_file, "w", encoding="utf-8") as f:
            f.write(toml_content)
        self.log_audit("save_task_queue", {"task_count": len(queue.get("tasks", []))})

    def update_task_status(self, task_id: int, status: str, agent: str) -> None:
        """Update task status in queue."""
        queue = self.get_task_queue()
        for task in queue.get("tasks", []):
            if task["id"] == task_id:
                task["status"] = status
                task["assigned_to"] = agent
                task["updated_at"] = datetime.now(timezone.utc).isoformat()
                break
        self.save_task_queue(queue)
        self.log_audit("update_task_status", {"task_id": task_id, "status": status, "assigned_to": agent})

    def update_component_status(
        self, component: str, status: str, progress: int = 0, issues: list = None
    ) -> None:
        """Update component status."""
        state = self.get_project_state()
        if component in state["components"]:
            state["components"][component]["status"] = status
            state["components"][component]["progress"] = progress
            if issues:
                state["components"][component]["issues"].extend(issues)
            if status == "complete":
                state["components"][component]["completed_at"] = datetime.now(timezone.utc).isoformat()
        self.save_project_state(state)

    def check_deployment_ready(self) -> Tuple[bool, List[str]]:
        """Check if project is ready for deployment."""
        state = self.get_project_state()
        blockers = []

        for name, component in state["components"].items():
            if component["status"] != "complete":
                blockers.append(f"{name}: not complete ({component['progress']}%)")
            if component["issues"]:
                blockers.append(f"{name}: has {len(component['issues'])} issues")

        for blocker in state.get("blockers", []):
            if isinstance(blocker, dict):
                blockers.append(f"{blocker.get('source')}: {blocker.get('message')}")
            else:
                blockers.append(str(blocker))

        return len(blockers) == 0, blockers

    def add_blocker(self, blocker: str, source: str) -> None:
        """Add deployment blocker."""
        state = self.get_project_state()
        state["blockers"].append({
            "message": blocker,
            "source": source,
            "added_at": datetime.now(timezone.utc).isoformat()
        })
        self.save_project_state(state)
        self.log_audit("add_blocker", {"source": source, "message": blocker})

    def remove_blocker(self, blocker: str) -> None:
        """Remove deployment blocker."""
        state = self.get_project_state()
        state["blockers"] = [
            b for b in state["blockers"] 
            if (isinstance(b, dict) and b["message"] != blocker) or (not isinstance(b, dict) and b != blocker)
        ]
        self.save_project_state(state)
        self.log_audit("remove_blocker", {"message": blocker})

    def get_full_context(self, agents: List[str] = None) -> Dict[str, Any]:
        """Get token-optimized context for session restoration."""
        agents = agents or [
            "product-owner", "team-lead", "architecture", "ai-engineer", "backend", "frontend", "devops", 
            "performance", "observability", "security", "privacy", "qa", "docs"
        ]
        context = {
            "project_state": self.get_project_state(),
            "task_queue": self.get_task_queue(),
            "agents": {}
        }
        for agent in agents:
            context["agents"][agent] = self.get_agent_brain(agent)
        return context

    # ==================== Helper Methods ====================

    def serialize_toml(self, data: Dict[str, Any]) -> str:
        """Custom simple TOML serializer for task queues."""
        lines = ["# AI Team Task Queue", "# Token-optimized task assignment format", ""]
        if "meta" in data:
            lines.append("[meta]")
            for k, v in data["meta"].items():
                if isinstance(v, str):
                    lines.append(f'{k} = "{v}"')
                else:
                    lines.append(f'{k} = {v}')
            lines.append("")

        if "tasks" in data:
            for task in data["tasks"]:
                lines.append("[[tasks]]")
                for k, v in task.items():
                    if isinstance(v, str):
                        lines.append(f'{k} = "{v}"')
                    elif isinstance(v, list):
                        items_str = ", ".join(str(x) for x in v)
                        lines.append(f'{k} = [{items_str}]')
                    elif isinstance(v, bool):
                        lines.append(f'{k} = {"true" if v else "false"}')
                    else:
                        lines.append(f'{k} = {v}')
                lines.append("")
        return "\n".join(lines)

    def _default_state(self) -> Dict[str, Any]:
        """Default project state configuration v2.1.0."""
        return {
            "schema_version": "2.1.0",
            "project_id": "",
            "project_name": "",
            "phase": "initiation",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "components": {
                "product-owner": {"status": "pending", "progress": 0, "issues": [], "remaining": []},
                "architecture": {"status": "pending", "progress": 0, "issues": [], "remaining": []},
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
            "deployment_ready": False
        }

    def _default_agent_brain(self, agent_name: str) -> Dict[str, Any]:
        """Default agent brain layout."""
        return {
            "agent": agent_name,
            "version": "2.1.0",
            "last_update": None,
            "state": {
                "status": "pending",
                "progress": 0,
                "deployment_blocked": False,
                "blocker_reason": None
            },
            "memory": {},
            "open_issues": [],
            "remaining": []
        }

def main():
    """CLI interface for brain manager."""
    if len(sys.argv) < 2:
        print("Usage: brain_manager.py <command> [args]")
        print("Commands: state, tasks, ready, context, migrate, audit")
        sys.exit(1)

    manager = BrainManager()
    command = sys.argv[1]

    if command == "state":
        print(json.dumps(manager.get_project_state(), indent=2, ensure_ascii=False))

    elif command == "tasks":
        print(json.dumps(manager.get_task_queue(), indent=2, ensure_ascii=False))

    elif command == "ready":
        ready, blockers = manager.check_deployment_ready()
        print(f"Deployment Ready: {ready}")
        if blockers:
            print("Blockers:")
            for b in blockers:
                print(f"  - {b}")

    elif command == "context":
        print(json.dumps(manager.get_full_context(), indent=2, ensure_ascii=False))

    elif command == "migrate":
        manager.migrate_v1_to_v2()
        print("✅ Migration completed to v2.1.0!")

    elif command == "audit":
        audit_file = manager.audit_log_path
        if audit_file.exists():
            with open(audit_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines[-20:]:  # Print last 20 audit events
                print(line.strip())
        else:
            print("No audit trail found yet.")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()