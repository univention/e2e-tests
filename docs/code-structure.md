# Code Structure of the Test Suite

## Overview

- `/docs` - Documentation about the e2e test suite and its design.

- `/src` - Source code of the utilities which support the test suite.

- `/src/e2e` - Base package for the source code.

   This does contain the implementation of the Page Object models and various
   utilities used as or by pytest fixtures.

   Note: We are moving the other packages into the `e2e` package to avoid
   clashes with other top level packages.

- `/src/e2e/api` - (former `/src/api`) Utilities for API interaction.

- `/src/e2e/chaos` - Supporting failure injection inspired by Chaos Testing.

- `/src/e2e/email` - Contains email related models.

- `/src/e2e/kubernetes` - Supporting the interaction with the Kubernetes
  cluster.

- `/src/e2e/ldap` - Supporting the ldap deployment interaction.

- `/src/e2e/pages` - (former `/src/umspages`) Contains the Page Object Model
  implementations.

- `/tests` - All regular e2e test cases are within this top level folder.

- `/tests-ldap` - Specific test cases which simulate failure scenarios around
  ldap and typically need an adjusted deployment as a starting point.


## Page Objects

Page Objects are organized as follows in the `tests/pages` folder.

```
├── base.py  # Base page objects
├── __init__.py
├── webapp_a  # Web application e.g. portal
│   ├── common  # Stuff shared across sections
│   │   ├── __init__.py
│   │   ├── navbar.py
│   │   ├── notifications.py
│   │   └── webapp_a_page.py
│   ├── __init__.py
│   ├── page_a.py  # Flat layout for pages that only require one file
│   ├── page_b.py
│   ├── page_c  # Pages requiring multiple files get a folder
│   │   ├── __init__.py
│   │   ├── page_c_logged_in.py
│   │   ├── page_c_logged_out.py
│   │   ├── page_c.py
│   │   ├── page_part_a_for_page_c.py
│   │   └── page_part_b  # Page parts requiring multiple files get a folder
│   │       ├── __init__.py
│   │       ├── page_part_b_base.py
│   │       ├── page_part_b_type_a.py
│   │       └── page_part_b_type_b.py
│   ├── section_a  # Website sections
│   │   ├── common  # Stuff common to the section go here
│   │   │   ├── __init__.py
│   │   │   ├── page_part_a_for_section.py
│   │   │   ├── page_part_b_for_section.py
│   │   │   └── section_page.py
│   │   ├── __init__.py
│   │   ├── page_a.py
│   │   └── page_b.py
│   │       ├── __init__.py
│   │       ├── page_b_logged_in.py
│   │       ├── page_b_logged_out.py
│   │       ├── page_b.py
│   │       └── page_part_a_for_page_b.py
│   └── section_b  # Another section
└── webapp_b  # Web application e.g. nextcloud
```

It is not possible to predict this structure in advance. Just keep refactoring
as new logical units appear, without breaking existing interfaces. In
general, only the import path should change (and modern IDEs can handle that
automatically for you).
