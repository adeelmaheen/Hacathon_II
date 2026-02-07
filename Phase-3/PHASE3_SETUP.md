# Phase III Setup Guide - AI Chatbot Integration

## ✅ What's Been Completed

All Phase III code has been implemented! You now have:

1. ✅ **Backend Chat Endpoint** - `/api/{user_id}/chat`
2. ✅ **OpenAI Agent** - Natural language understanding with tool calling
3. ✅ **MCP Tools** - 5 tools for task management
4. ✅ **Database Models** - Conversation and Message models
5. ✅ **Frontend Chat Page** - Beautiful chat interface at `/chat`
6. ✅ **Navigation** - Chat link added to dashboard

## 🚀 Setup Steps

### Step 1: Get OpenAI API Key

1. Go to https://platform.openai.com
2. Sign up or log in
3. Navigate to: **Settings → API Keys**
4. Click **"Create new secret key"**
5. Name it: `todo-chatbot`
6. **Copy the key immediately** (you won't see it again!)

### Step 2: Configure Backend

Add the OpenAI API key to your backend `.env` file:

```bash
cd backend
```

Edit `.env` file and add:

```env
DATABASE_URL=your-neon-url
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx  # Your OpenAI API key here
```

### Step 3: Restart Backend

The backend should auto-reload, but if not:

```bash
cd backend
# Stop current server (Ctrl+C)
uv run uvicorn app.main:app --reload --port 8000
```

### Step 4: Test the Chat

1. **Start Frontend** (if not running):
   ```bash
   cd frontend
   npm run dev
   ```

2. **Open Browser**: http://localhost:3000

3. **Login** to your account

4. **Click "💬 Chat Assistant"** button on dashboard

5. **Try these commands**:
   - "Add a task to buy groceries"
   - "Show me all my tasks"
   - "Mark task 1 as complete"
   - "Delete task 2"

## 🧪 Testing Checklist

### Basic Functionality
- [ ] Chat page loads correctly
- [ ] Can send messages
- [ ] Bot responds with helpful messages
- [ ] Messages persist (refresh page, messages still there)

### Task Operations via Chat
- [ ] "Add task to [something]" → Task created
- [ ] "Show my tasks" → List displayed
- [ ] "Mark task 1 complete" → Task marked complete
- [ ] "Delete task 2" → Task deleted
- [ ] "Change task 1 to [new title]" → Task updated

### Integration
- [ ] Task created via chat appears in dashboard
- [ ] Task completed via chat updates in dashboard
- [ ] Task deleted via chat disappears from dashboard

## 💡 Example Conversations

### Adding Tasks
```
You: Add a task to buy groceries
Bot: ✓ I've added 'Buy groceries' to your tasks!

You: I need to remember to call mom
Bot: ✓ I've added 'Call mom' to your tasks!

You: Create a todo for finishing the report
Bot: ✓ I've added 'Finish the report' to your tasks!
```

### Viewing Tasks
```
You: Show me all my tasks
Bot: You have 3 tasks:
1. Buy groceries (pending)
2. Call mom (pending)
3. Finish the report (pending)

You: What do I need to do?
Bot: You have 3 pending tasks:
1. Buy groceries
2. Call mom
3. Finish the report
```

### Completing Tasks
```
You: Mark task 1 as complete
Bot: ✓ 'Buy groceries' marked as complete!

You: I finished the report
Bot: ✓ 'Finish the report' marked as complete!
```

### Updating Tasks
```
You: Change task 1 title to "Buy milk and bread"
Bot: ✓ Task 'Buy milk and bread' updated successfully!
```

### Deleting Tasks
```
You: Delete task 2
Bot: ✓ Task 'Call mom' deleted successfully!
```

## 🐛 Troubleshooting

### Error: "OPENAI_API_KEY not found"
- **Solution**: Make sure you added `OPENAI_API_KEY` to backend `.env` file
- Restart the backend server

### Error: "Unauthorized" or "Invalid API key"
- **Solution**: 
  - Check your OpenAI API key is correct
  - Make sure you have credits in your OpenAI account
  - Visit https://platform.openai.com/usage to check balance

### Bot doesn't respond
- **Solution**:
  - Check backend logs for errors
  - Verify OpenAI API key is valid
  - Check network tab in browser for API errors

### Bot responds but doesn't execute actions
- **Solution**:
  - Check backend logs - tool calls should appear
  - Verify database connection is working
  - Check that user_id is being passed correctly

### Chat messages don't persist
- **Solution**:
  - Check database connection
  - Verify Conversation and Message tables exist
  - Check backend logs for database errors

## 📊 Architecture

```
User Browser (/chat)
    ↓ POST /api/{user_id}/chat
FastAPI Backend
    ↓
OpenAI Agent (gpt-4o-mini)
    ↓ Tool Calls
MCP Tools
    ↓ Database Operations
Neon PostgreSQL
    ↓
Response back to user
```

## 🎯 Next Steps

Once everything is working:

1. **Test extensively** - Try 20+ different phrasings
2. **Check dashboard integration** - Verify tasks sync correctly
3. **Test conversation persistence** - Refresh page, continue chat
4. **Deploy to production** - Add OPENAI_API_KEY to Railway/Render

## 💰 Cost Estimate

Using `gpt-4o-mini`:
- ~$0.15 per 1M input tokens
- ~$0.60 per 1M output tokens
- Average conversation: ~500 tokens
- **Cost per conversation: ~$0.0003** (very cheap!)

With $5 free credit, you can have **~16,000 conversations**!

## 🎉 You're Done!

Phase III is complete! Your todo app now has:
- ✅ Natural language task management
- ✅ AI-powered conversational interface
- ✅ Persistent conversation history
- ✅ Full integration with dashboard

Enjoy your AI-powered todo app! 🚀

