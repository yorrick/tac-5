# E2E Test: Random Query Generator

Test the Random Query Generator functionality in the Natural Language SQL Interface application.

## User Story

As a user
I want to generate random queries to explore data
So that I can discover interesting insights and learn how to query my data effectively

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** core UI elements are present:
   - Query input textbox
   - Query button
   - Upload Data button
   - Generate Random Query button
   - Available Tables section

5. Click the "Upload Data" button
6. Click the "Users Data" sample button to upload sample data
7. **Verify** the "Available Tables" section shows the users table
8. Take a screenshot showing the tables section

9. Click the "Generate Random Query" button
10. **Verify** the query input field is populated with a generated query
11. **Verify** the generated query is maximum 2 sentences
12. Take a screenshot of the generated query
13. Click the "Query" button to execute the generated query
14. **Verify** the query executes successfully and results are displayed
15. Take a screenshot of the query results

16. Click the "Generate Random Query" button again
17. **Verify** the query input field is updated (overwritten) with a new query
18. **Verify** the new generated query is maximum 2 sentences
19. Take a screenshot of the second generated query

20. Click the "Query" button to execute the second generated query
21. **Verify** the second query executes successfully and results are displayed
22. Take a screenshot of the second query results

## Success Criteria
- Generate Random Query button is visible and styled consistently with Upload Data button
- Button is visually separated from Query and Upload Data buttons
- Clicking the button generates a natural language query
- Generated queries are contextually relevant to the available tables
- Generated queries are limited to maximum two sentences
- Query input field is automatically populated with the generated query
- Existing text in query input is overwritten by generated query
- Button shows loading state while generating query
- Generated queries can be executed successfully
- Multiple clicks generate different queries (or at least update the field)
- 6 screenshots are taken
