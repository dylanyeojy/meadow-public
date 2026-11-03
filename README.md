# Meadow

An AI mental wellness app for Malaysian university students. Each day the student does a short check-in: four mood ratings and a journal entry. A fine-tuned MentalBERT classifier reads the entry, a deterministic routing and safety core decides how Meadow should respond, an LLM writes the response, and a Memory Engine keeps short notes so later responses can be more personal.

Final year Capstone Project for the Bachelor of Software Engineering at Sunway University, by Dylan Yeo.

## Status

**In progress.** Capstone Project 2 runs to December 2026. The app's screens are being built first, front end only, and the backend and classifier are connected to them afterwards. This repository is updated at each milestone.

## How it fits together

Meadow is three programs that talk over HTTP and JSON.

| Path | What |
| --- | --- |
| `app/` | The Android app: React Native with Expo, TypeScript and Expo Router |
| [backend/](backend/README.md) | The FastAPI backend: routing and safety core, LLM calls, Memory Engine, and the only part that touches the database |
| [classifier/](classifier/README.md) | The MentalBERT service (`ourafla/mental-health-bert-finetuned`), and the evaluation of how well it reads journal-style text |
| [assets/](assets/README.md) | Fonts and icons |

Supabase provides the database and sign-in, with row-level security. The LLM is an external API, using the student's own key.

## Safety by design

- **Routing is deterministic code. The LLM never decides how Meadow responds.**
- **No classification label, score or risk value is ever shown to the student**, and none is sent to the app.
- **Crisis hotlines are fixed content, never generated**, and stay reachable with or without an API key.
- **A failed classification or generation never makes up an answer.** Every check-in is saved whatever happens.

## Running

Each part has its own setup steps in its README. Secrets go in a `.env` file, which is never committed; each service has an `.env.example`.

## How this was built

AI assistance was used as a tutor while learning TypeScript and React, and to write evaluation scripts and setup code. The routing and safety logic, the check-in flow and the Memory Engine rules are written by hand.

## What is not here

The project's planning documents, specifications and logbooks are kept private, as are the evaluation dataset, its generation prompts and the rating sheets. Some READMEs mention files that are not in this repository for that reason.

## Licence

No licence is granted. This is assessed coursework: you are welcome to read the code, but please do not copy or reuse it.
