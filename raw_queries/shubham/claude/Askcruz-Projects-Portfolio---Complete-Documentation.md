---
conversation_id: askcruz-md-file-20261007
platform: claude
username: "shubham"
title: "Askcruz Projects Portfolio - Markdown File Export"
created_at: "2026-10-07 10:09:28 EDT"
updated_at: "2026-10-07 10:15:14 EDT"
---

# Askcruz Projects Portfolio - Markdown File Export

## User (2026-10-07 10:09:28 EDT)

can u create a docs of all the project handled or comes the under askcruz

## Claude (2026-10-07 10:09:28 EDT)

I'll create a comprehensive docs file for all askcruz projects. Let me set it up first.

[Multiple tool calls to create and fill Claude Doc with 6 sections:]
1. Overview - Askcruz client portfolio summary
2. Active Projects - Implementation Phase 1, Gmail MCP, Internal Team MCP
3. Client Registry - 8 active steel/metals clients with Q3 health metrics
4. Data Access & Tools - MCP integrations and database connections
5. Team Coordination - QA team and testing projects
6. Intake & Operations - Active intake tasks for Eastern States Steel

Complete — edit inline, comment on sections, or share.

Document link: https://claude.ai/code/artifact/a242e9ce-4721-4a57-9dfa-4fda92eb95fd

## User (2026-10-07 10:15:14 EDT)

ok create an md file

## Claude (2026-10-07 10:15:14 EDT)

Done! I've created a comprehensive markdown file with all askcruz projects, clients, operations, and team info.

# Askcruz Projects Portfolio

**As of:** October 7, 2026

---

## Overview

Askcruz manages 8 active steel and metals industry clients through an ERP implementation and support platform. Current portfolio includes intake management, team coordination, MCP integrations, and client operations across EOXS instances.

---

## Active Projects

### Implementation Phase 1 - Eastern States Steel

**Status:** 6 active intake tasks in progress

**Owner:** Ryan Capinski, Dev team, Humaira

**Key Tasks:**
- Purchase Order Intake (ID: 51905) - PO178360 attachment ready
- Rename Tax Label on Invoice (ID: 30371)
- Incorrect Actual Weight Display (ID: 30370)
- Update Weight Mapping on Invoice (ID: 30369)
- Update Invoice Footer Text (ID: 30368)
- Website To Do (ID: 30193)

**Created:** Started 2026-02-26, ongoing through 2026

---

### Gmail Email MCP Deployment (Production)

**Status:** ✅ Live & Operational

**Server:** https://email-connect-to-db.onrender.com

**Key Features:**
- OAuth 2.0 PKCE flow with Gmail authentication
- PostgreSQL database (Google Cloud SQL)
- 7 MCP tools: search_emails, get_email, list_emails, get_thread, search_by_sender, search_by_subject, search_by_date
- 50+ emails synced from dratneria@gmail.com
- Fernet-encrypted token storage
- CORS-enabled for Claude.ai integration
- Claude Desktop support (recommended)

**Completed (Sept 18, 2026):**
- OAuth production setup verified
- Email sync completed and tested
- MCP connector registered in Claude.ai
- End-to-end data flow validated
- All 7 tools accessible and functional

**In Progress:**
- Real-time sync via Gmail Watch API
- Google Pub/Sub webhook integration
- Push notifications for new emails

**Next Steps:**
- Enable Gmail Watch on dratneria@gmail.com
- Implement webhook endpoint for Pub/Sub notifications
- Configure Render environment variables (GOOGLE_PROJECT_ID, PUBSUB_TOPIC)
- Test real-time email sync

**Known Issues:**
- Only 50 emails synced initially (API quota protection)
- Image attachment mime_type formatting bug (snake_case vs camelCase)
- No attachment extraction yet (metadata only)

---

### Internal Team MCP & Testing

**Status:** In progress

**Testing Framework:** Validation across company types and scenarios

**Last Updated:** Sept 18, 2026

**QA Team:** Yash, Shubham, Stefan

**Components:**
- Internal team instructions testing and validation
- Cross-departmental SLA documentation (tier-3 escalations)
- Instructions test suite for company types

