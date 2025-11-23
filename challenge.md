# Odoo 18 Development Challenge - Day 1 Summary
**Topic:** Environment Setup, Architecture, and Deep Technical Theory

## 1. Infrastructure & Docker Setup
We established a professional, containerized development environment using Docker to ensure isolation and reproducibility.

*   **The Stack:**
    *   **Database:** PostgreSQL 15 (Required for Odoo 18 performance features).
    *   **Server:** Odoo 18.0 (Python 3.11+ based).
    *   **OS:** Linux (Debian-based) running inside Docker containers.

*   **The `docker-compose.yml` Blueprint:**
    *   **Services:** Defined `db` (Postgres) and `web` (Odoo).
    *   **Ports:**
        *   `8069`: Main HTTP traffic (UI/Buttons).
        *   `8072`: Long-polling/WebSockets (Live Chat, Notifications).
        *   `5432`: Exposed for direct Database access (for tools like DBeaver).
    *   **Volumes (Persistence):**
        *   `./addons:/mnt/extra-addons`: Maps local code to the server.
        *   `./config:/etc/odoo`: Maps local configuration.
        *   `odoo-db-data`: Persists SQL data (Customers, Invoices).
        *   `odoo-web-data`: Persists the **Filestore** (Images, PDFs, Attachments) and **Sessions**.

*   **Commands:**
    *   `docker-compose up -d`: Start services in background.
    *   `docker-compose down -v`: "Nuke it" command (Stops services AND deletes data volumes).
    *   `docker exec -it <container> <command>`: Run a command inside the running container.

## 2. Configuration (`odoo.conf`)
We replaced command-line flags with a robust configuration file to mimic a "Senior Dev" setup.

*   **Security:** `admin_passwd` sets the Master Password for DB management.
*   **Performance (Dev Mode):**
    *   `workers = 0`: Enables "Threaded Mode". Essential for using debuggers (`pdb`).
    *   `limit_time_cpu = 600`: Increases timeout to 10 minutes to prevent crashes while debugging.
*   **Network:** `proxy_mode = True` ensures Odoo resolves real user IPs behind Docker.
*   **Logging:** `log_handler` allows filtering noise (e.g., silencing `werkzeug` while keeping custom module logs).

## 3. Odoo Architecture & Internals
We deconstructed the "3-Tier Architecture" and looked under the hood.

*   **The "Brain" (Server Stack):**
    *   **Werkzeug:** The WSGI server that acts as the doorman, translating HTTP requests into Python objects.
    *   **Controllers:** The entry points for public web traffic (`@http.route`).
    *   **ORM (Object-Relational Mapping):** Translates Python objects (`partner.name`) into SQL (`UPDATE...`).

*   **The "Memory" (Data Storage):**
    *   **Structured Data:** Text/Numbers go to **PostgreSQL**.
    *   **Unstructured Data:** Images/PDFs go to the **Filestore** on disk.
    *   **Linkage:** The DB stores the *filename path*, not the actual file.
    *   **Sessions:** User login sessions are stored as **Files** on disk, not in the DB (for speed).

*   **The "Pulse" (Boot Process):**
    1.  **CLI/Config Parse:** Reads settings.
    2.  **DB Connect:** Establishes link to Postgres.
    3.  **Module Graph:** Loads modules based on `depends` tree.
    4.  **Registry:** Compiles Python classes into memory (Single Instance Pattern).
    5.  **Server Start:** Opens ports 8069/8072.

## 4. Developer Workflow & Best Practices
Key workflows to distinguish a Senior Developer from a Beginner.

*   **The "Golden Rule" of Updating:**
    *   Change **Python** → **Restart Server** (Classes loaded in RAM).
    *   Change **XML** → **Upgrade Module** (Data stored in DB `ir_ui_view`).
    *   Change **JS/CSS** → **Refresh Browser** (Static assets).

*   **IDE Setup (VS Code):**
    *   Map the external Odoo source code in `.vscode/settings.json` (`extraPaths`) to enable IntelliSense/Auto-complete.

*   **Debugging:**
    *   Use `import pdb; pdb.set_trace()` to pause execution and inspect variables in the terminal.
    *   Do not use `print()` for complex logic.

*   **The Shell:**
    *   `odoo-bin shell`: Opens a Python console with the Odoo environment loaded.
    *   `self.env`: The gateway to the database.

## 5. The Odoo Philosophy ("Everything is a Record")
The fundamental concept that drives Odoo's flexibility.

*   **The Concept:** Not just business data, but **System Configuration** is also data stored in tables.
    *   **Users:** Rows in `res_users`.
    *   **Menus:** Rows in `ir_ui_menu`.
    *   **Views:** Rows in `ir_ui_view`.
    *   **Access Rights:** Rows in `ir_model_access`.

*   **XML IDs (External IDs):**
    *   The string alias (e.g., `base.user_admin`) that links code to a specific database row (ID `2`).
    *   Stored in `ir.model.data`.
    *   **Crucial:** Never use Integer IDs (like `id=2`) in code; always use XML IDs.

## 6. Performance Mechanics
How Odoo achieves speed despite being dynamic.

*   **Registry:** Models are loaded into RAM once at boot.
*   **ormcache:** Results of pure functions (like permission checks) are memoized in RAM.
*   **Prefetching:** The ORM automatically fetches related records (batching) to solve the "N+1 Query" problem.
*   **Assets:** JS/CSS are minified and cached by the browser.

## 7. Odoo vs. SAP
*   **Odoo:** Disk-based DB (Postgres), Python-based, Modular/Agile, Low Cost, "Honda Civic Type-R".
*   **SAP:** In-Memory DB (HANA), ABAP-based, Rigid/Process-centric, High Cost, "Formula 1 Car".