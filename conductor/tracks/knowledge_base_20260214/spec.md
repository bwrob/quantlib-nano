# Specification: Knowledge Base Infrastructure

## Overview
Establish an automated system for creating and maintaining a local knowledge base of key project technologies (QuantLib, SWIG, nanobind, litgen) in a format optimized for AI consumption, ensuring integration with Gemini and the Conductor extension.

## Functional Requirements
- **Automated Fetching:** A script to pull documentation from multiple sources (GitHub, Doxygen HTML, ReadTheDocs).
- **Processing & Chunking:** Conversion of various formats (HTML, source files) into clean, chunked Markdown files.
- **Hierarchical Storage:** Organization within a `.knowledge` directory, structured by library/tool.
- **Git Integration:** Ensuring the `.knowledge` directory is ignored by Git via `.gitignore`.
- **Gemini & Conductor Integration:** Configure `.gemini/GEMINI.md` and `conductor/index.md` to explicitly point the AI agents to the `.knowledge` directory for technical reference.

## Non-Functional Requirements
- **AI Readability:** Markdown should be clean, consistent, and structured for high LLM context retrieval performance.
- **Maintainability:** The fetching script should be easy to run and update as upstream documentation evolves.

## Acceptance Criteria
- Script successfully fetches and processes at least one major documentation source (e.g., nanobind).
- The `.knowledge` directory structure matches the agreed-upon hierarchy.
- Files are correctly chunked and in readable Markdown format.
- `.gitignore` prevents the knowledge base from being committed.
- Gemini and Conductor can successfully "see" and reference the documentation (verified via a test query).

## Out of Scope
- Building the actual QuantLib bindings.
- Real-time synchronization.
