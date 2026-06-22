#!/usr/bin/env node

/**
 * AI Team Skills CLI — v2.1.0
 * Multi-agent development team initialization and management CLI.
 */

import { Command } from 'commander';
import chalk from 'chalk';
import fs from 'fs-extra';
import inquirer from 'inquirer';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const program = new Command();

// All 11 skill files to copy
const SKILL_FILES = [
  'product-owner.md',
  'team-lead.md',
  'architecture.md',
  'ai-engineer.md',
  'backend.md',
  'frontend.md',
  'devops.md',
  'performance.md',
  'observability.md',
  'security.md',
  'privacy.md',
  'qa.md',
  'docs.md',
  'INSTALL.md',
];

// Platform-specific directories
const PLATFORM_DIRS = {
  claude: '.claude/skills',
  cursor: '.cursor/skills',
  windsurf: '.windsurf/skills',
  vscode: '.vscode/ai-team-skills',
  generic: 'ai-team-skills',
};

async function copySkillFiles(targetDir: string, platform: string) {
  // Source is in .claude/skills relative to workspace root
  const sourceDir = path.join(__dirname, '..', '..', '.claude', 'skills');
  const destDir = path.join(targetDir, PLATFORM_DIRS[platform] || PLATFORM_DIRS.generic);

  console.log(chalk.blue(`Copying skill files to ${destDir}...`));

  await fs.ensureDir(destDir);

  for (const file of SKILL_FILES) {
    const src = path.join(sourceDir, file);
    const dest = path.join(destDir, file);
    if (await fs.pathExists(src)) {
      await fs.copy(src, dest);
      console.log(chalk.green(`  ✓ Copied ${file}`));
    } else {
      console.log(chalk.yellow(`  ⚠ Source file missing: ${file}`));
    }
  }

  // Copy brain directory structure
  const brainDir = path.join(targetDir, '.ai-team', 'brain');
  await fs.ensureDir(brainDir);

  const projectStateFile = path.join(brainDir, 'project-state.json');
  if (!(await fs.pathExists(projectStateFile))) {
    await fs.writeJSON(projectStateFile, {
      schema_version: '2.1.0',
      project_id: String(Date.now()),
      project_name: path.basename(targetDir),
      phase: 'initiation',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      components: {
        'product-owner': { status: 'pending', progress: 0, issues: [], remaining: [] },
        architecture: { status: 'pending', progress: 0, issues: [], remaining: [] },
        'ai-engineer': { status: 'pending', progress: 0, issues: [], remaining: [] },
        backend: { status: 'pending', progress: 0, issues: [], remaining: [] },
        frontend: { status: 'pending', progress: 0, issues: [], remaining: [] },
        devops: { status: 'pending', progress: 0, issues: [], remaining: [] },
        performance: { status: 'pending', progress: 0, issues: [], remaining: [] },
        observability: { status: 'pending', progress: 0, issues: [], remaining: [] },
        security: { status: 'pending', progress: 0, issues: [], remaining: [] },
        privacy: { status: 'pending', progress: 0, issues: [], remaining: [] },
        qa: { status: 'pending', progress: 0, issues: [], remaining: [] },
        docs: { status: 'pending', progress: 0, issues: [], remaining: [] },
      },
      blockers: [],
      deployment_ready: false,
    }, { spaces: 2 });
  }

  // Copy default task-queue.toml if exists in source
  const srcQueue = path.join(sourceDir, '..', '..', 'src', 'ai-team', 'brain', 'task-queue.toml');
  const destQueue = path.join(brainDir, 'task-queue.toml');
  if (await fs.pathExists(srcQueue) && !(await fs.pathExists(destQueue))) {
    await fs.copy(srcQueue, destQueue);
  }

  console.log(chalk.green('Brain directory initialized successfully.'));
}

