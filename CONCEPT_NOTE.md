---
title: Origami FarmOS Concept Note
document: CONCEPT_NOTE
version: 0.1
status: Concept Note
primary_use: Internal product definition, GitHub repository baseline, Codex implementation context
prepared_for: Origami Farms
prepared_by: Product Owner and Chief Software Architect collaboration
---

# Origami FarmOS Concept Note

## The Intelligent Operating System for Origami Farms

## 1. Executive Summary

Origami FarmOS is an offline-first, tablet-first digital operating system designed to manage the daily operations, production, health, inventory, finance, and decision-making needs of Origami Farms.

The first objective is not to build a generic commercial farm management application. The first objective is to build a practical system that solves real operational problems at Origami Farms. The system will be tested, refined, and validated through daily use on the farm before being prepared for commercial release to other farms.

FarmOS is based on a simple but powerful philosophy:

> FarmOS helps farmers make better decisions with less effort.

Unlike traditional farm management software that primarily stores records, FarmOS is designed as a knowledge-driven platform. It captures observations from workers, production data from daily activities, health records, feeding information, inventory movements, sales, expenses, and farm events. It then transforms this information into evidence-based insights and recommendations for the farm manager.

The system will support the current needs of Origami Farms, including cows, sheep, goats, chickens, ducks, turkeys, horses, fresh produce, milk production, egg production, feed management, veterinary records, inventory, sales, and costs.

The long-term ambition is to evolve FarmOS into a commercial product that can support other mixed farms. However, commercialization will only happen after the product has been proven through real use at Origami Farms.

## 2. Background and Rationale

Modern farms generate large amounts of information every day. Workers feed animals, collect eggs, milk cows, observe animal health, apply treatments, harvest produce, record sales, purchase feed, and manage inventory. Much of this knowledge is either recorded manually, kept in notebooks, stored in disconnected spreadsheets, or remembered by experienced workers.

This creates several challenges:

- The farm manager relies heavily on verbal feedback from workers.
- Important observations may be forgotten or recorded inconsistently.
- Animal health decisions may become subjective.
- Feed consumption is difficult to connect to production and profitability.
- Milk and egg production trends are not always analyzed early enough.
- Medical history may not be easily available when needed.
- Inventory shortages may be discovered too late.
- Farm knowledge is lost when experienced workers leave.
- Financial performance is difficult to understand at animal, flock, crop, or product level.

FarmOS responds to these challenges by creating a structured digital memory of the farm.

The system does not simply ask users to enter data. Instead, it helps users capture reality in the simplest possible way. Workers record observations and completed work. FarmOS organizes the information, detects patterns, generates alerts, and supports the farm manager with evidence-based recommendations.

The system is designed around real farm workflows, not around software modules. The guiding question is:

> What does the farm manager need to know and do tomorrow morning?

## 3. Product Vision

Origami FarmOS will become the digital operating system of Origami Farms.

It will help the farm manager answer questions such as:

- Which animals need attention today?
- Which cows have declining milk production?
- Which flock is underperforming in egg production?
- How much feed was consumed today?
- How many days of feed inventory remain?
- Which animal has repeated health issues?
- Which cows, goats, or sheep are ready for breeding?
- Which animals are profitable and which are not?
- Which crops or fresh produce generate the best margin?
- What should be done first this morning?
- Which recommendations require action?
- Which farm decisions were made, and what was the outcome?

FarmOS will not replace the farmer, the veterinarian, or the farm manager. It will support them.

The product philosophy is:

> FarmOS does not replace the farmer's experience. It amplifies it.

## 4. Core Product Principles

### 4.1 Build for Origami Farms First

The first version of FarmOS will be built for Origami Farms only. It should solve real problems on the farm before being generalized for other farms.

Every MVP feature must answer the question:

> Would this help run Origami Farms better tomorrow morning?

If the answer is no, the feature belongs in the roadmap, not the MVP.

### 4.2 Offline First

Farm operations cannot stop because internet connectivity is unavailable.

FarmOS must work fully offline for all critical workflows, including:

