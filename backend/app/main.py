from __future__ import annotations

from contextlib import asynccontextmanager

from chromadb import PersistentClient
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from fastapi.responses import JSONResponse

from .api.routes import chat_router, health_router, vision_router
from .core.config import get_settings
from .core.errors import AppError
from .core.logger import configure_logging, get_logger
from .core.middleware import RequestLoggingMiddleware
from .database.session import create_engine_and_sessionmaker
from .memory.embeddings.provider import EmbeddingsProviderFactory
from .memory.long_term.repository import SqlMemoryRepository
from .memory.retrieval.chroma import ChromaMemoryStore
from .memory.service import MemoryService
from .memory.short_term.redis_store import RedisSessionRepository
from .tools.registry import build_default_registry
from .tools.executor import ToolExecutor
from .vision.service import VisionService
from .ai.streaming.orchestrator import AIOrchestrator


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    configure_logging(settings.log_level)
    logger = get_logger('gewn.startup')
    logger.info('Booting GEWN backend')

    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    app.state.redis = redis

    engine, sessionmaker = create_engine_and_sessionmaker(settings.database_url)
    app.state.db_engine = engine
    app.state.db_sessionmaker = sessionmaker

    chroma_client = PersistentClient(path=settings.chroma_path)
    app.state.chroma = chroma_client

    embeddings = EmbeddingsProviderFactory.from_settings(settings)
    memory_store = ChromaMemoryStore(chroma_client, embeddings)
    short_term_repo = RedisSessionRepository(
        redis,
        ttl_seconds=settings.session_ttl_seconds,
        max_messages=settings.session_max_messages,
    )
    long_term_repo = SqlMemoryRepository(sessionmaker)
    memory_service = MemoryService(
        short_term_repo=short_term_repo,
        long_term_repo=long_term_repo,
        memory_store=memory_store,
        embeddings=embeddings,
        context_limit=settings.session_context_limit,
        similarity_k=settings.memory_similarity_k,
    )
    app.state.memory_service = memory_service

    tool_registry = build_default_registry()
    app.state.tool_registry = tool_registry
    app.state.tool_executor = ToolExecutor(tool_registry)

    vision_service = VisionService(settings)
    app.state.vision_service = vision_service

    ai_orchestrator = AIOrchestrator(settings)
    app.state.ai_orchestrator = ai_orchestrator

    yield

    logger.info('Shutting down GEWN backend')
    await redis.aclose()
    await engine.dispose()


app = FastAPI(title='GEWN', lifespan=lifespan)
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_middleware(RequestLoggingMiddleware)

app.include_router(health_router, prefix=settings.api_prefix, tags=['health'])
app.include_router(vision_router, prefix=settings.api_prefix, tags=['vision'])
app.include_router(chat_router, tags=['chat'])


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_response().model_dump(),
    )
