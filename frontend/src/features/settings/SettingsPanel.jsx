function SettingsPanel({ isOpen, onClose, includeScreen, onToggleScreen }) {
  if (!isOpen) {
    return null
  }

  return (
    <div className="fixed inset-0 z-40 flex justify-end bg-black/40 backdrop-blur-sm">
      <div className="h-full w-full max-w-sm border-l border-white/10 bg-slate-950/90 p-6">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white">Settings</h2>
          <button
            type="button"
            onClick={onClose}
            className="text-xs uppercase tracking-[0.2em] text-slate-400"
          >
            Close
          </button>
        </div>
        <div className="mt-6 space-y-4 text-sm text-slate-300">
          <div className="flex items-center justify-between">
            <span>Include screen context</span>
            <button
              type="button"
              onClick={onToggleScreen}
              className={`rounded-full border px-3 py-1 text-xs uppercase tracking-[0.2em] ${
                includeScreen
                  ? 'border-emerald-400/30 bg-emerald-500/20 text-emerald-200'
                  : 'border-white/10 bg-white/5 text-slate-500'
              }`}
            >
              {includeScreen ? 'On' : 'Off'}
            </button>
          </div>
          <p className="text-xs text-slate-500">
            Screen context is captured on demand and used to ground responses.
          </p>
        </div>
      </div>
    </div>
  )
}

export default SettingsPanel
