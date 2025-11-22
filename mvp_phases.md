# MVP Build Phases for AI Flow State Facilitator

This document outlines the phased approach to building the MVP of the AI Flow State Facilitator, based on the provided documentation. The project is broken down into logical phases that build upon each other, ensuring a structured development process from planning to pilot testing.

## Phase 1: Requirements Analysis and Design
**Objective:** Finalize all specifications, designs, and contracts before coding begins.

### Sub-tasks:
- [ ] Review and finalize flow detection thresholds and parameters
- [ ] Create UX copy and design mockups for tray menu and dashboard
- [ ] Define macOS permission prompts and user-facing texts
- [ ] Prepare Chrome extension manifest specification
- [ ] Define database schema and API contracts between Agent ↔ Dashboard ↔ Extension
- [ ] Create sequence diagrams for event flows
- [ ] Document privacy policy and security requirements
- [ ] Prepare onboarding documentation with screenshots

**Deliverables:** Complete design specs, mockups, and technical contracts.

## Phase 2: Infrastructure Setup
**Objective:** Establish the development environment and local infrastructure.

### Sub-tasks:
- [ ] Set up local Supabase environment (Docker Compose)
- [ ] Create and apply database migrations
- [ ] Configure local development ports and credentials
- [ ] Set up project repository structure
- [ ] Initialize CI/CD pipelines (GitHub Actions)
- [ ] Prepare development scripts (start-local.sh, reset-db.sh)

**Deliverables:** Working local Supabase instance with schema applied.

## Phase 3: Agent Core Development
**Objective:** Build the macOS background agent with event collection and flow detection.

### Sub-tasks:
- [ ] Implement input collector (keyboard, mouse, app switches)
- [ ] Build rolling metrics engine for typing rate, app switches, idle gaps
- [ ] Develop flow rule engine with configurable thresholds
- [ ] Implement protection controller (DND toggle, extension messaging)
- [ ] Add persistence layer for Supabase integration
- [ ] Create local API for dashboard communication
- [ ] Implement tray/menu UI for status and controls
- [ ] Add logging and error handling

**Deliverables:** Functional agent that can detect flow states and toggle protections.

## Phase 4: Chrome Extension Development
**Objective:** Create the browser helper for distraction blocking.

### Sub-tasks:
- [ ] Set up Chrome extension manifest (v3)
- [ ] Implement native messaging host for agent communication
- [ ] Build domain blocking logic
- [ ] Add whitelist/blacklist management
- [ ] Create extension UI for settings
- [ ] Implement fallback communication methods if needed

**Deliverables:** Installable Chrome extension that responds to agent commands.

## Phase 5: Dashboard Development
**Objective:** Build the local web interface for analytics and settings.

### Sub-tasks:
- [ ] Set up dashboard framework (React/Vue with local server)
- [ ] Implement session list and timeline views
- [ ] Add settings page for thresholds and lists
- [ ] Integrate Supabase client for data queries
- [ ] Build export functionality (CSV)
- [ ] Add real-time updates via Supabase Realtime
- [ ] Implement authentication/security measures

**Deliverables:** Functional local dashboard accessible via browser.

## Phase 6: Integration and Testing
**Objective:** Connect all components and validate functionality.

### Sub-tasks:
- [ ] Integrate agent ↔ extension messaging
- [ ] Connect dashboard ↔ agent API
- [ ] Implement end-to-end data flow
- [ ] Run unit tests for all components
- [ ] Execute integration tests
- [ ] Perform manual QA against acceptance test checklist
- [ ] Test permission handling and error states
- [ ] Validate performance metrics (CPU/memory usage)

**Deliverables:** Fully integrated system passing all acceptance tests.

## Phase 7: Packaging and Documentation
**Objective:** Prepare the MVP for distribution to pilot users.

### Sub-tasks:
- [ ] Create signed macOS app bundle
- [ ] Package Chrome extension for distribution
- [ ] Build installer with onboarding flow
- [ ] Create user installation instructions
- [ ] Document troubleshooting and FAQ
- [ ] Prepare pilot feedback collection mechanism

**Deliverables:** Installable MVP package with complete documentation.

## Phase 8: Pilot Testing and Iteration
**Objective:** Deploy to initial users and gather feedback for improvements.

### Sub-tasks:
- [ ] Onboard 5 pilot users
- [ ] Monitor usage and collect feedback
- [ ] Track success metrics (adoption, false positives)
- [ ] Identify and prioritize issues
- [ ] Implement critical fixes
- [ ] Prepare final MVP release notes

**Deliverables:** Validated MVP ready for broader testing.

## Risk Mitigation Throughout Phases
- **Accessibility Permission Issues:** Include clear onboarding and retry mechanisms
- **Chrome Extension Reliability:** Implement fallback communication methods
- **False Positives:** Use conservative thresholds with easy overrides
- **OS Compatibility:** Test on multiple macOS versions during QA
- **Data Privacy:** Ensure all data remains local with user controls

## Success Criteria
- Functional: 9/10 simulated sessions correctly detect flow and toggle protections
- Reliability: Agent runs with <5% CPU impact
- UX: Users report appropriate triggering and easy overrides
- Adoption: >50% of pilot users use app daily during testing week

## Dependencies and Prerequisites
- macOS development environment
- Docker for Supabase local
- Chrome browser for extension testing
- Apple Developer account for code signing (later phases)
- GitHub repository for CI/CD

This phased approach ensures systematic development while allowing for parallel work on independent components like the agent, extension, and dashboard.