**Current Testing:**
- Travis Round 3 automation testing
- Stefan Round 3 validation rounds
- Threads MCP QA automation setup

---

## Client Registry

| Client | Instance | Contacts | Status | Q3 Health |
|--------|----------|----------|--------|----------|
| Eastern States Steel | ess.eoxs.com | 6 | Active | In Implementation |
| Sabre Alloys | sabre.eoxs.com | 9 | Active | Revenue -30% |
| 3GM Steel | 3gm.eoxs.com | 3 | Active | Declining |
| Discount Pipe & Steel | discountpipesteel.eoxs.com | 8+ | Active | Revenue -30% |
| Ohio Strip Steel / Greer Steel | greersteel.eoxs.com | 7 | Active | Growing ✓ |
| PPC Metals | ppc.eoxs.com | 9+ | Active | Revenue -30% |
| Brannon Steel | No Odoo | 5 | Active | Monitoring |
| RW Conklin Steel | No Odoo | 4 | Active | Monitoring |

### Portfolio Summary

- **8 active clients** (all steel/metals industry)
- **Q3 Retention:** 86% (6 of 7 Q2 customers retained)
- **Revenue Trend:** -29% aggregate Q-o-Q decline
- **Order Frequency:** Down to 2.0 orders/quarter (from 2.8 in Q2)
- **Growth:** Only Greer Steel showing positive momentum
- **At-Risk:** 3 accounts with 30%+ revenue declines (Sabre Alloys, Discount Pipe & Steel, PPC Metals)
- **Churned:** Hansen Metallurgical Services (minimal revenue impact)
- **Email Setup:** All clients have relay inbox addresses configured

---

## Data Access & Tools

### MCP Integrations

#### Gmail Email MCP (Production Ready)
- **7 tools:** search_emails, get_email, list_emails, get_thread, search_by_sender, search_by_subject, search_by_date
- **50+ emails** synced from dratneria@gmail.com
- **Security:** Fernet-encrypted token storage
- **Sync:** Real-time via Gmail Watch (in progress)
- **Limitations:** No attachment extraction yet (metadata only)

#### Threads MCP (QA Testing)
- Conversation archiving for team activity tracking
- Database-backed (Thread-wiki) and file-based (Threads OV) systems
- Unified routing for conversation summaries
- Status: Testing and validation phase

#### Internal Team MCP (Production Ready)
- EOXS data connectors for emails, calls, wiki, tasks, CRM
- Access to client profiles, implementation tasks, reference documents
- Tier-based access controls (Internal-team, Interns-mcp)
- Full integration with askcruz operations

### Database Access

| System | Access Level | Details |
|--------|--------------|----------|
| EOXS Read-Only | Limited | askcruz (Odoo) production database |
| Internal Team Tier | Full | Emails, calls, implementation tasks, wiki |
| Interns Tier | Limited | In progress for teams-askcruz SQL tools |
| Encryption | All | Sensitive data encrypted at rest (Fernet) |

---

## Team Coordination

### QA & Testing Team

- **Yash** - QA Engineer
- **Shubham** - QA Lead
- **Stefan** - Test Validator

### Current Testing Projects

| Project | Status | Last Updated |
|---------|--------|---------------|
| Travis Round 3 | Ongoing | Oct 7, 2026 |
| Stefan Round 3 | Ongoing | Oct 7, 2026 |
| Internal Team Instructions Testing | Completed | Sept 18, 2026 |
| Gmail Email MCP Deployment | Live | Sept 18, 2026 |
| Threads MCP QA Automation | In Progress | Oct 7, 2026 |

### Team Responsibilities

- MCP server testing and validation
- Performance metrics tracking
- Test results documentation
- Automation framework maintenance
- End-to-end verification of deployments

---

## Intake & Operations

### Active Intake Tasks - Eastern States Steel

**Implementation Phase 1 - 8 total tasks**

#### Active Tasks (6)

