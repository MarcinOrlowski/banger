# How to Create a Compact PRD (Product Requirements Document)

## Core Principle

**If your PRD is getting too long, your scope is too big.** Break it down into smaller, iterative
deliverables.

## Target Length & Format

- **Maximum length**: 1-2 pages
- **Format**: Markdown or simple document
- **Rule**: If you can't explain the core value on one page, simplify the scope

## Required Sections

### 1. Problem Statement (2-3 sentences)

```markdown
## Problem Statement

- What specific problem are we solving?
- Who experiences this problem?
- What's the impact of not solving it?
```

**Example:**
> Users cannot track their daily water intake in our fitness app. Active users (65% of our base)
> manually log water consumption elsewhere. This leads to incomplete health data and 30% lower
> engagement with nutrition features.

### 2. Solution Overview (3-4 sentences)

```markdown
## Solution Overview

- Core functionality in plain language
- Key differentiator (if any)
- What success looks like
```

**Example:**
> Add a simple water tracking widget to the home screen that allows one-tap logging of water
> consumption. Unlike competitors, it will use smart reminders based on activity level. Success
> means
> 50% of active users log water at least once daily within 30 days.

### 3. User Stories (3-5 maximum)

```markdown
## User Stories

As a [user type], I want to [action], so that [outcome]
```

**Example:**

1. As an active user, I want to log water intake with one tap, so that I can track hydration without
   interrupting my day
2. As a fitness enthusiast, I want to see my hydration vs. activity level, so that I can optimize my
   performance
3. As a user, I want to receive smart reminders, so that I maintain healthy hydration habits

### 4. Acceptance Criteria (5-7 bullet points)

```markdown
## Acceptance Criteria

- Measurable, testable conditions
- Focus on WHAT, not HOW
```

**Example:**

- User can log water intake in under 3 seconds
- System tracks daily, weekly, and monthly intake
- Reminders adjust based on logged activity level
- Data syncs with existing nutrition dashboard
- Widget is accessible from home screen without additional navigation

### 5. Out of Scope (Critical!)

```markdown
## Out of Scope

- Explicitly list what this iteration does NOT include
```

**Example:**

- Custom beverage types (only water for v1)
- Integration with smart water bottles
- Detailed hydration analytics
- Social sharing features
- Apple Watch/wearable integration

### 6. Success Metrics (2-3 KPIs)

```markdown
## Success Metrics

- Quantifiable measures tied to problem statement
```

**Example:**

- 50% of active users log water at least once daily
- 25% increase in nutrition feature engagement
- Average logging time under 3 seconds

## Writing Best Practices

### DO:

- ✅ Use simple, jargon-free language
- ✅ Be specific about constraints (time, budget, technical)
- ✅ Include "Done when" statements
- ✅ Keep user benefit front and center
- ✅ Make acceptance criteria testable

### DON'T:

- ❌ Include implementation details (save for TRD)
- ❌ Use technical architecture terms
- ❌ Create nested bullet points in criteria
- ❌ Write vague success metrics
- ❌ Assume context - be explicit

## Quick Quality Checklist

Before finalizing your PRD, ensure:

- [ ] A non-technical stakeholder can understand it completely
- [ ] The scope is achievable in one sprint/iteration
- [ ] Success criteria are measurable and time-bound
- [ ] "Out of scope" section exists and is clear
- [ ] Total length is under 2 pages
- [ ] No technical implementation details are included

## PRD Template

```markdown
# [Feature Name] PRD

**Ticket**: [Link to github ticket]

## Problem Statement

[2-3 sentences maximum]

## Solution Overview

[3-4 sentences maximum]

## User Stories

1. As a..., I want to..., so that...
2. As a..., I want to..., so that...
3. As a..., I want to..., so that...

## Acceptance Criteria

- [ ] [Specific, measurable criterion]
- [ ] [Specific, measurable criterion]
- [ ] [Specific, measurable criterion]
- [ ] [Specific, measurable criterion]
- [ ] [Specific, measurable criterion]

## Out of Scope

- [Feature/functionality not included]
- [Feature/functionality not included]
- [Feature/functionality not included]

## Success Metrics

1. [Metric + target + timeframe]
2. [Metric + target + timeframe]
3. [Metric + target + timeframe]
```

## Red Flags: Your PRD Needs Simplification When...

1. 📛 You have more than 5 user stories
2. 📛 Your acceptance criteria have sub-bullets
3. 📛 Technical details are creeping in
4. 📛 You're solving multiple problems
5. 📛 Success metrics are vague or unmeasurable
6. 📛 The document exceeds 2 pages
7. 📛 You need extensive context to understand it

## Remember

The goal is **clear communication that enables rapid delivery**, not comprehensive documentation.
When in doubt, cut it out. You can always add detail in the next iteration.

**Your PRD should answer:**

- WHAT are we building?
- WHO is it for?
- WHY does it matter?
- WHEN is it done?

Save the HOW for the Technical Requirements Document (TRD).
