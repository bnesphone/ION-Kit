/**
 * Git Integration
 * Get commit history and repository info
 */

import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export interface GitCommit {
  hash: string;
  author: string;
  date: string;
  message: string;
}

export interface GitStatus {
  branch: string;
  modified: string[];
  untracked: string[];
  staged: string[];
}

/**
 * Get Git commit history
 */
export async function getCommitHistory(options: {
  rootDir: string;
  limit?: number;
}): Promise<GitCommit[]> {
  const { rootDir, limit = 10 } = options;

  try {
    const { stdout } = await execAsync(
      `git log --pretty=format:"%H|%an|%ad|%s" --date=short -n ${limit}`,
      { cwd: rootDir }
    );

    const commits: GitCommit[] = [];
    
    for (const line of stdout.split('\n')) {
      if (!line) continue;
      const [hash, author, date, message] = line.split('|');
      commits.push({ hash, author, date, message });
    }

    return commits;
  } catch (error) {
    throw new Error(`Failed to get commit history: ${error}`);
  }
}

/**
 * Get Git status
 */
export async function getStatus(options: {
  rootDir: string;
}): Promise<GitStatus> {
  const { rootDir } = options;

  try {
    const { stdout: branchOut } = await execAsync('git branch --show-current', { cwd: rootDir });
    const { stdout: statusOut } = await execAsync('git status --porcelain', { cwd: rootDir });

    const status: GitStatus = {
      branch: branchOut.trim(),
      modified: [],
      untracked: [],
      staged: []
    };

    for (const line of statusOut.split('\n')) {
      if (!line) continue;
      const statusCode = line.substring(0, 2);
      const file = line.substring(3);

      if (statusCode === '??') status.untracked.push(file);
      else if (statusCode[0] !== ' ') status.staged.push(file);
      else if (statusCode[1] === 'M') status.modified.push(file);
    }

    return status;
  } catch (error) {
    throw new Error(`Failed to get status: ${error}`);
  }
}

/**
 * Format Git status
 */
export function formatGitStatus(status: GitStatus): string {
  let output = `Git Status\n`;
  output += `==========\n\n`;
  output += `Branch: ${status.branch}\n\n`;

  if (status.staged.length > 0) {
    output += `Staged (${status.staged.length}):\n`;
    for (const file of status.staged) {
      output += `  + ${file}\n`;
    }
    output += '\n';
  }

  if (status.modified.length > 0) {
    output += `Modified (${status.modified.length}):\n`;
    for (const file of status.modified) {
      output += `  M ${file}\n`;
    }
    output += '\n';
  }

  if (status.untracked.length > 0) {
    output += `Untracked (${status.untracked.length}):\n`;
    for (const file of status.untracked.slice(0, 10)) {
      output += `  ? ${file}\n`;
    }
    if (status.untracked.length > 10) {
      output += `  ... and ${status.untracked.length - 10} more\n`;
    }
  }

  return output;
}
