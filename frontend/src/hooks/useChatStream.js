import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { WSClient } from '../services/wsClient'

const STREAM_EVENTS = {
  start: 'stream_start',
  token: 'token',
  toolCall: 'tool_call',
  toolResult: 'tool_result',
  complete: 'stream_complete',
  error: 'stream_error',
  cancel: 'cancelled',
}

const CONNECTION_STATES = {
  connecting: 'Connecting',
  connected: 'Connected',
  disconnected: 'Reconnecting',
}

const STREAM_PHASES = {
  idle: 'idle',
  starting: 'starting',
  streaming: 'streaming',
}

const buildId = () => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID()
  }
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`
}

const getWsBaseUrl = () =>
  import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

const buildChatUrl = (sessionId) => `${getWsBaseUrl()}/ws/chat/${sessionId}`

export default function useChatStream() {
  const sessionIdRef = useRef(buildId())
  const clientRef = useRef(null)
  const streamMapRef = useRef(new Map())
  const [messages, setMessages] = useState([])
  const [connectionState, setConnectionState] = useState(
    CONNECTION_STATES.connecting
  )
  const [streamPhase, setStreamPhase] = useState(STREAM_PHASES.idle)
  const [activeCorrelationId, setActiveCorrelationId] = useState(null)
  const [pendingApprovals, setPendingApprovals] = useState([])

  const appendMessage = useCallback((message) => {
    setMessages((prev) => [...prev, message])
  }, [])

  const updateMessage = useCallback((messageId, updater) => {
    setMessages((prev) =>
      prev.map((message) =>
        message.id === messageId ? updater(message) : message
      )
    )
  }, [])

  const handleStreamEvent = useCallback(
    (data) => {
      const { event, correlation_id: snakeId, correlation_id, correlationId } =
        data
      const correlation = correlationId || correlation_id || snakeId
      const payload = data.payload || {}

      if (!event || !correlation) {
        return
      }

      if (event === STREAM_EVENTS.start) {
        const messageId = payload.message_id || payload.messageId || buildId()
        streamMapRef.current.set(correlation, messageId)
        appendMessage({
          id: messageId,
          role: 'assistant',
          content: '',
          createdAt: new Date().toISOString(),
          correlationId: correlation,
          status: 'streaming',
        })
        setStreamPhase(STREAM_PHASES.streaming)
        setActiveCorrelationId(correlation)
        return
      }

      if (event === STREAM_EVENTS.toolCall) {
        const toolMessageId = payload.tool_call_id || buildId()
        appendMessage({
          id: toolMessageId,
          role: 'tool',
          status: payload.requires_approval ? 'requires_approval' : 'pending',
          tool: {
            id: toolMessageId,
            name: payload.tool_name,
            status: payload.requires_approval ? 'requires_approval' : 'pending',
            riskTier: payload.risk_tier,
            confirmationType: payload.confirmation_type,
            confirmationText: payload.confirmation_text,
            details: payload.arguments,
          },
        })
        if (payload.requires_approval) {
          setPendingApprovals((prev) => [
            ...prev,
            {
              id: toolMessageId,
              name: payload.tool_name,
              confirmationType: payload.confirmation_type,
              confirmationText: payload.confirmation_text,
              details: payload.arguments,
            },
          ])
        }
        return
      }

      if (event === STREAM_EVENTS.toolResult) {
        const toolId = payload.tool_call_id
        updateMessage(toolId, (message) => ({
          ...message,
          status: payload.status,
          tool: {
            ...(message.tool || {}),
            status: payload.status,
            details: payload.result,
          },
        }))
        setPendingApprovals((prev) =>
          prev.filter((tool) => tool.id !== toolId)
        )
        return
      }

      const messageId = streamMapRef.current.get(correlation)
      if (!messageId) {
        return
      }

      if (event === STREAM_EVENTS.token) {
        const token = payload.token || ''
        updateMessage(messageId, (message) => ({
          ...message,
          content: `${message.content}${token}`,
        }))
        return
      }

      if (event === STREAM_EVENTS.complete) {
        updateMessage(messageId, (message) => ({
          ...message,
          status: 'complete',
        }))
        setStreamPhase(STREAM_PHASES.idle)
        setActiveCorrelationId(null)
        return
      }

      if (event === STREAM_EVENTS.cancel) {
        updateMessage(messageId, (message) => ({
          ...message,
          status: 'cancelled',
        }))
        setStreamPhase(STREAM_PHASES.idle)
        setActiveCorrelationId(null)
        return
      }

      if (event === STREAM_EVENTS.error) {
        updateMessage(messageId, (message) => ({
          ...message,
          status: 'error',
        }))
        setStreamPhase(STREAM_PHASES.idle)
        setActiveCorrelationId(null)
      }
    },
    [appendMessage, updateMessage]
  )

  useEffect(() => {
    const url = buildChatUrl(sessionIdRef.current)
    const client = new WSClient(url, {
      onOpen: () => setConnectionState(CONNECTION_STATES.connected),
      onClose: () => setConnectionState(CONNECTION_STATES.disconnected),
      onError: () => setConnectionState(CONNECTION_STATES.disconnected),
      onMessage: (event) => {
        const data = JSON.parse(event.data)
        if (data.event) {
          handleStreamEvent(data)
        }
      },
    })

    client.connect()
    clientRef.current = client

    return () => client.close()
  }, [handleStreamEvent])

  const sendMessage = useCallback(
    (content, { includeScreen } = {}) => {
      const correlationId = buildId()
      appendMessage({
        id: buildId(),
        role: 'user',
        content,
        createdAt: new Date().toISOString(),
        correlationId,
        status: 'complete',
      })
      setStreamPhase(STREAM_PHASES.starting)
      setActiveCorrelationId(correlationId)
      clientRef.current?.send({
        event: 'chat.message',
        content,
        correlation_id: correlationId,
        include_screen: Boolean(includeScreen),
      })
    },
    [appendMessage]
  )

  const approveTool = useCallback((toolCallId, confirmationText) => {
    clientRef.current?.send({
      event: 'tool.approve',
      tool_call_id: toolCallId,
      confirmation_text: confirmationText,
    })
  }, [])

  const denyTool = useCallback((toolCallId) => {
    clientRef.current?.send({
      event: 'tool.deny',
      tool_call_id: toolCallId,
    })
    updateMessage(toolCallId, (message) => ({
      ...message,
      status: 'denied',
      tool: {
        ...(message.tool || {}),
        status: 'denied',
      },
    }))
    setPendingApprovals((prev) => prev.filter((tool) => tool.id !== toolCallId))
  }, [updateMessage])

  const cancelStream = useCallback(() => {
    if (!activeCorrelationId) {
      return
    }
    clientRef.current?.send({
      event: 'chat.cancel',
      correlation_id: activeCorrelationId,
    })
    setStreamPhase(STREAM_PHASES.idle)
    setActiveCorrelationId(null)
  }, [activeCorrelationId])

  const isStreaming = useMemo(
    () => streamPhase !== STREAM_PHASES.idle,
    [streamPhase]
  )

  return {
    messages,
    isStreaming,
    streamPhase,
    connectionState,
    sessionId: sessionIdRef.current,
    pendingApprovals,
    sendMessage,
    approveTool,
    denyTool,
    cancelStream,
  }
}
