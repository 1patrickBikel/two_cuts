# Two Cuts MVP Software Specification

## Overview

The Two Cuts MVP is a narrative reframing platform designed to ingest daily voice memos, transcribe them, classify them using analytic tags and taxonomies, and store them in a database for long‑term narrative synthesis.  The goal is to help users identify patterns in their experiences and reframe difficult stories into empowering arcs.

This specification defines the database schema, classification logic, API endpoints, Notion database configuration, GitHub repository structure, and long‑term agent instructions required for the MVP.  Where appropriate, design choices are justified with references to cognitive science and narrative theory【60702603803198†L190-L366】【139852294401243†L179-L360】.

## System Components

1. **Voice Memo Ingestion** – captures audio from user devices, uploads recordings to secure storage, and triggers transcription.  The ingestion service assigns unique identifiers and metadata.
2. **Transcription and Classification Engine** – transcribes audio to text (e.g. using Whisper or a similar model), applies the classification logic described below to generate analytic tags, meta‑themes, time orientation, cognitive and embodiment states, and reframe scores.  The classifier leverages natural language processing models and pattern‑matching rules.
3. **Data Storage** – persists users, voice memos, and analytic tags in a relational database (e.g., PostgreSQL).  A separate Notion workspace mirrors the voice memo table for user‑facing browsing and annotation.
4. **API Layer** – exposes REST endpoints for creating users, uploading memos, retrieving memo and user information, and fetching clustered data.  These endpoints allow integration with mobile apps and other clients.
5. **Narrative Synthesis/Clustering** – groups memos by meta‑themes, cognitive/embodiment states, and temporal orientation to identify narrative arcs and generate monthly reports.
6. **Front‑End (optional)** – a simple web dashboard or Notion database view where users can browse their memos, see analytic tags, and view narrative arcs.

## Data Schema

The MVP uses two primary tables.  Each property includes a suggested Notion type in parentheses.

### Users

| Property            | Type (DB) | Notion Property    | Description                                                  |
|---------------------|-----------|--------------------|--------------------------------------------------------------|
| `user_id`           | UUID      | Title (Name)        | Primary key; unique identifier for the user.                |
| `user_name`         | TEXT      | Rich text          | Display name for the user.                                   |
| `created_at`        | TIMESTAMPTZ | Date              | When the user account was created.                           |

### Voice Memos

| Property                    | Type (DB)           | Notion Property          | Description                                                                                                 |
|-----------------------------|---------------------|--------------------------|-------------------------------------------------------------------------------------------------------------|
| `voice_memo_id`             | UUID                | Title (Name)             | Primary key; unique identifier for the memo.                                                                |
| `user_id`                   | UUID                | Relation → Users         | Foreign key linking to the user who recorded the memo.                                                      |
| `timestamp`                 | TIMESTAMPTZ         | Date                     | When the voice memo was recorded.                                                                           |
| `audio_url`                 | TEXT                | URL                      | Link to the audio file in storage (e.g. S3 or GCS).                                                         |
| `transcription_text`        | TEXT                | Long text                | Full transcription of the voice memo.                                                                       |
| `emotion_primary`           | TEXT/ENUM           | Select                   | Primary emotion (e.g. joy, sadness, anger, fear, trust, disgust, anticipation, surprise, anxiety, etc.).    |
| `emotion_secondary`         | TEXT/ENUM           | Select (optional)        | Secondary emotion if detected.                                                                             |
| `narrative_function`        | TEXT/ENUM           | Select                   | Label describing the memo’s narrative function (scene, emotion_dump, meaning_making, decision_point, integration_reflection, planning_future). |
| `cognitive_state`           | TEXT/ENUM           | Select                   | Cognitive state such as overloaded, scattered, ruminating, calm, focused, numb or shutdown.                |
| `embodiment_state`          | TEXT/ENUM           | Select                   | Degree of somatic engagement: hypercognitive_disembodied, head_heavy_body_ignored, partially_embodied, grounded, somatically_overwhelmed【450110501613372†L0-L152】. |
| `time_reference`            | TEXT/ENUM           | Select                   | Past, present, future or mixed, reflecting the orientation of the narrative【5569325376337†L61-L74】.         |
| `flavor_tags`               | TEXT[]/JSONB        | Multi‑select             | Tags from the Texture & Flavor framework (SEE/FEEL/HEAR categories).                                        |
| `meta_themes`               | TEXT[]/JSONB        | Multi‑select             | Higher‑level thematic labels (trauma, conflict, hope, shame, absurdity, etc.).                              |
| `reframe_opportunity_score` | NUMERIC(3,2)        | Number (0–1)             | Score indicating how ripe the memo is for reframing; higher means greater potential.                        |

