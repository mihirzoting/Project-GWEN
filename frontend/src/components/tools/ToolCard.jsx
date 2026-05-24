function ToolCard({ tool }) {
  if (!tool) {
    return null
  }

  const statusColor =
    tool.status === 'success'
      ? 'text-emerald-200'
      : tool.status === 'error'
        ? 'text-rose-200'
        : 'text-amber-200'

  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-xs shadow-[0_0_24px_rgba(59,130,246,0.08)]">
      <div className="flex items-center justify-between">
        <p className="text-[10px] uppercase tracking-[0.24em] text-slate-500">
          Tool
        </p>
        <span className={`text-[10px] uppercase tracking-[0.22em] ${statusColor}`}>
          {tool.status || 'pending'}
        </span>
      </div>
      <p className="mt-2 text-sm text-slate-200">{tool.name}</p>
      <div className="mt-2 rounded-xl border border-white/10 bg-black/30 p-2 text-[11px] text-slate-300">
        <pre className="whitespace-pre-wrap">
          {JSON.stringify(tool.details, null, 2)}
        </pre>
      </div>
    </div>
  )
}

export default ToolCard
