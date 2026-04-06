# Specification: Task Timer

## Feature Number
001-task-timer

## Problem Statement
Developers often lose track of how long they spend on individual tasks. A simple
CLI timer would let them start, stop, and review time spent per task, helping
them plan better and identify where time is being spent.

## User Stories
- As a developer, I want to start a timer for a named task so that I can track
  how long it takes.
- As a developer, I want to stop the timer and see the elapsed time so that I
  can log my work.
- As a developer, I want to view a summary of all tracked tasks so that I can
  understand my time allocation.

## Functional Requirements
- REQ-001: The system must allow starting a timer with a task name.
- REQ-002: The system must allow stopping the active timer and displaying elapsed time.
- REQ-003: The system must persist timer data across sessions.
- REQ-004: The system must display a summary of all tasks with total time per task.
- REQ-005: The system must prevent starting a new timer when one is already active.

## Non-Functional Requirements
- REQ-NF-001: Timer data should be stored in a human-readable format.
- REQ-NF-002: The CLI should respond in under 100 milliseconds for all operations.

## Success Criteria
- [ ] A developer can start, stop, and review timers from the command line.
- [ ] Data persists between CLI invocations.
- [ ] Summary shows task names, durations, and totals.

## Edge Cases
- Starting a timer when one is already running should produce a clear error.
- Stopping when no timer is active should produce a clear error.
- Very long-running timers (hours or days) should display correctly.

## Open Questions
- [NEEDS CLARIFICATION] — Should the timer support pausing and resuming?
- [NEEDS CLARIFICATION] — Should there be a "report" export feature?

## Out of Scope
- GUI or web interface.
- Team-based time tracking.
- Integration with project management tools.

## Dependencies
- None. This is a standalone CLI tool.
