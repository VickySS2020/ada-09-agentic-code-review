# Traceability Matrix

|Requirement|SPEC/AC|Task|Files|Test|Status|Notes|
|---|---|---|---|---|---|---|
|FR-01|AC-01, SR-01|T-03, T-05|src/service.py, src/cli.py|tests/test_service.py::test_search_by_name_exact_and_partial, tests/test_cli.py::test_cli_search_by_name_renders_table|Completed|Search by name supports case-insensitive partial matching|
|FR-02|AC-02, SR-02|T-03, T-05|src/service.py, src/cli.py|tests/test_service.py::test_search_by_email_exact_and_partial, tests/test_cli.py::test_cli_search_by_email_renders_table|Completed|Search by email supports case-insensitive partial matching|
|FR-03|AC-03, VR-01, VR-02, EH-01|T-04, T-05|src/service.py, src/cli.py|tests/test_validation.py::test_validate_query_empty_string, tests/test_cli.py::test_cli_empty_query_rejected|Completed|Rejects empty or whitespace-only queries with 'ERROR: Invalid Input'|
|FR-04|AC-04|T-03, T-05|src/cli.py|tests/test_cli.py::test_cli_search_by_name_renders_table, tests/test_cli.py::test_format_table_output_structure|Completed|Results displayed in structured ASCII table with ID, Name, Email columns|
|FR-05|AC-05, EH-03|T-04, T-05|src/cli.py|tests/test_validation.py::test_cli_no_matches_by_name, tests/test_cli.py::test_cli_no_matches_message|Completed|Outputs 'MESSAGE: No customers found that matched <query>' on zero results|
|FR-06|AC-01, AC-02, AC-06, SR-03, VR-02, EH-02|T-03, T-04, T-05|src/cli.py|tests/test_cli.py::test_cli_unified_query_renders_table, tests/test_validation.py::test_cli_no_arguments_shows_instructions|Completed|Supports CLI flags --name, --email, --query|
|FR-07|AC-07, VR-03, EH-04, C-04|T-01, T-02, T-05|src/storage.py, customers.json|tests/test_storage.py::test_load_customers_default_file, tests/test_cli.py::test_cli_custom_file_argument|Completed|Customer records loaded from local JSON file with schema validation|
|NFR-01|C-02|T-01, T-02, T-03, T-04, T-05|src/models.py, src/storage.py, src/service.py, src/cli.py|tests/test_setup.py::test_project_structure|Completed|Zero external runtime dependencies; Python standard library only|
|NFR-02|(Architecture Decoupling)|T-03, T-05|src/service.py, src/cli.py|tests/test_service.py::test_business_logic_separation_from_presentation|Completed|Core business logic separated from presentation|
|NFR-03|C-03|T-01, T-05|tests/test_*.py|tests/test_service.py, tests/test_storage.py, tests/test_cli.py, tests/test_validation.py|Completed|Core logic automated and fully testable with pytest|
|NFR-04|AC-08|T-03, T-05|src/service.py|tests/test_service.py::test_search_performance_sub_100ms|Completed|Near-instantaneous search response time (< 100 ms)|
|NFR-05|C-01|T-01|tests/test_setup.py|tests/test_setup.py::test_python_version|Completed|Compatible with Python 3.11+ (validated on Python 3.13.5)|
