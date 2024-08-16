# Code Structure of the Test Suite

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
