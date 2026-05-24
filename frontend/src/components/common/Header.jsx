function Header({ status, memoryStatus, visionStatus, onOpenSettings }) {
  return (
    <header className="flex flex-wrap items-center justify-between gap-4 border-b border-white/10 pb-4">
      <div className="flex items-center gap-3">
        <div className="h-10 w-10 rounded-2xl bg-white/10 p-[2px]">
          <div className="h-full w-full rounded-2xl bg-gradient-to-br from-violet-400/70 via-sky-400/40 to-transparent" />
        </div>
        <div>
          <p className="text-xs uppercase tracking-[0.32em] text-slate-400">
            GEWN
          </p>
          <h1 className="text-lg font-semibold text-white">Neural Chat</h1>
        </div>
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <div className="flex items-center gap-2 rounded-full border border-white/10 bg-black/30 px-3 py-1 text-xs text-slate-300">
          <span className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_12px_rgba(52,211,153,0.9)]" />
          {status}
        </div>
        <div className="rounded-full border border-white/10 bg-black/30 px-3 py-1 text-[10px] uppercase tracking-[0.2em] text-slate-400">
          Memory {memoryStatus}
        </div>
        <div className="rounded-full border border-white/10 bg-black/30 px-3 py-1 text-[10px] uppercase tracking-[0.2em] text-slate-400">
          Screen {visionStatus}
        </div>
        <button
          type="button"
          onClick={onOpenSettings}
          className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-[10px] uppercase tracking-[0.2em] text-slate-400 transition hover:border-white/20"
        >
          Settings
        </button>
      </div>
    </header>
  )
}

export default Header