## Taxonomies and Classification Logic

### Emotional Taxonomy

The classifier uses a variant of Plutchik’s wheel, which posits eight primary emotions arranged in opposing pairs.  Emotions can vary in intensity (e.g., annoyance → anger → rage) and blend with adjacent emotions【794069523445180†L96-L141】.  For the MVP, the primary set includes joy, sadness, anger, fear, trust, disgust, anticipation, surprise, anxiety and frustration.

### Narrative Function Taxonomy

Drawing on narrative theory, memos are tagged by their function: **scene** (describes events), **emotion_dump** (expresses feelings without a clear plot), **meaning_making** (reflects on meaning), **decision_point** (where a choice is made), **integration_reflection** (connecting past insights), and **planning_future** (anticipating or setting goals).  These categories mirror Labov’s narrative structure of orientation, complication and evaluation【139852294401243†L179-L360】.

### Cognitive and Embodiment States

The cognitive state captures the user’s mental load, from **overloaded** or **scattered** to **calm**, **focused**, **numb** or **shutdown**.  Embodiment states describe how connected a person feels to their body.  The assumption that thoughts, feelings and behaviors are grounded in sensory and bodily experiences forms the basis of this taxonomy【450110501613372†L0-L152】.  States range from **hypercognitive_disembodied** and **head_heavy_body_ignored** to **grounded** and **somatically_overwhelmed**.

### Time Orientation

The system infers whether the narrative centres on the past, present, future or a mix.  Research suggests that present orientation fosters a sense of control while past or future orientation can be associated with rumination or anxiety【5569325376337†L61-L74】.  The classifier detects verb tenses and explicit temporal markers to assign a time reference.

### Meta‑Themes

Meta‑themes are broader categories capturing recurring motifs: **trauma**, **conflict**, **hope**, **shame**, **absurdity**.  Additional themes can be added as the vocabulary evolves.  Memos can have multiple meta‑themes.

### Reframe Opportunity Score

The reframe score (0–1) indicates how beneficial reframing might be.  High scores correspond to memos with strong emotional intensity, cognitive overload, and unresolved themes such as trauma or conflict.  Memos that already contain self‑integrated meaning or planning signals receive lower scores.

### Classification Workflow

1. **Transcription** – Convert audio to text using a speech‑to‑text model.
2. **Emotion Detection** – Use an emotion classifier (e.g., fine‑tuned transformer) to compute probabilities for each emotion; assign the highest as primary and second highest as secondary.
3. **Narrative Function** – Detect structural cues: many proper nouns and past events → scene; many emotion words → emotion_dump; sentences starting with “I realized” or “this means” → meaning_making; statements of intent (“I need to”, “I’m going to”) → decision_point; after‑action reflection → integration_reflection; future‑planning language → planning_future.
4. **Cognitive and Embodiment Detection** – Apply pattern matching and machine learning to detect keywords related to mental overload, calmness, numbness and bodily sensations (breathing, feeling feet on the ground, etc.).
5. **Time Reference** – Analyse verb tenses and phrases (yesterday, tomorrow) to classify as past, present, future or mixed.
6. **Flavor Tag Extraction** – Use named‑entity recognition and keyword mapping to assign SEE (visual objects), FEEL (touch sensations) and HEAR (sounds) tags from the Texture & Flavor framework.
7. **Meta‑Theme Assignment** – Identify the presence of trauma, conflict, hope, shame, absurdity and other themes via keyword and sentiment analysis.  For instance, references to harm, abuse, accidents or chronic fear map to trauma, while language expressing inner or interpersonal struggle maps to conflict.
8. **Reframe Score Calculation** – Combine emotional intensity, cognitive state (e.g. overloaded), embodiment state, meta‑themes and presence/absence of meaning‑making to compute a score.  High emotional charge with unresolved themes yields a higher score.

