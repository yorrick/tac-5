# Feature: Random Natural Language Query Generator

## Feature Description
A button that generates random, interesting natural language queries based on the existing database tables and their structure. When clicked, the button will use the LLM to create a contextually relevant query (limited to two sentences maximum) and automatically populate the query input field, overwriting any existing content. This feature helps users explore their data by providing example queries they can execute manually.

## User Story
As a user
I want to generate random natural language queries based on my uploaded data
So that I can discover interesting insights and learn how to query my data effectively

## Problem Statement
Users may not always know what questions to ask about their data, especially when first uploading a dataset. Without example queries or suggestions, users may struggle to explore their data effectively. This creates a barrier to entry and reduces engagement with the application.

## Solution Statement
Implement a "Generate Random Query" button positioned separately from the primary Query and Upload Data buttons, styled similarly to the Upload Data button. When clicked, the button will invoke the existing `llm_processor.py` to analyze the current database schema and generate an interesting, contextually relevant natural language query (max two sentences) that demonstrates the data exploration capabilities. The generated query will replace any existing text in the query input field, ready for the user to execute manually.

## Relevant Files
Use these files to implement the feature:

- **`app/server/core/llm_processor.py`** - Contains existing LLM integration with OpenAI and Anthropic. Will be extended to add a new function `generate_random_query()` that creates natural language queries based on database schema.

- **`app/server/core/sql_processor.py`** - Contains `get_database_schema()` function which retrieves current database schema information needed to generate contextual queries.

- **`app/server/server.py`** - FastAPI server where we'll add a new endpoint `POST /api/generate-query` to handle random query generation requests.

- **`app/server/core/data_models.py`** - Pydantic models for API request/response. Will add `GenerateQueryRequest` and `GenerateQueryResponse` models.

- **`app/client/index.html`** - Contains the UI structure. Will add the new "Generate Random Query" button in the query controls section, positioned using `justify-content: space-between` to separate it from primary buttons.

- **`app/client/src/main.ts`** - Main TypeScript file containing UI logic. Will add event handler for the new button and API call to fetch random query.

- **`app/client/src/api/client.ts`** - API client functions. Will add `generateRandomQuery()` function to call the new backend endpoint.

- **`app/client/src/types.d.ts`** - TypeScript type definitions. Will add `GenerateQueryRequest` and `GenerateQueryResponse` interfaces.

- **`app/client/src/style.css`** - Contains styling. The new button will reuse the existing `.secondary-button` class for consistent styling with the Upload Data button.

### New Files

- **`.claude/commands/e2e/test_random_query_generator.md`** - E2E test file to validate the Random Query Generator feature works correctly.

- **`app/server/tests/core/test_random_query_generator.py`** - Unit tests for the random query generation logic.

## Implementation Plan

### Phase 1: Foundation
First, we'll extend the backend infrastructure to support random query generation:
1. Add new Pydantic models to `data_models.py` for the request/response
2. Create the `generate_random_query()` function in `llm_processor.py` that uses existing LLM providers (OpenAI/Anthropic) to generate queries based on schema
3. Add the new `/api/generate-query` endpoint in `server.py`
4. Write comprehensive unit tests for the query generation logic

### Phase 2: Core Implementation
Build the frontend UI components and integrate with the backend:
1. Update TypeScript type definitions in `types.d.ts`
2. Add the API client function in `client.ts`
3. Add the "Generate Random Query" button to the HTML with appropriate styling
4. Implement the event handler in `main.ts` to fetch and populate the query input field
5. Ensure the button is properly positioned and styled to match the Upload Data button

### Phase 3: Integration
Test end-to-end functionality and ensure everything works together:
1. Create E2E test file to validate the feature
2. Test with various database schemas (no tables, single table, multiple tables)
3. Verify error handling when no tables are available
4. Validate that the query input field is properly overwritten
5. Run full test suite to ensure no regressions

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Backend Data Models
- Add `GenerateQueryRequest` model to `app/server/core/data_models.py` (minimal, potentially empty)
- Add `GenerateQueryResponse` model with fields: `query` (str), `tables_used` (List[str]), `error` (Optional[str])

### 2. Backend Query Generation Logic
- Add `generate_random_query_with_openai()` function to `app/server/core/llm_processor.py`
  - Accept `schema_info` parameter (from `get_database_schema()`)
  - Create prompt that instructs LLM to generate interesting natural language queries based on the schema
  - Emphasize max two sentences in the prompt
  - Request queries that demonstrate different types of operations (filtering, aggregation, sorting, joins if multiple tables)
  - Return the generated query string
- Add `generate_random_query_with_anthropic()` function with same signature and logic
- Add `generate_random_query()` router function that uses the same provider priority logic as `generate_sql()`

### 3. Backend API Endpoint
- Add `POST /api/generate-query` endpoint to `app/server/server.py`
  - Call `get_database_schema()` to get current schema
  - If no tables exist, return error: "No tables available. Please upload data first."
  - Call `generate_random_query()` with schema information
  - Return `GenerateQueryResponse` with the generated query and list of tables used
  - Add proper error handling and logging

### 4. Backend Unit Tests
- Create `app/server/tests/core/test_random_query_generator.py`
  - Test `generate_random_query_with_openai()` with mock API responses
  - Test `generate_random_query_with_anthropic()` with mock API responses
  - Test router function selects correct provider
  - Test error handling when no API keys available
  - Test that generated queries are 2 sentences or less
- Run tests: `cd app/server && uv run pytest tests/core/test_random_query_generator.py -v`