- Animal lookup
- Feeding
- Milk recording
- Egg collection
- Health observations
- Treatment records
- Inventory usage
- Task completion
- Sales and expenses

Internet connectivity should only be required for synchronization, cloud backup, remote access, and future integrations.

### 4.3 Tablet First

The primary device is an Android tablet used in the barn, stable, field, or storage area.

The user interface must support:

- Large buttons
- Minimal typing
- One-hand use
- Fast workflows
- QR code scanning
- Simple confirmations
- Offline saving
- Clear alerts
- Arabic and English support

The design principle is:

> If a worker cannot complete the task with one hand while standing in the barn, the design is wrong.

### 4.4 Workers Observe, Managers Decide

FarmOS separates observation from diagnosis.

Workers should record what they see, not what they think it means.

For example:

**Wrong:** Cow has mastitis.

**Correct:**

- Milk decreased.
- Udder swollen.
- Temperature elevated.
- Cow reluctant to be milked.

The system correlates the observations. The farm manager reviews the recommendation. The veterinarian confirms diagnosis and treatment.

This reduces subjective decision-making and improves consistency.

### 4.5 Evidence Before Opinion

Every recommendation must be supported by evidence.

FarmOS should never show a recommendation without explaining:

- What was observed
- Which trends were detected
- What historical context matters
- What confidence level is assigned
- What action is suggested
- What information is missing

This makes FarmOS trustworthy.

### 4.6 One Digital Twin per Object

Every physical object on the farm must have one digital representation.

This applies to:

- Animals
- Flocks
- Fields
- Barns
- Pens
- Products
- Feed items
- Medicines
- Assets
- Customers
- Suppliers

For example, Cow 744 must exist once. Milk records, feed records, medical records, breeding records, costs, photos, and recommendations all connect to the same digital twin.

### 4.7 Event-Driven History

FarmOS should not silently overwrite history.

Important farm activities are recorded as events, such as:

- Animal registered
- Feed distributed
- Milk recorded
- Eggs collected
- Treatment administered
- Vaccination completed
- Pregnancy confirmed
- Birth recorded
- Harvest completed
- Product sold
- Expense recorded

Corrections should be recorded as correction events rather than deleting history.

This supports auditability, offline synchronization, timelines, and AI reasoning.

### 4.8 AI Advises, Humans Decide

FarmOS intelligence is advisory.

It can recommend:

- Inspect this animal
- Schedule a veterinary check
- Review feed ration
- Monitor production
- Purchase feed soon
- Check withdrawal period
- Review low-performing animals

It must not:

- Diagnose disease as fact
- Prescribe medication
- Replace the veterinarian
- Automatically change records without approval
- Hide uncertainty
- Make recommendations without evidence

## 5. Problem Statement

Origami Farms needs a simple but intelligent system to manage mixed farm operations across livestock, poultry, fresh produce, inventory, sales, expenses, and animal health.

Current challenges include:

1. Daily activities are difficult to track consistently.
2. Worker feedback may be subjective or incomplete.
3. Animal health observations are not always correlated with production, feed, and history.
4. Feed cost is difficult to connect to milk, eggs, and profitability.
5. Milk and egg production trends are not automatically analyzed.
6. Veterinary history is not always structured for decision-making.
7. Inventory levels and shortages require manual tracking.
8. Produce costs and sales need better visibility.
9. The farm manager needs a daily briefing rather than static reports.
10. Farm knowledge should remain available even when people change.

FarmOS will address these issues by creating an integrated, knowledge-driven, offline-first operating system for the farm.

## 6. Proposed Solution

FarmOS will be developed as a digital platform that combines:

- Farm operations
- Animal digital twins
- Feeding records
- Production records
- Veterinary records
- Inventory management
- Fresh produce management
- Sales and expenses
- Task management
- Knowledge model
- Decision intelligence
- AI-assisted recommendations

The MVP will focus on the workflows that matter most to Origami Farms.

The system will start with the following priority workflows:

1. Morning briefing
2. Animal lookup and profile
3. Feeding
4. Milk production
5. Egg collection
6. Health observation
7. Treatment and vaccination
8. Feed inventory
9. Produce harvest
10. Sales and expenses
11. Basic reports
12. AI-supported alerts and recommendations

