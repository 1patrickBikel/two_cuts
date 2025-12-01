# Two Cuts Project\n\nThis repository contains the MVP architecture for the Two Cuts narrative reframing platform. The structure includes backend API definitions, classification logic, data files for testing, documentation, and space for notion synchronization and tests.
Two Cuts MVP Software Specification

Overview

The Two Cuts MVP is a narrative reframing platform designed to ingest daily voice memos, transcribe them, classify them using analytic tags and taxonomies, and store them in a database for long‑term narrative synthesis.  The goal is to help users identify patterns in their experiences and reframe difficult stories into empowering arcs.

This specification defines the database schema, classification logic, API endpoints, Notion database configuration, GitHub repository structure, and long‑term agent instructions required for the MVP.  Where appropriate, design choices are justified with references to cognitive science and narrative theory【60702603803198†L190-L366】 ￼.

System Components
	1.	Voice Memo Ingestion – captures audio from user devices, uploads recordings to secure storage, and triggers transcription.  The ingestion service assigns unique identifiers and metadata.
	2.	Transcription and Classification Engine – transcribes audio to text (e.g. using Whisper or a similar model), applies the classification logic described below to generate analytic tags, meta‑themes, time orientation, cognitive and embodiment states, and reframe scores.  The classifier leverages natural language processing models and pattern‑matching rules.
	3.	Data Storage – persists users, voice memos, and analytic tags in a relational database (e.g., PostgreSQL).  A separate Notion workspace mirrors the voice memo table for user‑facing browsing and annotation.
	4.	API Layer – exposes REST endpoints for creating users, uploading memos, retrieving memo and user information, and fetching clustered data.  These endpoints allow integration with mobile apps and other clients.
	5.	Narrative Synthesis/Clustering – groups memos by meta‑themes, cognitive/embodiment states, and temporal orientation to identify narrative arcs and generate monthly reports.
	6.	Front‑End (optional) – a simple web dashboard or Notion database view where users can browse their memos, see analytic tags, and view narrative arcs.

Data Schema

The MVP uses two primary tables.  Each property includes a suggested Notion type in parentheses.

Users
two-cuts/
├── README.md             # overview and setup instructions

├── backend/              # API application, models, schemas, services (ingestion, classifier, reports)

├── classification/       # emotion & narrative models, keyword maps

├── data/                 # sample JSON files for users, memos and clusters

├── notion/               # Notion sync script

├── docs/                 # documentation (including software spec)

└── tests/                # unit tests for the API
