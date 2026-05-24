import { useEffect, useMemo, useRef, useState } from 'react'
import './App.css'
import { AnimatePresence, motion } from 'framer-motion'
import ChatInput from './components/chat/ChatInput'
import ChatMessage from './components/chat/ChatMessage'
import Header from './components/common/Header'
import PermissionModal from './components/modals/PermissionModal'
import SettingsPanel from './features/settings/SettingsPanel'
import useChatStream from './hooks/useChatStream'

const panelMotion = {
  initial: { opacity: 0, y: 24, scale: 0.98 },
  animate: { opacity: 1, y: 0, scale: 1 },
  transition: { duration: 0.7, ease: [0.16, 1, 0.3, 1] },
}

function App() {
  const [input, setInput] = useState('')
  const [includeScreen, setIncludeScreen] = useState(false)
  const [screenStatus, setScreenStatus] = useState('Off')
  const [settingsOpen, setSettingsOpen] = useState(false)
  const bottomRef = useRef(null)
  const {
    messages,
    isStreaming,
    streamPhase,
    connectionState,
    sessionId,
    pendingApprovals,
    sendMessage,
    approveTool,
    denyTool,
    cancelStream,
  } = useChatStream()

  const headerStatus = useMemo(() => {
    if (connectionState === 'Connected') {
      return 'Connected'
    }
    return connectionState
  }, [connectionState])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages, isStreaming])

  const handleSend = () => {
    const trimmed = input.trim()
    if (!trimmed || isStreaming) {
      return
    }
    sendMessage(trimmed, { includeScreen })
    setInput('')
  }

  const handleCaptureScreen = async () => {
    const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
    setScreenStatus('Capturing')
    try {
      await fetch(`${apiBase}/vision/capture`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId }),
      })
      setScreenStatus('Captured')
    } catch (error) {
      setScreenStatus('Error')
    }
  }

  const pendingTool = pendingApprovals[0]

  return (
    <div className="relative h-screen w-screen overflow-hidden bg-transparent text-slate-100">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute -top-24 left-1/2 h-72 w-[520px] -translate-x-1/2 rounded-full bg-violet-500/25 blur-[140px]" />
        <div className="absolute bottom-[-140px] right-[-80px] h-72 w-72 rounded-full bg-cyan-400/20 blur-[120px]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(99,102,241,0.15),transparent_55%)]" />
      </div>

      <main className="relative flex h-full w-full items-center justify-center p-6 sm:p-10">
        <motion.section
          {...panelMotion}
          className="flex h-[82vh] max-h-[860px] w-full max-w-[920px] flex-col rounded-3xl border border-white/10 bg-white/5 p-6 shadow-[0_0_80px_rgba(59,130,246,0.18)] backdrop-blur-2xl sm:p-8"
        >
          <Header
            status={headerStatus}
            memoryStatus="On"
            visionStatus={screenStatus}
            onOpenSettings={() => setSettingsOpen(true)}
          />

          <div className="mt-6 flex min-h-0 flex-1 flex-col overflow-hidden">
            <div className="flex-1 overflow-y-auto pr-2">
              <div className="flex flex-col gap-4">
                <AnimatePresence initial={false}>
                  {messages.map((message) => (
                    <ChatMessage key={message.id} message={message} />
                  ))}
                </AnimatePresence>
                <AnimatePresence>
                  {isStreaming && streamPhase === 'starting' && (
                    <motion.div
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 6 }}
                      className="flex items-center justify-start"
                    >
                      <div className="flex items-center gap-2 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-xs text-slate-300 shadow-[0_0_24px_rgba(148,163,184,0.2)]">
                        <span className="text-slate-400">GEWN typing</span>
                        <div className="flex gap-1">
                          {[0, 1, 2].map((index) => (
                            <motion.span
                              key={index}
                              className="h-1.5 w-1.5 rounded-full bg-slate-400"
                              animate={{ opacity: [0.3, 1, 0.3] }}
                              transition={{
                                duration: 1,
                                repeat: Infinity,
                                delay: index * 0.2,
                              }}
                            />
                          ))}
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
                <div ref={bottomRef} />
              </div>
            </div>

            <div className="pt-4">
              <ChatInput
                value={input}
                onChange={setInput}
                onSend={handleSend}
                isLoading={isStreaming}
                includeScreen={includeScreen}
                onToggleScreen={() => setIncludeScreen((prev) => !prev)}
                onCaptureScreen={handleCaptureScreen}
              />
            </div>
            {isStreaming && (
              <div className="mt-3 flex justify-end">
                <button
                  type="button"
                  onClick={cancelStream}
                  className="rounded-xl border border-rose-400/30 bg-rose-500/10 px-4 py-2 text-[10px] uppercase tracking-[0.22em] text-rose-200"
                >
                  Stop
                </button>
              </div>
            )}
          </div>
        </motion.section>
      </main>

      <SettingsPanel
        isOpen={settingsOpen}
        onClose={() => setSettingsOpen(false)}
        includeScreen={includeScreen}
        onToggleScreen={() => setIncludeScreen((prev) => !prev)}
      />
      <PermissionModal
        pendingTool={pendingTool}
        onApprove={(confirmation) => {
          approveTool(pendingTool.id, confirmation)
        }}
        onDeny={() => denyTool(pendingTool.id)}
      />
    </div>
  )
}

export default App
