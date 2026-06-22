#!/usr/bin/env python3
"""
AI Team Agent Communication System — v2.1.0
Manages inter-agent message queues, dependencies, escalations, and deployment clearance.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Ensure console supports UTF-8 for emoji characters on Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Ensure current script directory is in path for imports
sys.path.append(str(Path(__file__).parent))
from brain_manager import BrainManager


class AgentStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    BLOCKED = "blocked"


@dataclass
class AgentMessage:
    """Standardized format for inter-agent messages."""
    from_agent: str
    to_agent: str
    message_type: str  # request, response, notification, escalation
    subject: str
    content: str
    timestamp: str
    priority: str = "normal"  # low, normal, high, critical
    references: list = None

    def __post_init__(self):
        if self.references is None:
            self.references = []

    def to_json(self) -> dict:
        return asdict(self)

    @classmethod
    def from_json(cls, data: dict) -> 'AgentMessage':
        return cls(**data)


class AgentCommunication:
    """Manages secure inter-agent communication, dependencies, and deployment readiness reviews."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.brain_manager = BrainManager(self.project_root)
        self.messages_dir = self.brain_manager.brain_dir / "messages"
        self.messages_dir.mkdir(exist_ok=True)

    # ==================== Agent Registry & Dependencies ====================

    def get_agent_dependencies(self) -> dict:
        """Get structural dependencies and orchestration configurations for all 13 agents."""
        return {
            "product-owner": {
                "manages": ["team-lead"],
                "blocks": ["architecture"],
                "blocked_by": []
            },
            "team-lead": {
                "manages": ["architecture", "ai-engineer", "backend", "frontend", "devops", "performance", "observability", "security", "privacy", "qa", "docs"],
                "blocks": ["deployment"],
                "blocked_by": ["product-owner"]
            },
            "architecture": {
                "manages": [],
                "blocks": ["ai-engineer", "backend", "frontend"],
                "blocked_by": []
            },
            "ai-engineer": {
                "manages": [],
                "blocks": ["backend", "frontend", "qa", "observability"],
                "blocked_by": ["architecture"]
            },
            "backend": {
                "manages": [],
                "blocks": ["frontend", "qa", "observability"],
                "blocked_by": ["architecture", "ai-engineer"]
            },
            "frontend": {
                "manages": [],
                "blocks": ["performance"],
                "blocked_by": ["architecture", "backend", "ai-engineer"]
            },
            "devops": {
                "manages": [],
                "blocks": ["observability", "deployment"],
                "blocked_by": []
            },
            "observability": {
                "manages": [],
                "blocks": ["deployment"],
                "blocked_by": ["backend", "devops", "ai-engineer"]
            },
            "qa": {
                "manages": [],
                "blocks": ["performance"],
                "blocked_by": ["backend", "frontend", "ai-engineer"]
            },
            "performance": {
                "manages": [],
                "blocks": ["security", "privacy", "deployment"],
                "blocked_by": ["frontend", "qa"]
            },
            "security": {
                "manages": [],
                "blocks": ["deployment"],
                "blocked_by": ["performance"],
                "veto_power": True
            },
            "privacy": {
                "manages": [],
                "blocks": ["deployment"],
                "blocked_by": ["performance"]
            },
            "docs": {
                "manages": [],
                "blocks": [],
                "blocked_by": ["architecture", "backend", "frontend"]
            }
        }

    def get_blockers_for_agent(self, agent_name: str) -> list:
        """Determine what components are currently blocking a specific agent's execution."""
        deps = self.get_agent_dependencies()
        agent_config = deps.get(agent_name, {})
        blockers = []

        for blocker in agent_config.get("blocked_by", []):
            brain = self.brain_manager.get_agent_brain(blocker)
            status = brain.get("state", {}).get("status", "pending")
            if status != "complete":
                blockers.append({
                    "agent": blocker,
                    "reason": f"Waiting for {blocker} to sign off",
                    "their_status": status
                })

        return blockers

    # ==================== Messaging Pipeline ====================

    def send_message(
        self,
        from_agent: str,
        to_agent: str,
        message_type: str,
        subject: str,
        content: str,
        priority: str = "normal"
    ) -> AgentMessage:
        """Send a message from one agent to another and save to the mailbox registry."""
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            subject=subject,
            content=content,
            timestamp=datetime.now(timezone.utc).isoformat(),
            priority=priority
        )

        # Write message file
        msg_file = self.messages_dir / f"{to_agent}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')}.json"
        with open(msg_file, "w", encoding="utf-8") as f:
            json.dump(message.to_json(), f, indent=2, ensure_ascii=False)

        # Notify recipient's brain
        recipient_brain = self.brain_manager.get_agent_brain(to_agent)
        if "pending_messages" not in recipient_brain:
            recipient_brain["pending_messages"] = []
        recipient_brain["pending_messages"].append({
            "from": from_agent,
            "subject": subject,
            "timestamp": message.timestamp
        })
        self.brain_manager.save_agent_brain(to_agent, recipient_brain)
        
        self.brain_manager.log_audit("agent_message_sent", {
            "from": from_agent,
            "to": to_agent,
            "type": message_type,
            "subject": subject
        })
        return message

    def get_messages_for_agent(self, agent_name: str) -> List[AgentMessage]:
        """Fetch all unread messages addressed to the specified agent."""
        messages = []
        for msg_file in self.messages_dir.glob(f"{agent_name}_*.json"):
            try:
                with open(msg_file, "r", encoding="utf-8") as f:
                    messages.append(AgentMessage.from_json(json.load(f)))
            except Exception as e:
                self.brain_manager.log_audit("message_read_error", {"file": msg_file.name, "error": str(e)})
        return sorted(messages, key=lambda m: m.timestamp, reverse=True)

    def acknowledge_message(self, message: AgentMessage) -> None:
        """Acknowledge a received message and move it to the archive directory."""
        for msg_file in self.messages_dir.glob(f"{message.to_agent}_*.json"):
            try:
                with open(msg_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("timestamp") == message.timestamp:
                    ack_dir = self.messages_dir / "acknowledged"
                    ack_dir.mkdir(exist_ok=True)
                    msg_file.rename(ack_dir / msg_file.name)
                    
                    # Update brain memory to clear notification
                    brain = self.brain_manager.get_agent_brain(message.to_agent)
                    if "pending_messages" in brain:
                        brain["pending_messages"] = [
                            m for m in brain["pending_messages"] 
                            if m.get("timestamp") != message.timestamp
                        ]
                        self.brain_manager.save_agent_brain(message.to_agent, brain)
                    
                    self.brain_manager.log_audit("agent_message_ack", {
                        "agent": message.to_agent, 
                        "from": message.from_agent, 
                        "timestamp": message.timestamp
                    })
                    break
            except Exception as e:
                self.brain_manager.log_audit("message_ack_error", {"error": str(e)})

    # ==================== Escalation Protocols ====================

    def escalate_to_team_lead(
        self,
        from_agent: str,
        issue: str,
        severity: str = "high"
    ) -> None:
        """Escalate an blocking issue to the Team Lead for sprint triage."""
        self.send_message(
            from_agent=from_agent,
            to_agent="team-lead",
            message_type="escalation",
            subject=f"ESCALATION [{severity.upper()}]: {issue}",
            content=f"Agent '{from_agent}' has escalated: {issue}",
            priority=severity
        )
        self.brain_manager.add_blocker(f"Escalation from {from_agent}: {issue}", from_agent)

    # ==================== Task Delegation & Resolution ====================

    def request_from_agent(
        self,
        from_agent: str,
        to_agent: str,
        task: str,
        context: dict = None
    ) -> None:
        """Trigger an official task request directed to another specialized agent."""
        content = f"Task requested: {task}"
        if context:
            content += f"\n\nContext:\n{json.dumps(context, indent=2)}"

        self.send_message(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type="request",
            subject=f"Task: {task}",
            content=content,
            priority="high"
        )

    def respond_to_request(
        self,
        from_agent: str,
        to_agent: str,
        original_task: str,
        response: str,
        status: str = "completed"
    ) -> None:
        """Send a task resolution payload responding to a previous request."""
        content = f"Response to: {original_task}\n\nStatus: {status}\n\nResponse:\n{response}"
        self.send_message(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type="response",
            subject=f"Re: {original_task}",
            content=content,
            priority="normal"
        )

    # ==================== Deployment Clearance Audit ====================

    def check_deployment_clearance(self) -> Tuple[bool, List[dict]]:
        """Run audit scan across all 13 agents to confirm deployment clearance."""
        deps = self.get_agent_dependencies()
        blockers = []

        for agent, config in deps.items():
            if "deployment" in config.get("blocks", []):
                brain = self.brain_manager.get_agent_brain(agent)
                state = brain.get("state", {})
                
                # Check deployment status
                if state.get("deployment_blocked"):
                    blockers.append({
                        "agent": agent,
                        "reason": state.get("blocker_reason", "Vulnerability found"),
                        "veto_power": config.get("veto_power", False)
                    })
                elif state.get("status") != "complete":
                    blockers.append({
                        "agent": agent,
                        "reason": f"Development not marked complete (status: {state.get('status')})",
                        "veto_power": config.get("veto_power", False)
                    })

        veto_blockers = [b for b in blockers if b.get("veto_power")]
        if veto_blockers:
            return False, veto_blockers

        return len(blockers) == 0, blockers


def main():
    """CLI handler."""
    if len(sys.argv) < 2:
        print("Usage: agent-communication.py <command> [args]")
        print("Commands: send, messages, blockers, clearance, deps")
        sys.exit(1)

    comm = AgentCommunication()
    command = sys.argv[1]

    if command == "deps":
        print(json.dumps(comm.get_agent_dependencies(), indent=2))

    elif command == "blockers":
        if len(sys.argv) < 3:
            print("Usage: agent-communication.py blockers <agent>")
            sys.exit(1)
        blockers = comm.get_blockers_for_agent(sys.argv[2])
        print(json.dumps(blockers, indent=2))

    elif command == "clearance":
        ready, blockers = comm.check_deployment_clearance()
        print(f"Deployment Cleared: {ready}")
        if blockers:
            print("Blockers:")
            for b in blockers:
                veto_tag = " [VETO POWER]" if b.get("veto_power") else ""
                print(f"  - {b['agent']}: {b['reason']}{veto_tag}")

    elif command == "messages":
        if len(sys.argv) < 3:
            print("Usage: agent-communication.py messages <agent>")
            sys.exit(1)
        msgs = comm.get_messages_for_agent(sys.argv[2])
        for msg in msgs:
            print(f"[{msg.timestamp}] {msg.from_agent} -> {msg.to_agent} ({msg.message_type}): {msg.subject}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()