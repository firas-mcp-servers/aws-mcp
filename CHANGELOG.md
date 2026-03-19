# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-01

### Added
- EC2 tools: `list_instances`, `start_instance`, `stop_instance`, `describe_instance`
- S3 tools: `list_buckets`, `upload_file`, `download_file`, `list_objects`, `delete_object`
- Lambda tools: `list_functions`, `invoke_function`, `get_function_logs`
- RDS tools: `list_databases`, `describe_db`, `create_snapshot`
- CloudWatch tools: `get_metrics`, `list_alarms`, `get_log_events`
- IAM tools: `list_users`, `list_roles`, `get_policy`
- stdio and SSE transport modes
- AWS profile and region support per tool call
