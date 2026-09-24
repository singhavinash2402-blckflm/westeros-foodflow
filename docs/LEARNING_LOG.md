# FoodFlow — Learning Log

This log records important learning experiences, problems, solutions, decisions, and interview-level explanations throughout the FoodFlow project.

The goal is to capture not only what was built, but why it works and what was learned while building it.

---

# 2026-09-24 — Python Environment and Git Foundation

## Topics

* Python installation
* Python virtual environments
* Project-local `.venv`
* VS Code Python interpreter
* pip
* Git
* Git configuration
* Git repository initialization
* `.gitignore`
* Project documentation structure

---

## Python Environment

Python 3.12.0 was installed on Windows.

A project-local virtual environment was created:

C:\Work\westeros_foodflow_workspace\.venv

The virtual environment isolates FoodFlow's Python dependencies from the system Python installation.

The active interpreter was verified using:

where.exe python

The FoodFlow interpreter is:

C:\Work\westeros_foodflow_workspace\.venv\Scripts\python.exe

---

## Why Use a Project-Local Virtual Environment?

Different projects may require different package versions.

A project-local environment allows each project to maintain its own dependency set.

Example:

Project A
└── .venv

Project B
└── .venv

This prevents dependency conflicts between projects.

The `.venv` directory is excluded from Git.

---

## Git

Git was initialized at:

C:\Work\westeros_foodflow_workspace

The repository will contain:

* Source code
* Databricks notebooks
* Tests
* Documentation
* Configuration templates
* Infrastructure code
* Pipeline definitions
* Learning history

The Python virtual environment itself will not be committed.

---

## `.gitignore`

The `.gitignore` file excludes:

* `.venv`
* Environment files
* Secrets
* Python cache files
* Test caches
* Logs
* Machine-specific temporary files

This reduces the risk of accidentally committing local or sensitive artifacts.

---

## Key Learning

A Git repository should be treated as the project's source of truth.

Documentation is part of the engineering project and should therefore be version controlled.

---

## Interview Explanation

### Why use a virtual environment?

A virtual environment provides an isolated Python environment for a project so its dependencies and package versions do not interfere with the system Python installation or other projects.

### Why should `.venv` not be committed?

The environment contains installed packages and machine-specific files. Instead of committing it, the project should commit dependency definitions so the environment can be recreated.

### Why use `.gitignore`?

`.gitignore` prevents files such as virtual environments, caches, temporary files, and secrets from being tracked by Git.

---

# Future Learning Entries

Each significant FoodFlow implementation should add an entry containing:

## Topic

What was learned?

## Problem

What failed or required investigation?

## Solution

How was it solved?

## Why It Works

What underlying engineering concept explains the solution?

## Important Commands

Commands worth remembering.

## Design Decision

Was an architectural decision made?

## Interview Explanation

How would the concept be explained in a technical interview?

## Further Questions

What should be investigated next?
