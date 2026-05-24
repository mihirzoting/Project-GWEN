import { useMemo, useState } from 'react'

function PermissionModal({ pendingTool, onApprove, onDeny }) {
  const [confirmation, setConfirmation] = useState('')

  const needsTyped = useMemo(
    () => pendingTool?.confirmationType === 'typed',
    [pendingTool]
  )

  if (!pendingTool) {
    return null
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="w-full max-w-md rounded-2xl border border-white/10 bg-slate-900/90 p-6 shadow-[0_0_60px_rgba(59,130,246,0.35)]">
        <h2 className="text-lg font-semibold text-white">Permission required</h2>
        <p className="mt-2 text-sm text-slate-300">
          GEWN wants to run: <span className="text-slate-100">{pendingTool.name}</span>
        </p>
        <div className="mt-4 rounded-xl border border-white/10 bg-black/40 p-3 text-xs text-slate-300">
          <pre className="whitespace-pre-wrap">
            {JSON.stringify(pendingTool.details, null, 2)}
          </pre>
        </div>
        {needsTyped && (
          <div className="mt-4">
            <label className="text-xs uppercase tracking-[0.2em] text-slate-400">
              Type "{pendingTool.confirmationText}"
            </label>
            <input
              value={confirmation}
              onChange={(event) => setConfirmation(event.target.value)}
              className="mt-2 w-full rounded-xl border border-white/10 bg-black/40 px-3 py-2 text-sm text-slate-100 focus:outline-none"
            />
          </div>
        )}
        <div className="mt-6 flex justify-end gap-2">
          <button
            type="button"
            onClick={onDeny}
            className="rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.2em] text-slate-400"
          >
            Deny
          </button>
          <button
            type="button"
            onClick={() => onApprove(needsTyped ? confirmation : undefined)}
            className="rounded-xl border border-sky-400/30 bg-sky-500/20 px-4 py-2 text-xs uppercase tracking-[0.2em] text-sky-200"
          >
            Approve
          </button>
        </div>
      </div>
    </div>
  )
}

export default PermissionModal
