import { motion } from 'framer-motion'

function ChatInput({ value, onChange, onSend, isLoading }) {
  const canSend = value.trim().length > 0 && !isLoading

  const handleSubmit = (event) => {
    event.preventDefault()
    if (!value.trim()) {
      return
    }
    onSend()
  }

  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-black/40 px-4 py-3 shadow-[0_0_32px_rgba(59,130,246,0.12)] backdrop-blur-xl">
        <input
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder="Send a command or ask GEWN anything..."
          className="flex-1 bg-transparent text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none"
          type="text"
          disabled={isLoading}
          aria-label="Message input"
        />
        <motion.button
          type="submit"
          whileHover={canSend ? { scale: 1.02 } : undefined}
          whileTap={canSend ? { scale: 0.98 } : undefined}
          className={`rounded-xl border px-4 py-2 text-xs font-semibold uppercase tracking-[0.22em] transition ${
            canSend
              ? 'border-sky-400/30 bg-sky-500/20 text-sky-200 shadow-[0_0_18px_rgba(59,130,246,0.35)]'
              : 'cursor-not-allowed border-white/10 bg-white/5 text-slate-500'
          }`}
          disabled={!canSend}
        >
          Send
        </motion.button>
      </div>
      <div className="mt-2 flex items-center justify-between text-[10px] uppercase tracking-[0.2em] text-slate-500">
        <span>Enter to transmit</span>
        <span className="text-slate-600">Voice ready</span>
      </div>
    </form>
  )
}

export default ChatInput
