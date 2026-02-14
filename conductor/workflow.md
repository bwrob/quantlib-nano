# Project Workflow

## Guiding Principles

1. **The Plan is the Source of Truth:** All work must be tracked in `plan.md`
2. **The Tech Stack is Deliberate:** Changes to the tech stack must be documented in `tech-stack.md` _before_ implementation
3. **Test-Driven Development:** Write unit tests before implementing functionality
4. **High Code Coverage:** Aim for >100% (for binding scripts) code coverage for all modules
5. **User Experience First:** Every decision should prioritize user experience
6. **Non-Interactive & CI-Aware:** Prefer non-interactive commands. Use `CI=true` for watch-mode tools (tests, linters) to ensure single execution.

## Task Workflow

All tasks follow a strict lifecycle:

### Standard Task Workflow

1. **Select Task:** Choose the next available task from `plan.md` in sequential order

2. **Mark In Progress:** Before beginning work, edit `plan.md` and change the task from `[ ]` to `[~]`

3. **Write Failing Tests (Red Phase):**
   - Create a new test file for the feature or bug fix.
   - Write one or more unit tests that clearly define the expected behavior and acceptance criteria for the task.
   - **CRITICAL:** Run the tests and confirm that they fail as expected. This is the "Red" phase of TDD. Do not proceed until you have failing tests.

4. **Implement to Pass Tests (Green Phase):**
   - Write the minimum amount of application code necessary to make the failing tests pass.
   - Run the test suite again and confirm that all tests now pass. This is the "Green" phase.

5. **Refactor (Optional but Recommended):**
   - With the safety of passing tests, refactor the implementation code and the test code to improve clarity, remove duplication, and enhance performance without changing the external behavior.
   - Rerun tests to ensure they still pass after refactoring.

6. **Verify Coverage:** Run coverage reports using the project's chosen tools. For example, in a Python project, this might look like:

   ```bash
   pytest --cov=app --cov-report=html
   ```

   Target: >100% (for binding scripts) coverage for new code. The specific tools and commands will vary by language and framework.

7. **Document Deviations:** If implementation differs from tech stack:
   - **STOP** implementation
   - Update `tech-stack.md` with new design
   - Add dated note explaining the change
   - Resume implementation

