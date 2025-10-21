"""
Configuración de autenticación simplificada para desarrollo local.
Esta versión no requiere Supabase ni tokens JWT.
"""

from langgraph_sdk import Auth
from langgraph_sdk.auth.types import StudioUser
from typing import Optional, Any

# The "Auth" object is a container that LangGraph will use to mark our authentication function
auth = Auth()


# The `authenticate` decorator tells LangGraph to call this function as middleware
# for every request. This will determine whether the request is allowed or not
@auth.authenticate
async def get_current_user(authorization: str | None) -> Auth.types.MinimalUserDict:
    """Simplified authentication for local development - allows all requests."""
    
    # For local development, we'll allow all requests without authentication
    # This bypasses the need for Supabase or JWT tokens
    return {
        "identity": "local-dev-user",
    }


@auth.on.threads.create
@auth.on.threads.create_run
async def on_thread_create(
    ctx: Auth.types.AuthContext,
    value: Auth.types.on.threads.create.value,
):
    """Add owner when creating threads for local development."""

    if isinstance(ctx.user, StudioUser):
        return

    # Add owner metadata to the thread being created
    metadata = value.setdefault("metadata", {})
    metadata["owner"] = ctx.user.identity


@auth.on.threads.read
@auth.on.threads.delete
@auth.on.threads.update
@auth.on.threads.search
async def on_thread_read(
    ctx: Auth.types.AuthContext,
    value: Auth.types.on.threads.read.value,
):
    """Allow reading threads for local development."""

    if isinstance(ctx.user, StudioUser):
        return

    return {"owner": ctx.user.identity}


@auth.on.assistants.create
async def on_assistants_create(
    ctx: Auth.types.AuthContext,
    value: Auth.types.on.assistants.create.value,
):
    """Allow creating assistants for local development."""
    
    if isinstance(ctx.user, StudioUser):
        return

    # Add owner metadata to the assistant being created
    metadata = value.setdefault("metadata", {})
    metadata["owner"] = ctx.user.identity


@auth.on.assistants.read
@auth.on.assistants.delete
@auth.on.assistants.update
@auth.on.assistants.search
async def on_assistants_read(
    ctx: Auth.types.AuthContext,
    value: Auth.types.on.assistants.read.value,
):
    """Allow reading assistants for local development."""

    if isinstance(ctx.user, StudioUser):
        return

    return {"owner": ctx.user.identity}


@auth.on.store()
async def authorize_store(ctx: Auth.types.AuthContext, value: dict):
    """Allow store access for local development."""
    
    if isinstance(ctx.user, StudioUser):
        return

    # For local development, allow all store access
    pass
