---
title: Farm Entities Glossary
status: Draft
version: 0.1.0
last_updated: 2026-07-01
---

# Farm Entities Glossary

Terms used across the domain chapters ([Ontology, Ch. 2](../02-Ontology.md) and [Chapters 5-12](../SUMMARY.md#part-3--core-mvp)). See [glossary/knowledge-model.md](knowledge-model.md) for Knowledge Model terminology.

### Animal

A single living animal (cow, sheep, goat, or horse) with its own Digital Twin, tracked individually. See [Chapter 5](../05-Animal-Digital-Twin/05-Animal-Digital-Twin.md).

### Flock

A managed group of poultry (chickens, ducks, or turkeys), tracked collectively as its own Digital Twin rather than bird-by-bird. See [Chapter 8](../08-Poultry/08-Poultry-Management.md).

### Herd

An optional grouping of Animals (e.g., "milking herd") used for feeding and task assignment. Does not replace the individual Animal Digital Twin. See [Ontology §2.3.5](../02-Ontology.md#235-herd).

### Location

A physical place on the farm — barn, pasture, field, pen, or storage area — that can nest (a pen belongs to a barn). See [Ontology §2.3.2](../02-Ontology.md#232-location-barn--field--pen).

### Field / Crop / Harvest Batch

A Field is a location used for planting; a Crop is what is planted there for a season; a Harvest Batch is the recorded output of harvesting a crop. See [Chapter 11](../11-Produce/11-Produce-Management.md).

### Feed Item / Feed Lot

A Feed Item is a type of feed; a Feed Lot is a specific purchased or produced batch of it with its own quantity and cost. See [Chapter 6](../06-Feed/06-Feed-Management.md).

### Inventory Lot

The general pattern applied to any stockable item (feed, medicine, product): a batch with quantity and cost, drawn down by movement events, with remaining stock always derived rather than directly edited. See [Chapter 10](../10-Inventory/10-Inventory-Management.md).

### Withdrawal Period

The time window after a medicine is administered during which milk, eggs, or meat from the treated Animal/Flock must not be sold or consumed. FarmOS blocks or warns against violating an active withdrawal period at the point of sale. See [Chapter 9 §9.3](../09-Veterinary/09-Veterinary-Management.md#93-treatment-workflow).

### Correction Event

A new event recorded to fix a mistaken prior entry, rather than editing or deleting the original. See [Behavioral Model §3.2](../03-Behavioral-Model.md#32-the-governing-rule-nothing-changes-without-an-event).

### Five-Minute Test

The acceptance test for a Digital Twin: an unfamiliar farm manager should be able to understand an entity's current status and history within five minutes using its Timeline. See [Ontology §2.6](../02-Ontology.md#26-the-five-minute-test).
