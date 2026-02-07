"""Chat routes for AI chatbot."""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session, select
from typing import Optional
from pydantic import BaseModel
from app.database import get_session
from app.models import Conversation, Message, User
from app.auth import decode_token
from app.agents.todo_agent import run_agent

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    """Chat request model."""
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    """Chat response model."""
    conversation_id: int
    response: str
    tool_calls: list[str] = []


def get_current_user_id(authorization: Optional[str] = Header(None)) -> int:
    """Extract user_id from JWT token."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    
    try:
        token = authorization.split(" ")[1]  # Remove "Bearer " prefix
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )
    
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user_id"
        )
    
    return int(user_id)


def verify_user_access(user_id: int, token_user_id: int):
    """Verify that token user_id matches requested user_id."""
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch"
        )


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: int,
    request: ChatRequest,
    session: Session = Depends(get_session),
    token_user_id: int = Depends(get_current_user_id)
):
    """Chat endpoint for AI assistant."""
    verify_user_access(user_id, token_user_id)
    
    # Get or create conversation
    if request.conversation_id:
        statement = select(Conversation).where(
            Conversation.id == request.conversation_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(statement).first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    else:
        # Create new conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
    
    # Load conversation history from database (before adding new message)
    statement = select(Message).where(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at)
    messages = session.exec(statement).all()
    
    # Convert to OpenAI format
    conversation_history = [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]
    
    # Call agent (this will use tools that modify the database)
    try:
        assistant_response, tool_calls = await run_agent(
            user_id=str(user_id),
            user_message=request.message,
            conversation_history=conversation_history,
            session=session
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calling AI agent: {str(e)}"
        )
    
    # Save user message (after agent call, so it's in the same transaction)
    user_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content=request.message
    )
    session.add(user_message)
    
    # Save assistant response
    assistant_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="assistant",
        content=assistant_response
    )
    session.add(assistant_message)
    
    # Update conversation timestamp
    from datetime import datetime
    conversation.updated_at = datetime.utcnow()
    session.add(conversation)
    
    # Commit everything at once (user message, assistant message, and any task changes from tools)
    session.commit()
    
    return ChatResponse(
        conversation_id=conversation.id,
        response=assistant_response,
        tool_calls=tool_calls
    )