## 7. FarmOS as a Knowledge System

FarmOS is not only a system of record.

A traditional system of record stores information:

- Temperature = 39.7°C
- Milk = 24 L
- Feed = 18 kg

FarmOS turns information into understanding:

> Cow 744 has reduced milk production, reduced feed intake, elevated temperature, and a previous history of mastitis. FarmOS recommends veterinary inspection within 12 hours.

This is the central product differentiator.

FarmOS transforms:

> Observations → Information → Knowledge → Recommendations → Decisions → Outcomes → Learning

This creates a continuous knowledge feedback loop.

## 8. Knowledge Lifecycle

FarmOS knowledge evolves through the following lifecycle:

### 8.1 Reality

Reality is the actual state of the farm before it is observed.

FarmOS must never assume that missing data means everything is normal.

For example, "no temperature recorded" does not mean "temperature normal." It means the temperature is unknown.

### 8.2 Observation

Observation is the raw fact captured by a worker, manager, veterinarian, sensor, or external system.

Examples:

- Cow refused feed
- Milk decreased
- Temperature 39.6°C
- Duck flock produced 42 eggs
- Tomatoes showing yellow leaves
- Feed stock below minimum

Observations should be objective and structured.

### 8.3 Validation

FarmOS validates observations before using them for intelligence.

Validation includes:

- Required fields
- Valid timestamp
- Valid animal or flock
- Plausible biological values
- Duplicate detection
- Active status check
- Unit validation
- Offline sync validation

Invalid observations should be flagged, not silently deleted.

### 8.4 Information

Validated observations are organized into useful metrics.

Example:

- Expected feed intake: 24 kg
- Actual feed intake: 18 kg
- Difference: -25%

This is no longer raw data. It is structured information.

### 8.5 Knowledge

FarmOS correlates information from multiple sources.

Example:

- Milk decreased.
- Feed intake decreased.
- Temperature increased.
- Animal has previous mastitis history.

FarmOS can then generate knowledge: "Animal performance is declining and health risk is increasing."

### 8.6 Recommendation

A recommendation is a suggested action based on evidence.

Example:

> Schedule veterinary examination for Cow 744 today. Confidence: High. Reason: Milk production dropped 18%, feed intake dropped 12%, temperature increased, and cow has previous mastitis history.

### 8.7 Decision

The farm manager decides what to do.

Possible decisions:

- Accept
- Reject
- Monitor
- Delegate
- Escalate
- Postpone

Every decision is logged.

### 8.8 Action

The accepted decision becomes farm work.

Examples:

- Worker checks animal
- Veterinarian visits
- Feed ration adjusted
- Animal isolated
- Treatment administered
- Product withheld from sale

### 8.9 Outcome

FarmOS records what happened after the action.

Examples:

- Milk recovered
- Temperature normalized
- Vet confirmed diagnosis
- No issue found
- Recommendation was incorrect
- Animal deteriorated

### 8.10 Learning

FarmOS learns from outcomes.

Over time, the system becomes more adapted to Origami Farms.

It learns:

- How each animal behaves
- Which signs usually matter
- Which workers provide reliable observations
- Which interventions work best
- Which production changes indicate health risks
- Which recommendations are useful

## 9. Observation Model

Observations are the foundation of FarmOS intelligence.

The system must encourage objective observations and discourage vague subjective entries.

### 9.1 Observation Types

FarmOS should support:

- Quantitative observations
- Qualitative observations
- Binary observations
- Media observations
- Sensor observations
- Veterinary observations
- Production observations
- Environmental observations
- Financial observations

Examples:

- Quantitative: Milk = 28.5 L
- Qualitative: Appetite reduced
- Binary: Pregnant = Yes
- Media: Photo of swollen udder
- Sensor: Barn temperature = 31°C
- Veterinary: Vet visit completed
- Production: Eggs collected = 185
- Environmental: Soil dry
- Financial: Feed purchase = $450

### 9.2 Observation Quality Levels

FarmOS should classify observation quality.

