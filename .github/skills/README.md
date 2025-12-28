# AI Agent Skills

This directory contains skill definitions for AI agents. Each skill is defined in a YAML file containing metadata, inputs, and the execution logic (typically a prompt template).

## Skill Structure

Each YAML file should follow this structure:

```yaml
name: Skill Name
description: A brief description of what the skill does.
version: 1.0.0
tags: [tag1, tag2]
inputs:
  input_name:
    type: string
    description: Description of the input.
    required: true/false
execution:
  type: prompt
  template: |
    Your prompt template here.
    Use {{input_name}} to insert input values.
```

## Available Skills

- **Code Review** (`code-review.yaml`): Analyzes code for bugs, style, and performance.
- **Generate Documentation** (`generate-documentation.yaml`): Creates documentation for code snippets.
- **Create Pull Request** (`create-pull-request.yaml`): Creates a GitHub PR using the `gh` CLI.
