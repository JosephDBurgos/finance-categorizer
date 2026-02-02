# Database Schema Overview

This document provides an overview of the database schema, including the tables and their purposes.

| **Table Name**            | **Purpose**                                                                |
| ------------------------- | -------------------------------------------------------------------------- |
| **workspaces**            | Represents a logical grouping or container for resources, data, and users. |
| **users**                 | Represents individual users who interact with the system.                  |
| **workspace_memberships** | Links users to workspaces and defines their roles (e.g., admin, member).   |
| **accounts**              | Represents financial accounts associated with a workspace.                 |
| **ingest_artifacts**      | Tracks uploaded files or data ingested into the system.                    |
| **transactions**          | Stores financial transactions, including metadata and categorization.      |
| **rules**                 | Defines categorization rules for transactions.                             |
| **manual_overrides**      | Tracks manual changes to transactions, including old and new values.       |
| **audit_events**          | Logs events for auditing purposes.                                         |

## Table Details

### **workspaces**

- **Purpose**: Represents a logical grouping or container for resources, data, and users.
- **Key Columns**:
  - `id`: Unique identifier for the workspace.
  - `name`: Name of the workspace.
  - `slug`: URL-friendly identifier for the workspace.
  - `primary_admin_user_id`: References the primary admin user.
  - `data_retention_days`: Specifies how long data is retained.

### **users**

- **Purpose**: Represents individual users who interact with the system.
- **Key Columns**:
  - `id`: Unique identifier for the user.
  - `email`: User's email address.
  - `full_name`: User's full name.
  - `mfa_status`: Multi-factor authentication status.
  - `last_login`: Timestamp of the user's last login.

### **workspace_memberships**

- **Purpose**: Links users to workspaces and defines their roles.
- **Key Columns**:
  - `workspace_id`: References the workspace.
  - `user_id`: References the user.
  - `role`: Role of the user in the workspace (e.g., admin, member).

### **accounts**

- **Purpose**: Represents financial accounts associated with a workspace.
- **Key Columns**:
  - `id`: Unique identifier for the account.
  - `workspace_id`: References the workspace.
  - `institution_name`: Name of the financial institution.
  - `account_mask`: Masked account number.

### **ingest_artifacts**

- **Purpose**: Tracks uploaded files or data ingested into the system.
- **Key Columns**:
  - `id`: Unique identifier for the artifact.
  - `workspace_id`: References the workspace.
  - `account_id`: References the account.
  - `checksum`: Checksum of the file.
  - `storage_path`: Path to the stored file.

### **transactions**

- **Purpose**: Stores financial transactions, including metadata and categorization.
- **Key Columns**:
  - `transaction_id`: Unique identifier for the transaction.
  - `workspace_id`: References the workspace.
  - `amount`: Transaction amount.
  - `currency`: Currency of the transaction.
  - `description_raw`: Raw description of the transaction.
  - `category`: Categorization of the transaction.

### **rules**

- **Purpose**: Defines categorization rules for transactions.
- **Key Columns**:
  - `id`: Unique identifier for the rule.
  - `workspace_id`: References the workspace.
  - `pattern`: Pattern to match for categorization.
  - `output_category`: Category to assign.

### **manual_overrides**

- **Purpose**: Tracks manual changes to transactions, including old and new values.
- **Key Columns**:
  - `id`: Unique identifier for the override.
  - `transaction_id`: References the transaction.
  - `field`: Field that was changed.
  - `old_value`: Previous value.
  - `new_value`: New value.

### **audit_events**

- **Purpose**: Logs events for auditing purposes.
- **Key Columns**:
  - `id`: Unique identifier for the event.
  - `workspace_id`: References the workspace.
  - `actor_user_id`: References the user who performed the action.
  - `event_type`: Type of event.
  - `event_payload`: Details of the event.