async function initializeProject(targetDir: string, platform: string, options: any) {
  console.log(chalk.cyan('\n🤖 AI Team Skills Initialization\n'));

  let projectName = options.name;
  if (!projectName) {
    const answers = await inquirer.prompt([
      {
        type: 'input',
        name: 'projectName',
        message: 'Project name:',
        default: path.basename(targetDir),
      },
    ]);
    projectName = answers.projectName;
  }

  await copySkillFiles(targetDir, platform);

  // Write files to targetDir depending on platform selection
  const readmeContent = `# ${projectName}
  
> AI Team Skills powered project (v2.1.0)

## Team Members
- **Product Owner**: Backlog grooming, user stories, Gherkin acceptance criteria
- **Team Lead**: Project coordination, sprint metrics and quality gates
- **Architecture**: System design and tech stack selection
- **AI Engineer**: LLM integrations, prompt engineering, RAG, vector databases
- **Backend**: APIs, business logic, and DB query optimization
- **Frontend**: Responsive UI, WCAG 2.2 accessibility, and Web Vitals
- **DevOps**: Containerization, CI/CD automation, and deployment orchestration
- **Performance**: Latency profiles, caching strategies, and load testing
- **Observability**: Metrics aggregation, structured logging, and traces correlation
- **Security**: OWASP 2024 compliance and SAST/DAST audits (VETO POWER)
- **Privacy**: GDPR/CCPA/KVKK compliance and DPIA audits
- **QA**: Automated test suites (Jest, Playwright, Pact, Stryker)
- **Docs**: Runbooks, OpenAPI specs, and incident post-mortems

## Quick Start
\`\`\`bash
# Install CLI commands
npm install -g

# Query team status report
aiteam status

# Check quality gates status
aiteam deploy-check

# Start a sprint
aiteam sprint start
\`\`\`
`;

  await fs.writeFile(path.join(targetDir, 'AI-TEAM.md'), readmeContent);
  console.log(chalk.green(`\n✅ AI Team Skills initialized for ${projectName}`));
}

program
  .name('aiteam')
  .description('AI Team Skills CLI - Multi-agent development team')
  .version('2.1.0');

program
  .command('init')
  .description('Initialize AI Team Skills in a project')
  .option('-n, --name <name>', 'Project name')
  .option('-a, --ai <platform>', 'AI platform (claude, cursor, windsurf, generic)', 'claude')
  .action(async (options) => {
    await initializeProject(process.cwd(), options.ai, options);
  });

program
  .command('status')
  .description('Show team status report')
  .action(async () => {
    const stateFile = path.join(process.cwd(), '.ai-team', 'brain', 'project-state.json');
    if (!(await fs.pathExists(stateFile))) {
      console.log(chalk.red('\n✗ Project state not found. Initialize using "aiteam init" first.\n'));
      return;
    }

    try {
      const state = await fs.readJSON(stateFile);
      console.log(chalk.cyan(`\n🤖 AI Team Status Report — ${state.project_name || 'Project'}\n`));
      console.log(`Phase:      ${chalk.bold(state.phase.toUpperCase())}`);
      
      console.log(`\nComponents:`);
      let completeCount = 0;
      const componentEntries = Object.entries(state.components);
      for (const [name, info] of componentEntries) {
        const compInfo = info as any;
        const progressStr = `${compInfo.progress}%`;
        let statusStr = '';
        if (compInfo.status === 'complete') {
          statusStr = chalk.green('✔ COMPLETE');
          completeCount++;
        } else if (compInfo.status === 'in_progress') {
          statusStr = chalk.yellow('⏳ IN PROGRESS');
        } else {
          statusStr = chalk.gray('⏳ PENDING');
        }
        console.log(`  - ${name.padEnd(15)}: [${progressStr.padEnd(4)}] ${statusStr}`);
      }

      const overallProgress = Math.round((completeCount / componentEntries.length) * 100);
      console.log(`\nOverall Completion: ${chalk.bold(`${overallProgress}%`)}`);

      if (state.blockers && state.blockers.length > 0) {
        console.log(chalk.red(`\n🚫 Active Blockers (${state.blockers.length}):`));
        for (const blocker of state.blockers) {
          if (typeof blocker === 'object') {
            console.log(chalk.red(`  - [${blocker.source}]: ${blocker.message}`));
          } else {
            console.log(chalk.red(`  - ${blocker}`));
          }
        }
      } else {
        console.log(chalk.green('\n✔ No active blockers!'));
      }
      console.log('');
    } catch (e: any) {
      console.log(chalk.red(`\n✗ Error parsing project state: ${e.message}\n`));
    }
  });

