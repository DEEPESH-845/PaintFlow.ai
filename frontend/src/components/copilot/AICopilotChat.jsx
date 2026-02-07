import { useState, useRef, useEffect } from 'react'
import { ChatBubbleLeftRightIcon, XMarkIcon, PaperAirplaneIcon } from '@heroicons/react/24/solid'
import { sendChat } from '../../api/copilot'
import { useSimulation } from '../../contexts/SimulationContext'
import ChatBubble from './ChatBubble'

export default function AICopilotChat() {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState([
    { text: "Hi! I'm your PaintFlow AI assistant. Ask me about inventory, stockouts, or demand trends.", isUser: false },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)
  const { scenario } = useSimulation()

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || loading) return
    const userMsg = input.trim()
    setInput('')
    setMessages(prev => [...prev, { text: userMsg, isUser: true }])
    setLoading(true)

    try {
      const res = await sendChat(userMsg, { scenario_id: scenario })
      setMessages(prev => [...prev, { ...res.data, isUser: false }])
    } catch {
      setMessages(prev => [...prev, { text: 'Sorry, something went wrong. Try again.', isUser: false }])
    } finally {
      setLoading(false)
    }
  }

  const handleWidgetAction = () => {
    setMessages(prev => [...prev, {
      text: "Transfer confirmed! 500 units of Bridal Red are now in transit from Mumbai to Pune. ETA: 2 days. The map will update shortly.",
      isUser: false,
    }])
  }

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-blue-600 hover:bg-blue-500 text-white shadow-2xl flex items-center justify-center transition-transform hover:scale-110"
      >
        <ChatBubbleLeftRightIcon className="w-6 h-6" />
      </button>
    )
  }

  return (
    <div className="fixed bottom-6 right-6 z-50 w-96 h-[500px] bg-gray-900 border border-gray-700 rounded-2xl shadow-2xl flex flex-col overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-blue-600/20 border-b border-gray-800">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
          <span className="text-sm font-semibold text-white">AI Copilot</span>
        </div>
        <button onClick={() => setOpen(false)} className="text-gray-400 hover:text-white">
          <XMarkIcon className="w-5 h-5" />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-auto p-4 space-y-1">
        {messages.map((msg, i) => (
          <ChatBubble key={i} message={msg} isUser={msg.isUser} onWidgetAction={handleWidgetAction} />
        ))}
        {loading && (
          <div className="flex justify-start mb-3">
            <div className="bg-gray-800 rounded-2xl rounded-bl-sm px-4 py-2">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-800 p-3">
        <div className="flex gap-2">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            placeholder="Ask about inventory, transfers..."
            className="flex-1 bg-gray-800 text-white text-sm rounded-lg px-3 py-2 outline-none focus:ring-1 focus:ring-blue-500 placeholder-gray-600"
          />
          <button
            onClick={handleSend}
            disabled={loading}
            className="p-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 rounded-lg transition-colors"
          >
            <PaperAirplaneIcon className="w-4 h-4 text-white" />
          </button>
        </div>
        <div className="flex gap-2 mt-2">
          {['Why is Bridal Red low in Pune?', 'Stockouts', 'Diwali prep'].map(q => (
            <button
              key={q}
              onClick={() => { setInput(q); }}
              className="text-[10px] text-gray-500 bg-gray-800 px-2 py-1 rounded-full hover:bg-gray-700 hover:text-gray-300 transition-colors"
            >
              {q}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
