# Story template: Feature / Agent

Every feature story MUST follow this structure.

## Required sections

### 1. Available APIs & data sources
- API endpoints with URL, auth, rate limits, cost
- Response format (relevant fields)
- Free tier vs. paid — which do we need?

### 2. Code examples (project pattern)
- Concrete fetch functions in project style
- Error handling, timeout, fallback
- No npm if stdlib is enough

### 3. Signal format & config integration
- Signal output JSON (`signals/xyz.json`) in the standard format:
  `{ timestamp, agent, score, signal, components, flags }`
- Config entries: AGENT_WEIGHTS, SIGNAL_FILES
- Tier assignment (fast/medium/slow)
- Scoring logic explained

### 4. Architecture integration
- ASCII diagram: data sources → agent → signal → supervisor
- Weight in supervisor, protected-agents yes/no

### 5. Phased plan
- Phase 1 (free) → Phase 2 (free APIs) → Phase 3 (paid optional)

### 6. Dependencies (MANDATORY)
```markdown
## Dependencies
- Needs: [STORY-XX] (must be done first)
- Affects: [STORY-YY] (will be altered by this story)

## Position in overall plan
- Order: #X/Y | Phase: [phase name]
- Predecessor: STORY-XX
- Successor: STORY-ZZ
```

### 7. Acceptance criteria
- Checkboxes, testable, concrete

### 8. Security Impact (MANDATORY)
- Change type: `none | api | auth | data | dependency | ci | governance | external-provider`
- New or changed attack surface?
- Are personal data, secrets, tokens, cookies, or external providers touched?
- Which sections from `SECURITY.md` and which security references must `/implement` read?
- If there is no security impact: explicitly explain why; do not leave this empty.

### 9. Security Validation (MANDATORY for code, security, tooling, dependency, CI, or governance changes)
- Which local checks must run? (e.g. Semgrep, dependency-check, tests, manual review)
- Which sensitive paths may be affected?
- What evidence must be documented before `Done`?
- Which risks remain knowingly accepted?

### 10. Dependencies
- Only if stdlib is insufficient
- Reason why
