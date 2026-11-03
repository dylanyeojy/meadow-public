# Backend

The FastAPI service at the centre of Meadow. It receives each check-in from the app, calls the classifier, runs the deterministic routing and safety core, calls the LLM, runs the Memory Engine, and is the only part of the system that reads or writes the database. The design follows the project proposal: the routing rules in Section 3.3.4, the response layer and Memory Engine in Sections 3.3.5 to 3.3.7, the architecture in Section 3.5.1, and the database in Section 3.5.3.

## The rules it follows

- **Routing is deterministic Python, never the LLM.** The routing core is a pure function: input in, decision out, no database or network calls inside it.
- **No response body ever contains** `classification_label`, `class_probabilities`, `distress_score` or `route`. The app is told which screen to draw through `display.kind` and nothing more.
- **A classifier failure never defaults to a route.** The check-in is saved and the app shows "classification unavailable".
- **A failed generation never fabricates a reply.** The crisis hotlines are fixed content, never generated.
- Every check-in is saved, whatever the outcome.
- The backend queries Supabase **with the signed-in user's token**, so row-level security applies. The service role key is used for account deletion only.
- The stored LLM API key is encrypted before it is saved and is never sent back to the app.

## Secrets

Copy `.env.example` to `.env` and fill it in. `.env` is never committed.