| Level | Type | Example | Confidence |
|---|---|---|---|
| A | Instrument measured | Digital thermometer, scale, milk meter | Highest |
| B | Counted | Eggs collected, feed bags used | High |
| C | Human observed | Limping, reduced appetite | Medium |
| D | Opinion | Looks sick, seems weak | Low |

The system should guide users toward Level A, B, or C observations.

Level D observations are allowed but should not be used alone for high-confidence recommendations.

### 9.3 Observation Metadata

Every observation should include:

- Observation ID
- Farm ID
- Entity type
- Entity ID
- Observation type
- Value
- Unit
- Observer
- Timestamp
- Location
- Source
- Confidence
- Verification status
- Notes
- Attachments
- Sync status

### 9.4 Missing Observations

FarmOS should reason about missing data.

Examples:

- No milk entry for a lactating cow today
- No feed record for a herd
- No egg collection for a laying flock
- No health follow-up after treatment
- No inventory update after feed purchase

Missing expected observations should generate reminders or alerts.

## 10. Animal Digital Twin Concept

The Animal Digital Twin is the heart of FarmOS.

An animal is not just a record. It is a living digital representation of a real animal.

Each animal digital twin should include:

- Identity
- Species
- Breed
- Sex
- Age
- Location
- Photos
- QR code
- Health state
- Production history
- Feed history
- Medical history
- Breeding history
- Weight history
- Financial history
- Timeline
- Recommendations
- AI-generated insights

The system should answer:

> If this animal disappeared tomorrow, could another farm manager understand its life in under five minutes?

If yes, the Animal Digital Twin is successful.

## 11. MVP Scope

The first version of FarmOS will focus on practical daily use at Origami Farms.

### 11.1 Included in MVP

The MVP includes:

- Farm profile
- Barns and locations
- Animal registry
- Cow, sheep, goat, horse records
- Flock records for chickens, ducks, and turkeys
- Feed inventory
- Feed distribution
- Milk production
- Egg collection
- Health observations
- Treatment records
- Vaccination records
- Withdrawal period warnings
- Fresh produce harvest
- Product inventory
- Sales
- Expenses
- Customers
- Suppliers
- Morning briefing
- Basic dashboard
- Basic reports
- Offline operation
- Synchronization
- English and Arabic support
- Rule-based AI recommendations

### 11.2 MVP-Light Features

These may be included if they are easy to implement:

- Animal photos
- Document attachments
- Basic asset register
- Simple weather note
- Product processing such as cheese, labneh, yogurt, preserves
- QR code generation
- Basic export to Excel or PDF

### 11.3 Excluded from MVP

The MVP will not include:

- Full payroll
- Full accounting system
- IoT integration
- Smart collars
- Milk meter integration
- Satellite imagery
- Drone monitoring
- Marketplace
- Commercial SaaS billing
- Multi-country compliance
- Advanced machine learning
- Veterinary telemedicine
- Blockchain traceability

These features may be considered in later phases.

## 12. Key MVP Workflows

### 12.1 Morning Briefing

FarmOS should open with a morning briefing, not a static dashboard.

The briefing should show:

- Urgent animal health alerts
- Today's feeding tasks
- Expected milk production
- Expected egg collection
- Animals needing observation
- Vaccinations due
- Feed inventory warnings
- Produce harvest reminders
- Weather note
- Sales or delivery reminders

Primary action: **Start My Day**

### 12.2 Feeding Workflow

The feeding workflow should allow the worker to:

1. Select barn, herd, flock, or animal.
2. View planned ration.
3. Confirm feed delivered.
4. Adjust quantity if needed.
5. Record leftovers or refusals.
6. Save offline.
7. Deduct inventory automatically.
8. Allocate feed cost.
9. Update animal or flock timeline.
10. Trigger alerts for abnormal intake.

### 12.3 Milk Production Workflow

The milk workflow should support:

- Morning and evening milking
- Individual cow entry
- Group entry when needed
- Goat milk if enabled
- Milk quality status
- Milk destination: sale, processing, consumption, or waste
- Withdrawal period warning
- Production trend
- Cost per liter

### 12.4 Egg Collection Workflow

The egg workflow should support:

