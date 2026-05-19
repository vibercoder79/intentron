# Story template: Fix / Refactor

For bug fixes, refactors, and small changes. Less overhead than the feature template.

## Required sections

### 1. Problem description
- What is broken / suboptimal?
- How does it manifest? (error message, behavior, log entry)
- Since when? (version, commit if known)

### 2. Affected files
- Which files need to change?
- Which components are affected?

### 3. Solution
- Concrete fix approach
- Code example if helpful

### 4. Dependencies (MANDATORY)
```markdown
## Dependencies
- Needs: [STORY-XX] or none
- Affects: [STORY-YY] or none

## Position in overall plan
- Independent / or specify order
```

### 5. Acceptance criteria
- Checkboxes, testable

### 6. Security Impact (MANDATORY)
- Change type: `none | api | auth | data | dependency | ci | governance | external-provider`
- Does the fix touch sensitive paths, external inputs, secrets, auth, data storage, or CI/governance?
- Which sections from `SECURITY.md` must `/implement` read?
- If there is no security impact: briefly explain why.

### 7. Security Validation (MANDATORY for code, security, tooling, dependency, CI, or governance changes)
- Which checks must run before `Done`?
- What evidence belongs in the closing comment?
- Which residual risks remain knowingly accepted?
