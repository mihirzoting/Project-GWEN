import { motion } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'
import ToolCard from '../tools/ToolCard'

const messageMotion = {
  initial: { opacity: 0, y: 12, scale: 0.98 },
  animate: { opacity: 1, y: 0, scale: 1 },
  exit: { opacity: 0, y: 6, scale: 0.98 },
}

function ChatMessage({ message }) {
  const isUser = message.role === 'user'
  const isStreaming = message.status === 'streaming'
  const isError = message.status === 'error'

  if (message.role === 'tool') {
    return (
      <motion.div {...messageMotion} layout className="flex justify-start">
        <ToolCard tool={message.tool} />
      </motion.div>
    )
  }

  return (
    <motion.div
      {...messageMotion}
      layout
      className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <motion.div
        whileHover={{ scale: 1.01 }}
        className={`max-w-[78%] rounded-2xl border px-4 py-3 text-sm leading-relaxed shadow-[0_0_24px_rgba(59,130,246,0.08)] ${
          isUser
            ? 'border-sky-400/20 bg-sky-500/15 text-slate-100'
            : isError
              ? 'border-rose-400/30 bg-rose-500/10 text-rose-100'
              : 'border-white/10 bg-white/5 text-slate-200'
        }`}
      >
        <p className="text-[10px] uppercase tracking-[0.24em] text-slate-500">
          {isUser ? 'You' : 'GEWN'}
        </p>
        <div className="prose prose-invert mt-2 text-sm">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeHighlight]}
          >
            {message.content}
          </ReactMarkdown>
        </div>
        {isStreaming && (
          <span className="mt-2 inline-block h-3 w-[2px] animate-pulse rounded-full bg-sky-300/80" />
        )}
      </motion.div>
    </motion.div>
  )
}

export default ChatMessage