- Flock selection
- Species: chicken, duck, turkey
- Total eggs
- Broken eggs
- Sellable eggs
- Eggs consumed
- Eggs sold
- Eggs for hatching
- Egg inventory update
- Production percentage
- Feed conversion estimate

### 12.5 Health Observation Workflow

The health workflow should allow workers to record:

- Reduced appetite
- Limping
- Swelling
- Wound
- Coughing
- Nasal discharge
- Fever
- Low activity
- Abnormal milk
- Abnormal behavior
- Photo evidence
- Notes

The worker should not diagnose. FarmOS correlates observations and raises recommendations.

### 12.6 Treatment Workflow

The treatment workflow should support:

- Animal or flock
- Symptom
- Diagnosis, when entered by veterinarian or authorized user
- Medicine
- Dose
- Route
- Date
- Person responsible
- Withdrawal period
- Follow-up date
- Cost
- Notes
- Attachments

The system should automatically block or warn against selling milk, eggs, or meat during active withdrawal periods.

### 12.7 Produce Workflow

Fresh produce management should support:

- Field
- Crop
- Planting date
- Harvest date
- Harvest quantity
- Unit
- Waste quantity
- Input cost
- Labor cost
- Packaging cost
- Sales
- Inventory
- Profitability

### 12.8 Sales and Expenses Workflow

FarmOS should allow quick recording of:

- Milk sales
- Egg sales
- Animal sales
- Produce sales
- Cheese/labneh/preserved food sales
- Feed purchases
- Medicine purchases
- Vet expenses
- Fuel expenses
- Labor expenses
- Equipment expenses
- Other farm expenses

The goal is not full accounting in MVP. The goal is decision-grade profitability.

## 13. User Roles

FarmOS should support role-based permissions.

### 13.1 Farm Owner

Can access everything.

Responsibilities: configure farm, review reports, approve recommendations, review financial performance, manage users, export data.

### 13.2 Farm Manager

Can manage daily operations.

Responsibilities: review morning briefing, assign tasks, validate observations, review alerts, approve actions, monitor performance.

### 13.3 Worker

Can complete assigned work and record observations.

Responsibilities: feed animals, milk cows, collect eggs, record observations, complete tasks, capture photos, report issues.

Worker cannot diagnose diseases unless authorized.

### 13.4 Veterinarian

Can access health records.

Responsibilities: review animal history, record diagnosis, prescribe treatment, confirm recovery, define withdrawal period, add veterinary notes.

### 13.5 Accountant / Finance User

Can access sales, expenses, customers, suppliers, and financial reports.

### 13.6 Read-Only User

Can view selected records and reports without editing.

## 14. Technical Concept

The preferred architecture is a GitHub-based product engineering repository supported by AI-assisted development.

The product should be built as an offline-first application using a modern architecture.

Recommended technical direction:

- Frontend: Flutter or another cross-platform framework
- Mobile target: Android tablet
- Desktop/laptop access: Windows app, web/PWA, or BlueStacks
- Backend: FastAPI or similar API framework
- Local database: SQLite
- Central database: PostgreSQL
- Synchronization: event-based sync queue
- API documentation: OpenAPI
- Documentation: Markdown
- Diagrams: Mermaid or PlantUML
- Repository: GitHub
- Implementation support: Codex

The exact technical stack can be refined, but the architecture must preserve the following:

- Offline-first operation
- Local data capture
- Event-driven history
- Sync when online
- Role-based access
- Bilingual interface
- Audit trail
- Exportable data
- Modular future expansion

## 15. GitHub Repository Concept

The GitHub repository should become the single source of truth for product, architecture, documentation, and code.

Recommended repository name: `origami-farmos`

Recommended structure:

