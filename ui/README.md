# UI Directory

This directory contains all Streamlit-related code for the FinFriend application, organized into a clear structure that separates different UI concerns.

## Directory Structure

- **components/**: Reusable UI components that can be used across multiple pages
  - `sidebar.py`: Sidebar component used on all pages with navigation and controls

- **interactions/**: Handlers for UI interactions that connect the UI to services
  - `chat_handler.py`: Handles chat interactions with the LLM service, including conversation management and CSV utilities

- **layouts/**: Page layout helpers for consistent UI structure
  - (To be populated as needed)

## Usage

Import components and interaction handlers as needed in your Streamlit pages:

```python
# Import a UI component
import ui.components.sidebar

# Import an interaction handler
from ui.interactions import chat_handler

# Use the component
ui.components.sidebar.show()

# Use the interaction handler
messages = await chat_handler.run_conversation(messages, message_placeholder)
```

## Design Principles

1. **Separation of Concerns**: UI code is separated from business logic (services)
2. **Reusability**: Components are designed to be reused across multiple pages
3. **Consistency**: Common UI patterns are encapsulated in reusable components
4. **Maintainability**: Clear organization makes it easier to find and modify code

## Migration from helpers/

This structure replaces the previous `helpers/` directory:
- `helpers/sidebar.py` → `ui/components/sidebar.py`
- `helpers/util.py` → `ui/interactions/chat_handler.py`