### 5. Frontend Type Definitions
- Add `GenerateQueryRequest` interface to `app/client/src/types.d.ts` (likely empty)
- Add `GenerateQueryResponse` interface with fields matching backend model

### 6. Frontend API Client
- Add `generateRandomQuery()` function to `app/client/src/api/client.ts`
  - Call `POST /api/generate-query`
  - Return `GenerateQueryResponse`
  - Handle errors appropriately

### 7. Frontend UI - HTML Structure
- Add "Generate Random Query" button to `app/client/index.html`
  - Insert in the `.query-controls` div, positioned after the existing buttons
  - Use `id="generate-query-button"`
  - Apply `class="secondary-button"` for consistent styling with Upload Data button
  - Set button text to "Generate Random Query"
- Update `.query-controls` CSS to use `justify-content: space-between` to separate the Generate button from Query/Upload buttons

### 8. Frontend UI - Event Handler
- Add event handler initialization in `app/client/src/main.ts`
  - Create `initializeGenerateQuery()` function
  - Get reference to `generate-query-button`
  - On click:
    - Disable button and show loading state
    - Call `api.generateRandomQuery()`
    - If successful and no error, set `query-input.value` to the generated query (overwrite existing content)
    - If error, display error message using existing `displayError()` function
    - Re-enable button
  - Call `initializeGenerateQuery()` from the `DOMContentLoaded` event listener

### 9. Frontend UI - Styling (if needed)
- Review `.secondary-button` styling in `app/client/src/style.css`
- Verify button spacing in `.query-controls` is appropriate
- Adjust if necessary to ensure proper visual separation between primary buttons (Query, Upload Data) and the Generate Random Query button

### 10. Create E2E Test File
- Read `.claude/commands/test_e2e.md` to understand E2E test format
- Read `.claude/commands/e2e/test_basic_query.md` to understand existing test structure
- Create `.claude/commands/e2e/test_random_query_generator.md`
  - User Story: User wants to generate random queries to explore data
  - Test Steps:
    1. Navigate to application
    2. Upload sample users data
    3. Verify "Generate Random Query" button is present
    4. Click the button
    5. Verify query input field is populated with generated query (max 2 sentences)
    6. Take screenshot of generated query
    7. Click Query button to execute the generated query
    8. Verify results are displayed
    9. Click Generate Random Query again
    10. Verify a different query is generated (or at least the field is updated)
    11. Take screenshot of second generated query
  - Success Criteria:
    - Button generates queries when clicked
    - Query input field is overwritten with generated query
    - Generated queries are valid and executable
    - Generated queries reference actual table names
    - Queries are max 2 sentences
    - Screenshots captured successfully

### 11. Validation - Run All Tests
- Execute backend unit tests: `cd app/server && uv run pytest -v`
- Execute frontend type check: `cd app/client && bun tsc --noEmit`
- Execute frontend build: `cd app/client && bun run build`
- Read `.claude/commands/test_e2e.md` then execute E2E test: `.claude/commands/e2e/test_random_query_generator.md`

## Testing Strategy

### Unit Tests
- **LLM Provider Functions**: Mock OpenAI and Anthropic API calls to test query generation logic
- **Routing Logic**: Test that the correct provider is selected based on API key availability
- **Schema Handling**: Test behavior with empty schema, single table, and multiple tables
- **Error Handling**: Test error responses when no tables exist or API calls fail
- **Query Length**: Verify generated queries don't exceed two sentences

### Edge Cases
- **No tables in database**: Should return helpful error message
- **Single table**: Should generate query for that one table
- **Multiple tables**: Should generate queries that may involve joins
- **Complex schemas**: Tables with many columns should generate focused queries
- **API failures**: Handle OpenAI/Anthropic API errors gracefully
- **Concurrent clicks**: Button should be disabled during API call to prevent multiple simultaneous requests
- **Empty query input**: Generated query should populate empty field
- **Existing query text**: Generated query should overwrite existing text

## Acceptance Criteria
- [ ] New "Generate Random Query" button is visible and styled consistently with Upload Data button
- [ ] Button is visually separated from Query and Upload Data buttons (using justify-content: space-between)
- [ ] Clicking the button generates a natural language query based on current database schema
- [ ] Generated queries are contextually relevant to the available tables and columns
- [ ] Generated queries are limited to maximum two sentences
- [ ] Query input field is automatically populated with the generated query, overwriting any existing content
- [ ] Error message is displayed when no tables are available in the database
- [ ] Button shows loading state while generating query
- [ ] Backend endpoint handles errors gracefully and returns appropriate error messages
- [ ] Unit tests pass with >80% coverage for new code
- [ ] E2E test validates full user workflow
- [ ] TypeScript compiles without errors
- [ ] Frontend builds successfully
- [ ] No regressions in existing functionality

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute E2E test `.claude/commands/e2e/test_random_query_generator.md` to validate this functionality works
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type check to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes
- The feature uses the existing `llm_processor.py` module, maintaining consistency with the current architecture
- The LLM provider selection follows the same priority logic as query SQL generation (OpenAI first, then Anthropic)
- The button is intentionally positioned separately from primary action buttons to indicate it's an exploratory/helper feature
- Generated queries should be diverse and interesting, demonstrating different SQL capabilities (WHERE clauses, aggregations, ORDER BY, LIMIT, JOINs when applicable)
- Consider adding variety in query complexity - mix simple queries with more complex ones
- The two-sentence limit ensures queries remain focused and easy to understand
- Future enhancement: Add a "Recent Generated Queries" history feature
- Future enhancement: Allow users to specify query complexity level (simple, medium, complex)
- Future enhancement: Add ability to generate queries for specific tables only