```
origami-farmos/
├── README.md
├── CONSTITUTION.md
├── CONCEPT_NOTE.md
├── handbook/
│   ├── SUMMARY.md
│   ├── 01-Vision.md
│   ├── 02-Ontology.md
│   ├── 03-Behavioral-Model.md
│   ├── 04-Knowledge-Model/
│   │   ├── 04.1-Purpose.md
│   │   ├── 04.2-Knowledge-Lifecycle.md
│   │   ├── 04.3-Observation-Model.md
│   │   └── diagrams/
│   ├── 05-Animal-Digital-Twin/
│   ├── 06-Operational-Workflows/
│   ├── adr/
│   ├── glossary/
│   └── references/
├── product/
│   ├── MVP_SCOPE.md
│   ├── ROADMAP.md
│   ├── RELEASES.md
│   └── TRACEABILITY.md
├── design-system/
├── ui/
├── api/
├── database/
├── backend/
├── mobile/
├── tests/
└── docs/
```

> Implementation note: the handbook has since been expanded beyond this initial sketch. `06-Operational-Workflows` was split into one chapter per domain (Feed, Dairy, Poultry, Veterinary, Inventory, Produce, Sales & Finance) and chapters 13-19 cover UI/UX, database, API, sync, security, testing, and deployment architecture. See [handbook/SUMMARY.md](handbook/SUMMARY.md) for the current structure.

## 16. FarmOS Constitution

The repository should include a file called `CONSTITUTION.md`. This file defines the non-negotiable principles of FarmOS.

Initial constitution:

- FarmOS is built for Origami Farms first.
- FarmOS is offline first.
- FarmOS is tablet first.
- Workers record observations.
- Workers do not diagnose.
- Farm managers decide.
- Veterinarians diagnose and prescribe.
- AI explains.
- AI never replaces professional judgement.
- Every recommendation requires evidence.
- Every recommendation has confidence.
- Every object has one digital twin.
- Every important change is an event.
- History is never silently deleted.
- The system must reduce effort, not increase it.
- If a worker cannot use it in the barn, the design is wrong.

> See [CONSTITUTION.md](CONSTITUTION.md) for the ratified version.

## 17. Design and UX Concept

FarmOS should feel simple, even though it manages complex operations.

The user interface should follow these principles:

- Morning briefing first
- Task-driven navigation
- Large cards
- Large buttons
- Minimal typing
- QR-first lookup
- Quick actions
- Offline status visible
- Clear alerts
- Timeline-based history
- Arabic and English support
- Right-to-left support for Arabic
- Dark/light mode later
- Simple colors and icons

Common quick actions: Feed, Milk, Collect Eggs, Observe, Treat, Vaccinate, Move, Sell, Harvest, Record Expense.

The system should not feel like a spreadsheet. It should feel like a farm assistant.

## 18. Reporting Concept

FarmOS reports should be practical and decision-oriented.

MVP reports include:

- Daily milk production
- Weekly milk trend
- Milk per cow
- Egg production by flock
- Feed consumed
- Feed cost
- Feed stock remaining
- Animal health alerts
- Treatment history
- Withdrawal periods
- Produce harvest
- Sales by product
- Expenses by category
- Profitability summary

Future reports include:

- Cost per liter
- Cost per egg
- Profit per animal
- Profit per flock
- Profit per crop
- Breeding performance
- Veterinary cost trend
- Worker productivity
- AI recommendation accuracy
- Knowledge maturity index

## 19. Decision Intelligence Concept

FarmOS should generate periodic intelligence reviews.

### 19.1 Daily Review

Focus: What needs attention today?

Examples: cow with production drop, feed stock below threshold, flock with egg decline, vaccination due, active withdrawal period, harvest due.

### 19.2 Weekly Review

Focus: What trends are emerging?

Examples: milk trend, egg trend, feed efficiency, repeated health issues, inventory consumption, sales performance.

### 19.3 Monthly Review

Focus: What management decisions are needed?

Examples: low-performing animals, high-cost feed, veterinary expenses, product profitability, crop profitability, supplier performance.

### 19.4 Quarterly Review

Focus: What strategic changes are needed?

Examples: breeding strategy, cull candidates, feed sourcing, crop planning, investment priorities, commercial readiness.

## 20. Expected Benefits

### 20.1 Operational Benefits

Better daily task coordination, faster data capture, less paperwork, reduced duplicate work, improved follow-up, better worker accountability.

### 20.2 Animal Health Benefits