## API Endpoints

The platform exposes the following RESTful endpoints.  Requests and responses use JSON; all endpoints require authentication (e.g., bearer token).

### Users

| Method | Endpoint             | Description                                  | Request Body/Parameters                                                             | Response                                  |
|-------|----------------------|----------------------------------------------|-------------------------------------------------------------------------------------|--------------------------------------------|
| POST  | `/users`             | Create a new user.                           | `{ "user_name": "string" }`                                                     | `201 Created` with `{ "user_id": UUID }` |
| GET   | `/users/{user_id}`   | Retrieve user details.                       | Path parameter `user_id`.                                                          | `200 OK` with user object.                 |
| GET   | `/users/{user_id}/voice-memos` | List voice memos for a user.            | Path parameter `user_id`, optional query params `page`, `limit`.                   | `200 OK` with list of memos.               |

### Voice Memos

| Method | Endpoint                | Description                                            | Request Body/Parameters                                                                                                                    | Response                                   |
|-------|-------------------------|--------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
| POST  | `/voice-memos`          | Upload a voice memo (audio and metadata).              | Multipart form: audio file or `audio_url`, `user_id`, optional `timestamp`.  Server will transcribe and classify automatically.             | `201 Created` with memo object.            |
| GET   | `/voice-memos/{id}`     | Retrieve a specific memo.                              | Path parameter `id`.                                                                                                                     | `200 OK` with memo object.                 |
| GET   | `/voice-memos`          | Query memos by filters.                                | Query params: `user_id`, `meta_theme`, `cognitive_state`, `time_reference`, `min_score`, `max_score`, pagination.                         | `200 OK` with list of memos.               |

### Clusters and Reports

| Method | Endpoint                 | Description                                           | Request Body/Parameters                | Response                                     |
|-------|--------------------------|-------------------------------------------------------|----------------------------------------|----------------------------------------------|
| GET   | `/clusters`              | Return mapping of meta‑themes to memo IDs.            | Optional query: `meta_theme=conflict`. | `200 OK` with cluster object.                |
| GET   | `/users/{id}/report`     | Generate a monthly arc report for a user.             | Path parameter `id`; optional `month`. | `200 OK` with aggregated statistics.         |

Errors follow standard HTTP codes (400 for bad request, 401 for unauthorized, 404 for not found, 500 for server errors).  All responses include an `error` field when a request fails.

## Notion Database Configuration

To mirror the voice memo table in Notion:

1. Create a new Notion **Database** titled “Voice Memos”.
2. Add the properties listed in the **Voice Memos** table above, using the specified Notion types (e.g., Select for `emotion_primary`, Multi‑select for `meta_themes`).
3. Create a second **Database** titled “Users” with `user_id` as the Title property and `user_name` as text.  Add a Relation property in “Voice Memos” pointing to the “Users” database.
4. Configure views such as “By Theme” (group by meta‑themes), “High Reframe” (filter `reframe_opportunity_score` ≥ 0.75), and “This Month” (filter by `timestamp` within the current month).

Integration can be automated via the Notion API: upon classification, the backend inserts or updates records using the same schema.

## Agent Long‑Term Instruction Set

The classification agent should adhere to these long‑term instructions:

1. **Consistent Taxonomies** – Always use the defined sets for emotions, narrative functions, cognitive and embodiment states, time references and meta‑themes.  If uncertain, choose the closest match or leave secondary fields null.
2. **Grounding in Embodiment** – Attend to sensory descriptions (seeing, feeling, hearing) to infer embodiment state.  Recognise that physical sensations anchor cognitive processes【450110501613372†L0-L152】.
3. **Detect Conflict and Dissonance** – Flag memos expressing aversive tension, unresolved dilemmas or self‑contradictory beliefs, as these indicate cognitive dissonance【60702603803198†L190-L366】 and may warrant higher reframe scores.
4. **Respect Narrative Function** – Distinguish between recounting events, venting emotions, making meaning, deciding and planning.  This aids in creating coherent story arcs.
5. **Prioritise Present Orientation** – Identify whether the user is focused on the present (in control), the past (rumination) or the future (anticipation)【5569325376337†L61-L74】, and encourage shifts toward present‑focused perspectives where appropriate.
6. **Meta‑Theme Recognition** – Assign trauma, conflict, hope, shame and absurdity by matching language patterns; multiple meta‑themes are allowed.
7. **Reframe Scoring** – Use emotional intensity and unresolved themes to compute the `reframe_opportunity_score`.  Emphasise memos where the user seems stuck and lacks meaning‑making.
8. **Update Notion** – After classification, push results to Notion, maintaining data consistency and property types.
9. **Learn Continuously** – Incorporate feedback from users (e.g. corrections to tags) to refine models and expand taxonomies.

## GitHub Repository Structure

The following structure organises the codebase:

```
 two-cuts/
 ├── README.md                  # Project overview and setup instructions
 ├── backend/
 │   ├── app.py                 # FastAPI or Flask application with API endpoints
 │   ├── models/                # SQLAlchemy models for Users and VoiceMemos
 │   ├── schemas/               # Pydantic schemas for request/response bodies
 │   ├── services/
 │   │   ├── ingestion.py       # Handles audio upload and transcription
 │   │   ├── classifier.py      # Contains classification logic and taxonomies
 │   │   └── reports.py         # Generates cluster maps and monthly reports
 │   └── utils/                 # Helper functions (e.g., time parsing, NER)
 ├── classification/
 │   ├── emotion_model.py       # Pre‑trained emotion classifier
 │   ├── narrative_model.py     # Model or rules for narrative function detection
 │   └── keyword_maps.json      # Keywords for flavor tags and meta‑themes
 ├── data/
 │   ├── users.json             # Example user data for development
 │   ├── voice_memos.json       # Example memos for testing
 │   └── clusters.json          # Example cluster map
 ├── notion/
 │   └── notion_sync.py         # Script to sync DB records with Notion via API
 ├── docs/
 │   ├── software_spec.md       # This document
 │   └── api_reference.md       # Auto‑generated API documentation
 └── tests/
     └── test_endpoints.py      # Unit tests for API endpoints
```

## Future Extensions

The MVP lays the groundwork for more advanced features:

* **Adaptive Learning** – Fine‑tune classifiers using user feedback to improve tagging accuracy.
* **Story Generation** – Build upon narrative clusters to generate summaries or reframed stories, while respecting privacy and user agency.
* **Real‑Time Embodiment Coaching** – Provide prompts encouraging users to reconnect with their bodies when hypercognitive states are detected.
* **Integration with Calendar/Tasks** – Link memos with action items and schedule follow‑up reflections.
* **Multi‑language Support** – Expand transcription and classification to handle languages beyond English.

## Citations

Key theoretical underpinnings include:

* Cognitive dissonance, the aversive state arising from inconsistent beliefs or actions【60702603803198†L190-L366】.
* Narrative structure components (orientation, complication, evaluation) that inform narrative function tagging【139852294401243†L179-L360】.
* Embodiment theory, which posits that thoughts, feelings and behaviours are grounded in sensory and bodily experiences【450110501613372†L0-L152】.
* Research on temporal orientation, noting how focus on past, present or future influences mood and control【5569325376337†L61-L74】.
* The eight primary emotions and their intensity scales used to construct the emotional taxonomy【794069523445180†L96-L141】.

