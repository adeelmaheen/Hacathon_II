"""OpenAI Agent for Todo Management."""
import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from app.config import settings
from app.mcp import tools

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a helpful todo assistant. You help users manage their tasks through natural conversation.

Your capabilities:
- Create tasks when user mentions adding/creating/remembering something
- List tasks when user asks to see/show/view tasks
- Update tasks when user wants to change/modify/edit
- Delete tasks when user says remove/delete/cancel
- Complete tasks when user says done/finished/complete

Guidelines:
- Always confirm actions with friendly, concise messages
- When listing tasks, format them clearly with numbers
- If the user's intent is unclear, ask for clarification
- Be conversational and helpful
- Use emojis sparingly (✓ for confirmations)
- When completing tasks, mention the task title

Examples:
User: "Add a task to buy groceries"
You: "✓ I've added 'Buy groceries' to your tasks!"

User: "Show me all my pending tasks"
You: "You have 3 pending tasks:
1. Buy groceries
2. Call mom
3. Finish report"

User: "Mark task 1 as complete"
You: "✓ 'Buy groceries' marked as complete!"
"""

# Tool definitions for OpenAI
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "The task title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description",
                        "default": ""
                    }
                },
                "required": ["user_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List tasks for the user. Can filter by status: all, pending, or completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's ID"
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by status: 'all', 'pending', or 'completed'",
                        "enum": ["all", "pending", "completed"],
                        "default": "all"
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update a task's title or description",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's ID"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The task ID to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title (optional)"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description (optional)"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's ID"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The task ID to delete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Toggle task completion status (mark as done or pending)",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's ID"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The task ID to toggle"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    }
]

# Tool mapping
TOOL_MAP = {
    "add_task": tools.add_task,
    "list_tasks": tools.list_tasks,
    "update_task": tools.update_task,
    "delete_task": tools.delete_task,
    "complete_task": tools.complete_task,
}


async def run_agent(
    user_id: str,
    user_message: str,
    conversation_history: List[Dict[str, str]] = None,
    session = None
) -> tuple[str, List[str]]:
    """
    Run the OpenAI agent with tool calling.
    
    Args:
        user_id: User ID
        user_message: User's message
        conversation_history: Previous messages in the conversation
    
    Returns:
        Tuple of (assistant_response, list_of_tool_calls)
    """
    if conversation_history is None:
        conversation_history = []
    
    # Build messages array
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    
    # Add conversation history
    messages.extend(conversation_history)
    
    # Add current user message
    messages.append({"role": "user", "content": user_message})
    
    tool_calls_made = []
    max_iterations = 5  # Prevent infinite loops
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using cheaper model, can upgrade to gpt-4 if needed
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        messages.append(assistant_message.model_dump())
        
        # Check if tool calls are needed
        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Add user_id to all tool calls
                function_args["user_id"] = user_id
                
                tool_calls_made.append(function_name)
                
                # Execute tool
                tool_func = TOOL_MAP.get(function_name)
                if tool_func:
                    try:
                        # Pass session if available
                        if session is not None:
                            function_args["session"] = session
                        tool_result = await tool_func(**function_args)
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": json.dumps(tool_result)
                        })
                    except Exception as e:
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": json.dumps({"status": "error", "message": str(e)})
                        })
                else:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": json.dumps({"status": "error", "message": f"Unknown tool: {function_name}"})
                    })
        else:
            # No more tool calls, return the response
            return assistant_message.content, tool_calls_made
    
    # If we've done too many iterations, return the last message
    if messages:
        last_message = messages[-1]
        if isinstance(last_message, dict) and "content" in last_message:
            return last_message["content"], tool_calls_made
    
    return "I apologize, but I encountered an issue processing your request.", tool_calls_made