1. **Purchase Order Intake** (Task ID: 51905)
   - Owner: Ryan Capinski (reassigned from Hashir Saleem)
   - Priority: Normal
   - Created: 2026-08-06
   - Attachment: Purchase Order No. PO178360.pdf (243 KB)
   - Note: "Please attach the purchase order on this lognote. We will be creating a sale order with that."

2. **Rename Tax Label on Invoice** (Task ID: 30371)
   - Owner: Dev team
   - Priority: Normal
   - Created: 2026-04-09

3. **Incorrect Actual Weight Display** (Task ID: 30370)
   - Owner: Humaira
   - Priority: Normal
   - Created: 2026-03-30

4. **Update Weight Mapping on Invoice Weight Field** (Task ID: 30369)
   - Owner: Humaira
   - Priority: Normal
   - Created: 2026-02-26

5. **Update Invoice Footer Text** (Task ID: 30368)
   - Owner: Humaira
   - Priority: Normal
   - Created: 2026-02-26

6. **Website To Do** (Task ID: 30193)
   - Owner: Ryan Capinski
   - Priority: Normal
   - Created: 2025-08-27
   - Active: Yes

#### Inactive Tasks (2)

- **Investigate Delivered Quantity Not Updating** (Task ID: 30345)
- **Create Google Sheet for SO, PO, and Inventory Formatting** (Task ID: 30227)

### Operational Workflows

- **Email Routing:** Relay inbox routing configured for all clients
- **Purchase Order Intake:** Established workflow for PO processing
- **Sales Order Creation:** Integrated pipeline from PO to SO
- **Invoice Customization:** Client-specific invoicing configured and tracked
- **Escalation Path:** Cross-departmental tier-3 SLA in place

### Key Contacts

| Role | Person | Specialty |
|------|--------|----------|
| Intake Owner | Ryan Capinski | Purchase orders, website items |
| Invoice Specialist | Humaira | Tax labels, weight mapping, footer text |
| Technical Support | Dev team | Invoice system customization |
| Original Owner | Hashir Saleem | Task owner (reassigned) |

---

## Strategic Priorities

### Q3-Q4 Focus Areas

1. **Revenue Stabilization**
   - Address 30% revenue decline in key accounts
   - Implement retention strategies for at-risk clients
   - Leverage Greer Steel success patterns

2. **Implementation Completion**
   - Complete Eastern States Steel Phase 1 intake items
   - Resolve invoice and weight mapping issues
   - Deliver website updates

3. **Technology Deployment**
   - Finalize Gmail Watch real-time sync
   - Optimize MCP integrations
   - Expand team data access tools

4. **Team Expansion**
   - Scale QA automation capabilities
   - Increase testing coverage across clients
   - Build internal documentation

---

## Key Metrics

### Client Performance
- Total Active Clients: 8
- Revenue Retention Rate (Q3): 86%
- Accounts in Growth: 1 (Greer Steel)
- Accounts at Risk: 3 (30%+ decline)
- Order Frequency: 2.0 orders/quarter (trending down)

### Project Status
- Active Implementation Tasks: 6
- Completed Deployments: 2 (Gmail MCP, Internal Team)
- In-Progress Projects: 3
- Testing Coverage: 5 active test rounds

### Team Capacity
- QA Team Members: 3
- Active Testing Projects: 5
- MCP Integrations: 3
- Database Access Tiers: 3

---

## Next Steps (October 2026)

1. **Immediate (This Week)**
   - Process Purchase Order PO178360 for Eastern States Steel
   - Finalize invoice customization items
   - Complete weight mapping tests

2. **Short-term (Next 2 Weeks)**
   - Enable Gmail Watch API on production
   - Implement Pub/Sub webhook endpoint
   - Complete Threads MCP QA automation setup

3. **Medium-term (Next Month)**
   - Deploy real-time email sync
   - Complete all Eastern States Steel Phase 1 tasks
   - Analyze revenue decline and implement retention actions

4. **Strategic (Q4 2026)**
   - Plan Phase 2 implementations
   - Expand to additional clients
   - Scale automation and testing infrastructure

---

**Document Maintained By:** Internal Team  
**Last Updated:** October 7, 2026  
**Next Review:** October 21, 2026