Earlier detection of health issues, better medical history, reduced subjective diagnosis, better treatment follow-up, withdrawal period control, improved veterinary decision support.

### 20.3 Production Benefits

Better milk tracking, better egg tracking, detection of production drops, feed-to-production analysis, improved productivity monitoring.

### 20.4 Financial Benefits

Better cost tracking, better revenue tracking, feed cost visibility, product profitability, animal and flock profitability, better purchasing decisions.

### 20.5 Knowledge Benefits

Farm memory preserved, worker observations structured, AI recommendations improved over time, better decisions based on evidence, reduced dependence on verbal feedback alone.

## 21. Risks and Mitigation

**Risk 1: Scope Creep**
Mitigation: use MVP scope document, apply product decision matrix, move non-essential features to roadmap.

**Risk 2: Workers Do Not Use the System**
Mitigation: design for one-hand use, minimize typing, use quick actions, start with only high-value workflows.

**Risk 3: Poor Data Quality**
Mitigation: use structured observation templates, validate entries, encourage objective observations, use confidence scoring.

**Risk 4: AI Recommendations Are Not Trusted**
Mitigation: explain every recommendation, show evidence, show confidence, allow manager feedback, never hide uncertainty.

**Risk 5: Offline Sync Conflicts**
Mitigation: use event-based sync, preserve local timestamps, flag conflicts for review, avoid silent overwrites.

**Risk 6: Product Becomes Too Complex**
Mitigation: morning briefing as main entry point, workflow-first navigation, hide advanced screens from workers, keep MVP focused on daily farm use.

## 22. Implementation Roadmap

**Phase 0: Engineering Repository Setup** — GitHub repository, constitution, concept note, engineering handbook structure, ADR folder, MVP scope, roadmap, initial glossary.

**Phase 1: Core Farm Setup** — Farm profile, users and roles, locations, basic offline database, language structure, initial sync architecture.

**Phase 2: Animal and Flock Foundation** — Animal registry, flock registry, QR code support, animal profile, timeline, basic health status.

**Phase 3: Morning Routine MVP** — Morning briefing, feeding workflow, milk workflow, egg workflow, observation workflow, task completion.

**Phase 4: Health and Veterinary** — Medical records, treatments, vaccinations, withdrawal periods, health recommendations, follow-up reminders.

**Phase 5: Inventory, Produce, Sales, Expenses** — Feed stock, medicine stock, product inventory, fresh produce harvest, simple sales, simple expenses, basic profitability.

**Phase 6: Intelligence and Reports** — Rule-based alerts, health recommendations, feed shortage forecast, production trends, daily/weekly/monthly reports, recommendation feedback loop.

**Phase 7: Origami Farms Pilot** — Daily use on farm, worker feedback, bug fixing, workflow refinement, feature removal where unused, MVP stabilization.

**Phase 8: Commercial Readiness** — Multi-farm support, onboarding flow, farm templates, subscription model, customer support model, commercial documentation.

> See [product/ROADMAP.md](product/ROADMAP.md) for the tracked, phase-by-phase engineering roadmap derived from this plan.

## 23. Definition of Success

FarmOS MVP is successful when:

- The farm manager uses it daily.
- Workers can complete core tasks without heavy training.
- Morning briefing becomes useful.
- Feed, milk, eggs, health, produce, sales, and expenses are captured consistently.
- Animal health alerts are more evidence-based.
- The system reduces reliance on memory and verbal feedback.
- The farm manager can see production and cost trends clearly.
- The product is useful enough that another farm would want it.

The strongest success indicator is:

> Origami Farms would continue using FarmOS even if it were not intended for commercialization.

## 24. Conclusion

Origami FarmOS is not simply a farm management application.

It is an intelligent operating system for a mixed farm.

It is designed to help Origami Farms run daily operations, preserve institutional memory, improve animal health, track production, manage costs, and support better decisions.

The MVP will remain focused on the real needs of Origami Farms. Only after the product proves its value internally will it evolve into a commercial product for other farms.

The long-term vision is clear:

> FarmOS transforms farm observations into evidence-based decisions.

This is the foundation of the product, the engineering handbook, and the future business opportunity.