8. **Commit Code Changes:**
   - Stage all code changes related to the task.
   - Propose a clear, concise commit message e.g, \`feat(scraper): Add intelligent chunking for Markdown\`.
   - Perform the commit.

9. **Attach Task Summary with Git Notes:**
   - **Step 9.1: Get Commit Hash:** Obtain the hash of the _just-completed commit_ (`git log -1 --format="%H"`).
   - **Step 9.2: Draft Note Content:** Create a detailed summary for the completed task. This should include the task name, a summary of changes, a list of all created/modified files, and the core "why" for the change.
   - **Step 9.3: Attach Note:** Use the `git notes` command to attach the summary to the commit.
     ```bash
     # The note content from the previous step is passed via the -m flag.
     git notes add -m "<note content>" <commit_hash>
     ```

10. **Get and Record Task Commit SHA:**
    - **Step 10.1: Update Plan:** Read `plan.md`, find the line for the completed task, update its status from `[~]` to `[x]`, and append the first 7 characters of the _just-completed commit's_ commit hash.
    - **Step 10.2: Write Plan:** Write the updated content back to `plan.md`.

11. **Commit Plan Update:**
    - **Action:** Stage the modified `plan.md` file.
    - **Action:** Commit this change with a descriptive message (e.g., `conductor(plan): Mark task 'Create user model' as complete`).

### Phase Completion Verification and Checkpointing Protocol

**Trigger:** This protocol is executed immediately after a task is completed that also concludes a phase in `plan.md`.

1.  **Announce Protocol Start:** Inform the user that the phase is complete and the verification and checkpointing protocol has begun.

2.  **Ensure Test Coverage for Phase Changes:**
    - **Step 2.1: Determine Phase Scope:** To identify the files changed in this phase, you must first find the starting point. Read `plan.md` to find the Git commit SHA of the _previous_ phase's checkpoint. If no previous checkpoint exists, the scope is all changes since the first commit.
    - **Step 2.2: List Changed Files:** Execute `git diff --name-only <previous_checkpoint_sha> HEAD` to get a precise list of all files modified during this phase.
    - **Step 2.3: Verify and Create Tests:** For each file in the list:
      - **CRITICAL:** First, check its extension. Exclude non-code files (e.g., `.json`, `.md`, `.yaml`).
      - For each remaining code file, verify a corresponding test file exists.
      - If a test file is missing, you **must** create one. Before writing the test, **first, analyze other test files in the repository to determine the correct naming convention and testing style.** The new tests **must** validate the functionality described in this phase's tasks (`plan.md`).

3.  **Execute Automated Tests with Proactive Debugging:**
    - Before execution, you **must** announce the exact shell command you will use to run the tests.
    - **Example Announcement:** "I will now run the automated test suite to verify the phase. **Command:** \`uv run pytest\`"
    - Execute the announced command.
    - If tests fail, you **must** inform the user and begin debugging. You may attempt to propose a fix a **maximum of two times**. If the tests still fail after your second proposed fix, you **must stop**, report the persistent failure, and ask the user for guidance.

4.  **Propose a Detailed, Actionable Manual Verification Plan:**
    - **CRITICAL:** To generate the plan, first analyze `product.md`, `product-guidelines.md`, and `plan.md` to determine the user-facing goals of the completed phase.
    - You **must** generate a step-by-step plan that walks the user through the verification process, including any necessary commands and specific, expected outcomes.
    - The plan you present to the user **must** follow this format:

      **For a Binding Change:**

      ```
      The automated tests have passed. For manual verification, please follow these steps:

      **Manual Verification Steps:**
      1.  **Build the bindings using:** `uv run poe build`
      2.  **Run the verification script:** `python .help/verify_binding.py`
      3.  **Confirm that you see:** The expected discount factor output for the target date.
      ```

      **For an Infrastructure Change:**

      ```
      The automated tests have passed. For manual verification, please follow these steps:

      **Manual Verification Steps:**
      1.  **Execute the utility command:** `uv run poe fetch-knowledge`
      2.  **Check the output directory:** `ls -R .knowledge/quantlib`
      3.  **Confirm that you see:** The new documentation chunks correctly split by headers.
      ```

5.  **Announce Phase Verification:**
    - After presenting the detailed plan, inform the user that the phase verification steps have been defined and are ready for later UAT.
    - **CONTINUE:** Proceed immediately to the next task or phase. Do not pause for user feedback at this stage.

6.  **Create Checkpoint Commit:**
    - Stage all changes. If no changes occurred in this step, proceed with an empty commit.
    - Perform the commit with a clear and concise message (e.g., `conductor(checkpoint): Checkpoint end of Phase X`).

7.  **Attach Auditable Verification Report using Git Notes:**
    - **Step 7.1: Draft Note Content:** Create a detailed verification report including the automated test command, the manual verification steps, and the user's confirmation.
    - **Step 7.2: Attach Note:** Use the `git notes` command and the full commit hash from the previous step to attach the full report to the checkpoint commit.

8.  **Get and Record Phase Checkpoint SHA:**
    - **Step 8.1: Get Commit Hash:** Obtain the hash of the _just-created checkpoint commit_ (`git log -1 --format="%H"`).
    - **Step 8.2: Update Plan:** Read `plan.md`, find the heading for the completed phase, and append the first 7 characters of the commit hash in the format `[checkpoint: <sha>]`.
    - **Step 8.3: Write Plan:** Write the updated content back to `plan.md`.

9.  **Commit Plan Update:**
    - **Action:** Stage the modified `plan.md` file.
    - **Action:** Commit this change with a descriptive message following the format `conductor(plan): Mark phase '<PHASE NAME>' as complete`.

10. **Announce Completion:** Inform the user that the phase is complete and the checkpoint has been created, with the detailed verification report attached as a git note.

### Track Acceptance and Closure Protocol (UAT)

**Trigger:** This protocol is executed after all implementation phases in a \`plan.md\` are completed.

1.  **Perform Automated Self-Review:**
    - Announce that the implementation is complete and you will now perform an automated self-review of the changes.
    - Execute the \`/code-review\` command to analyze the code quality and adherence to best practices.
    - Execute the internal \`conductor review\` check (if available) or perform a manual cross-reference check to analyze the track's implementation specifically against the \`spec.md\`, \`plan.md\`, \`tech-stack.md\`, and \`product-guidelines.md\`.
    - Address any high-priority issues or inconsistencies identified by both reviews before proceeding.

2.  **Initiate UAT Phase:** Announce that the implementation and self-review are complete and the track is now entering the **User Acceptance Testing (UAT)** stage.

3.  **Continuous Feedback Loop:**
    - The track remains in the "UAT" status until the user explicitly approves closure.
    - **"I commented" Protocol:** If the user states "I commented" (or similar), the AI agent MUST immediately fetch all comments from the active pull request (using the \`poe fetch-comments\` task), analyze them, and systematically address each piece of feedback by updating the code and tests.
    - The user is encouraged to test the feature/fix and provide feedback, especially regarding underspecified requirements or adjustments based on the implementation results.
    - If the user requests changes, the AI agent must update the `spec.md` and `plan.md` to include the necessary tasks and resume implementation.

4.  **Final Approval Request:** Once all feedback has been addressed, ask the user: "**All implementation and feedback for this track have been addressed. Are you satisfied with the results and ready to close this track?**"

5.  **Mark Track as Completed (Perform in Feature Branch):**

    -   **Step 5.1: Update Metadata:** Set the \`status\` to \`completed\` in the track's \`metadata.json\`.

    -   **Step 5.2: Update Registry:** Update the \`conductor/tracks.md\` file, marking the track as done \`[x]\` and updating its link to the archive.

    -   **Step 5.3: Mandatory Archiving:** Move the track's directory to \`conductor/archive/\`. Completed tracks MUST ALWAYS be archived and NEVER deleted; they serve as a permanent historical record of the project's evolution.

    -   **Step 5.4: Commit Closure Artifacts:** Commit these changes to the feature branch with the message \`chore(conductor): Prepare track '<track_description>' for closure\`.



6.  **Final Merge:** Merge the feature branch into \`main\` (via PR or direct merge as per policy).



7.  **Announce Track Closure:** Inform the user that the track is officially closed and summarized in the project history.



### Quality Gates

Before marking any task complete, verify:

- [ ] All tests pass
- [ ] Code coverage meets requirements (>100% (for binding scripts))
- [ ] **Performance:** No regressions in the 50-year daily benchmark (for binding tasks)
- [ ] Code follows project's code style guidelines (as defined in \`code_styleguides/\`)
- [ ] All public functions/methods are documented (e.g., docstrings, JSDoc, GoDoc)
- [ ] Type safety is enforced (e.g., type hints, TypeScript types, Go types)
- [ ] No linting or static analysis errors (using the project's configured tools)
- [ ] Documentation updated if needed
- [ ] No security vulnerabilities introduced

## Development Commands

### Auxiliary & Verification Scripts

- **The .help Directory:** All project-specific auxiliary scripts, manual verification prototypes, debug helpers, and temporary "scripts-of-the-moment" MUST be created in the \`.help/\` directory.
- **Git Ignored:** The \`.help/\` directory is excluded from version control to keep the repository clean and avoid polluting the project's utility modules.
- **Documentation:** If an auxiliary script becomes a permanent part of the development toolkit, it should be refactored into the \`utils/\` directory and properly documented before being committed.

### Setup

\`\`\`bash
# Install dependencies using uv
uv sync
# Install pre-commit hooks
uv run pre-commit install
\`\`\`

### Daily Development

\`\`\`bash
# Run the knowledge base scraper
uv run poe fetch-knowledge
# Run tests
uv run pytest
# Run linting and formatting
uv run ruff check .
uv run ruff format .
\`\`\`

### Before Committing

\`\`\`bash
# Run all pre-commit checks on staged files
uv run pre-commit run
# Run all checks on all files
uv run pre-commit run --all-files
\`\`\`

## Testing Requirements

### Unit Testing

- **Pytest Required:** All Python code MUST be tested using the \`pytest\` framework.
- Every module must have corresponding tests.
- Use appropriate test setup/teardown mechanisms (e.g., fixtures, beforeEach/afterEach).
- Mock external dependencies.
- Test both success and failure cases.

### Integration Testing

- Test complete user flows
- Verify library integration with sample applications

## Code Review Process

### Self-Review Checklist

Before requesting review:

1. **Functionality**
   - Feature works as specified
   - Edge cases handled
   - Error messages are user-friendly

2. **Code Quality**
   - Follows style guide
   - DRY principle applied
   - Clear variable/function names
   - Appropriate comments

3. **Testing**
   - Unit tests comprehensive
   - Integration tests pass
   - Coverage adequate (>100% (for binding scripts))

4. **Security**
   - No hardcoded secrets
   - Input validation present

5. **Performance**
   - No regressions in the 50-year daily benchmark
   - Caching implemented where needed

## Commit Guidelines

### Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests
- `chore`: Maintenance tasks

### Examples

\`\`\`bash
git commit -m "feat(scraper): Add intelligent chunking for Markdown"
git commit -m "fix(binding): Correct Date arithmetic in Python wrapper"
git commit -m "test(quantlib): Add tests for Calendar business day advancement"
git commit -m "style(config): Update ruff linting rules"
\`\`\`

## Definition of Done

A task is complete when:

1. All code implemented to specification
2. Unit tests written and passing
3. Code coverage meets project requirements
4. Documentation complete (if applicable)
5. Code passes all configured linting and static analysis checks
6. Implementation notes added to \`plan.md\`
7. Changes committed with proper message
8. Git note with task summary attached to the commit

## Continuous Improvement

- Review workflow weekly
- Update based on pain points
- Document lessons learned
- Optimize for developer experience
- Keep things simple and maintainable

## Branching & Commit Policy

- **Feature Branches Required:** NEVER work directly on the \`main\` branch.
- **Track-Based Branching:** Create a new feature branch (named after the track ID, e.g., \`track/shortname_YYYYMMDD\`) immediately upon starting work on a new track.
- **Phase-Based Branching (Optional):** Maintain separate branches for each phase within a track if necessary, but the primary rule is isolation from \`main\`.
- **Frequent commits within branches.**
- **Always merge via PR with Squash.**
- **No direct commits to the main branch.**
