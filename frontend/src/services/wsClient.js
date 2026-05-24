const DEFAULT_BACKOFF_MS = 800
const MAX_BACKOFF_MS = 8000

export class WSClient {
  constructor(url, { onMessage, onOpen, onClose, onError, reconnect = true } = {}) {
    this.url = url
    this.onMessage = onMessage
    this.onOpen = onOpen
    this.onClose = onClose
    this.onError = onError
    this.reconnect = reconnect
    this._ws = null
    this._queue = []
    this._retries = 0
    this._shouldReconnect = true
    this._reconnectTimer = null
  }

  connect() {
    this._shouldReconnect = true
    this._connect()
  }

  _connect() {
    if (!this._shouldReconnect) {
      return
    }

    this._ws = new WebSocket(this.url)

    this._ws.onopen = () => {
      this._retries = 0
      if (this.onOpen) {
        this.onOpen()
      }
      this._flushQueue()
    }

    this._ws.onmessage = (event) => {
      if (this.onMessage) {
        this.onMessage(event)
      }
    }

    this._ws.onerror = (event) => {
      if (this.onError) {
        this.onError(event)
      }
    }

    this._ws.onclose = () => {
      if (this.onClose) {
        this.onClose()
      }
      if (this.reconnect) {
        this._scheduleReconnect()
      }
    }
  }

  _scheduleReconnect() {
    if (!this._shouldReconnect) {
      return
    }
    const delay = Math.min(
      DEFAULT_BACKOFF_MS * 2 ** this._retries,
      MAX_BACKOFF_MS
    )
    const jitter = Math.floor(Math.random() * 250)
    this._retries += 1
    if (this._reconnectTimer) {
      clearTimeout(this._reconnectTimer)
    }
    this._reconnectTimer = setTimeout(() => this._connect(), delay + jitter)
  }

  _flushQueue() {
    if (!this._ws || this._ws.readyState !== WebSocket.OPEN) {
      return
    }
    while (this._queue.length > 0) {
      const payload = this._queue.shift()
      this._ws.send(payload)
    }
  }

  send(data) {
    const payload = JSON.stringify(data)
    if (this._ws && this._ws.readyState === WebSocket.OPEN) {
      this._ws.send(payload)
      return
    }
    this._queue.push(payload)
  }

  close() {
    this._shouldReconnect = false
    if (this._reconnectTimer) {
      clearTimeout(this._reconnectTimer)
    }
    if (this._ws) {
      this._ws.close()
    }
  }
}
