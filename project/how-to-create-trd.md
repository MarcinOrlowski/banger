# How to Create a Compact TRD (Technical Requirements Document)

## Core Principle

**The TRD answers HOW we'll build what the PRD describes.** Keep it focused on decisions, not possibilities.

## Target Length & Format

- **Maximum length**: 2-3 pages
- **Format**: Markdown with diagrams where appropriate
- **Rule**: If you're listing options without decisions, you're not ready to write the TRD

## Required Sections

### 1. Technical Approach (1 paragraph)

```markdown
## Technical Approach
- High-level architecture decision
- Technology stack (only what's new/different)
- Integration points
```

**Example:**
> We'll implement water tracking as a React component in our existing mobile app, storing data in
> our PostgreSQL database with a new `hydration_logs` table. The feature will use our existing
> notification service for reminders and integrate with the current nutrition module via shared
> user_id foreign keys.

### 2. Data Model (If applicable)

```markdown
## Data Model
- Key entities and relationships
- Use simple diagrams/tables
- Only include what changes
```

**Example:**

```sql
hydration_logs
- id (UUID, PK)
- user_id (FK -> users.id)
- amount_ml (INTEGER)
- logged_at (TIMESTAMP)
- source (ENUM: 'manual', 'reminder')

Daily index on (user_id, logged_at::date) for quick aggregations
```

### 3. API/Interface Design

```markdown
## API Design
- Endpoint signatures (not full specs)
- Key request/response examples
- Error handling approach
```

**Example:**

```text
POST /api/v1/hydration/log
Request: { amount_ml: 250 }
Response: { id: "uuid", daily_total_ml: 1750 }

GET /api/v1/hydration/daily?date=2024-01-15
Response: { date: "2024-01-15", total_ml: 2500, logs: [...] }

Errors: Standard 400/401/500 with { error: "message" }
```

### 4. Security & Performance

```markdown
## Security & Performance
- Specific requirements only
- Quantifiable targets
```

**Example:**

- Authentication: Existing JWT token validation
- Rate limiting: 100 logs per user per hour
- Performance: <200ms response time for logging
- Data retention: 90 days of detailed logs, then daily aggregates only

### 5. Technical Risks & Mitigations

```markdown
## Technical Risks & Mitigations
- Top 2-3 risks only
- One-line mitigation for each
```

**Example:**

1. **Risk**: Database bloat from high-frequency logging → **Mitigation**: Daily aggregation job + 90-day retention
2. **Risk**: Notification service overload → **Mitigation**: Batch notifications, max 5/day per user
3. **Risk**: Mobile app performance impact → **Mitigation**: Local caching with background sync

### 6. Implementation Plan

```markdown
## Implementation Plan
- Phase breakdown (if phased)
- Dependencies
- Rough time estimates
```

**Example:**

- Phase 1 (S): Database schema + basic API endpoints - 2 days
- Phase 2 (M): Mobile UI component + integration - 3 days  
- Phase 3 (S): Notification service integration - 2 days
- Phase 4 (S): Analytics dashboard update - 1 day

Dependencies: Nutrition module v2.0 deployed

## Writing Best Practices

### DO:

- ✅ Reference the PRD version you're implementing
- ✅ Focus on implementation decisions
- ✅ Use diagrams over lengthy explanations
- ✅ Include rollback/feature flag strategy
- ✅ Specify monitoring and logging approach
- ✅ Define clear integration boundaries

### DON'T:

- ❌ Repeat requirements from the PRD
- ❌ List multiple options without choosing
- ❌ Include full API documentation
- ❌ Copy-paste from external docs
- ❌ Forget about error cases
- ❌ Skip deployment considerations

## Quick Quality Checklist

Before finalizing your TRD, ensure:

- [ ] All technical decisions are made and justified
- [ ] A developer can start coding with just this doc
- [ ] Risks and mitigations are identified
- [ ] Performance targets are quantified
- [ ] Rollback plan is defined
- [ ] No requirements are repeated from PRD

## TRD Template

```markdown
# [Feature Name] TRD

**Ticket**: [Link to github ticket]
**PRD Reference**: [PRD version]

## Technical Approach
[1 paragraph describing overall implementation strategy]

## Data Model
[Tables/schemas/entities that change or are added]

## API Design
[Endpoint signatures and key examples]

## Security & Performance
- [Specific requirement]: [Target/approach]
- [Specific requirement]: [Target/approach]

## Technical Risks & Mitigations
1. **Risk**: [Description] → **Mitigation**: [Approach]
2. **Risk**: [Description] → **Mitigation**: [Approach]

## Implementation Plan
- [Phase/Task] ([Size]): [Description] - [Estimate]
- [Phase/Task] ([Size]): [Description] - [Estimate]

Dependencies: [List any blockers]

## Monitoring & Rollback
- Feature flag: [Flag name and strategy]
- Key metrics: [What to monitor]
- Rollback: [How to disable if issues arise]
```

## Red Flags: Your TRD Needs Simplification When...

1. 📛 You're listing pros/cons without decisions
2. 📛 It duplicates content from the PRD
3. 📛 Full API specs are included
4. 📛 Database schemas show every field
5. 📛 No clear "how to build this" emerges
6. 📛 The document exceeds 3 pages
7. 📛 External documentation is copy-pasted

## Remember

The TRD should enable a developer to start implementation immediately. It's about **HOW** to build what the PRD defined.

**Your TRD should answer:**

- HOW will we build it?
- WHAT technical decisions were made?
- WHAT are the risks?
- HOW do we roll back if needed?

Keep it focused on decisions and implementation guidance, not exploration of options.