program
  .command('deploy-check')
  .description('Check deployment readiness against quality gates')
  .action(async () => {
    const stateFile = path.join(process.cwd(), '.ai-team', 'brain', 'project-state.json');
    if (!(await fs.pathExists(stateFile))) {
      console.log(chalk.red('\n✗ Project state not found. Initialize using "aiteam init" first.\n'));
      return;
    }

    try {
      const state = await fs.readJSON(stateFile);
      console.log(chalk.cyan('\n🚀 Deployment Readiness Check\n'));
      
      let allPassed = true;
      const gates = [
        { name: 'Security Audit', key: 'security', minProgress: 100 },
        { name: 'QA Test Coverage', key: 'qa', minProgress: 100 },
        { name: 'Docs & Runbooks', key: 'docs', minProgress: 100 },
        { name: 'DevOps & Secrets', key: 'devops', minProgress: 100 },
        { name: 'Performance Budgets', key: 'performance', minProgress: 100 },
      ];

      for (const gate of gates) {
        const comp = state.components[gate.key];
        if (comp && comp.status === 'complete' && comp.progress >= gate.minProgress) {
          console.log(`  ${chalk.green('✔')} ${gate.name.padEnd(20)}: ${chalk.green('PASSED')}`);
        } else {
          console.log(`  ${chalk.red('✗')} ${gate.name.padEnd(20)}: ${chalk.red('BLOCKED')} (Progress: ${comp ? comp.progress : 0}%)`);
          allPassed = false;
        }
      }

      if (state.blockers && state.blockers.length > 0) {
        console.log(chalk.red(`\n🚫 Deployment blocked by ${state.blockers.length} active blockers.`));
        allPassed = false;
      }

      if (allPassed) {
        console.log(chalk.green('\n🎉 ALL QUALITY GATES GREEN! Ready for deployment.'));
      } else {
        console.log(chalk.yellow('\n⚠ Deployment blocked. Please complete requirements and resolve blockers.'));
      }
      console.log('');
    } catch (e: any) {
      console.log(chalk.red(`\n✗ Error checking deployment readiness: ${e.message}\n`));
    }
  });

program
  .command('sprint')
  .description('Sprint planning and velocity management')
  .argument('[action]', 'start, end, status', 'status')
  .action(async (action) => {
    const leadFile = path.join(process.cwd(), '.ai-team', 'brain', 'team-lead-brain.json');
    if (!(await fs.pathExists(leadFile))) {
      console.log(chalk.red('\n✗ Team Lead brain file not found. Run "aiteam init" first.\n'));
      return;
    }

    try {
      const brain = await fs.readJSON(leadFile);
      const velocity = brain.memory.velocity || { sprints: [], average_velocity: 0, current_sprint: 1 };
      
      console.log(chalk.cyan(`\n🏃 Sprint Management — Current Sprint: ${velocity.current_sprint}\n`));

      if (action === 'start') {
        velocity.current_sprint += 1;
        brain.memory.velocity = velocity;
        await fs.writeJSON(leadFile, brain, { spaces: 2 });
        console.log(chalk.green(`Sprint ${velocity.current_sprint} successfully started!`));
      } else if (action === 'end') {
        console.log(chalk.green(`Sprint ${velocity.current_sprint} completed!`));
      } else {
        console.log(`Average Velocity: ${chalk.bold(velocity.average_velocity)} pts`);
        console.log(`Past Sprints:`);
        if (velocity.sprints.length === 0) {
          console.log('  No sprint data recorded yet.');
        } else {
          for (const s of velocity.sprints) {
            console.log(`  - Sprint ${s.sprint}: Planned ${s.planned}pts, Completed ${s.completed}pts`);
          }
        }
      }
      console.log('');
    } catch (e: any) {
      console.log(chalk.red(`\n✗ Error: ${e.message}\n`));
    }
  });

program
  .command('adr')
  .description('Spawn a new Architecture Decision Record')
  .action(async () => {
    const adrDir = path.join(process.cwd(), 'docs', 'adr');
    await fs.ensureDir(adrDir);

    const files = await fs.readdir(adrDir);
    const adrFiles = files.filter(f => f.startsWith('ADR-') && f.endsWith('.md'));
    const nextId = String(adrFiles.length + 1).padStart(3, '0');

    const answers = await inquirer.prompt([
      { type: 'input', name: 'title', message: 'ADR Title:' },
      { type: 'input', name: 'slug', message: 'ADR Filename Slug (e.g. use-redis-caching):' },
    ]);

    const filename = `ADR-${nextId}-${answers.slug}.md`;
    const adrPath = path.join(adrDir, filename);

    const content = `# ADR-${nextId}: ${answers.title}

**Date**: ${new Date().toISOString().split('T')[0]}
**Status**: Proposed
**Deciders**: Team Lead, Architecture Agent

## Context & Problem Statement
[Describe the problem requiring a decision.]

## Decision Drivers
* [Driver 1]
* [Driver 2]

## Considered Options
1. Option A
2. Option B

## Decision Outcome
Chosen option: [Option], because [reasons].
`;

    await fs.writeFile(adrPath, content);
    console.log(chalk.green(`\n✔ ADR created successfully at docs/adr/${filename}\n`));
  });

program.parse(process.argv);