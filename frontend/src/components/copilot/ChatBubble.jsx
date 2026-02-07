import TransferCard from './TransferCard'

const InsightCard = ({ props }) => (
  <div className="bg-gray-800/80 rounded-lg p-4 border border-gray-700 mt-2">
    <p className="text-xs font-semibold text-yellow-400 mb-2">{props?.title}</p>
    <div className="space-y-2">
      {(props?.items || []).map((item, i) => (
        <div key={i} className="flex items-center justify-between text-xs">
          <span className="text-white">{item.shade} - {item.location}</span>
          <span className="text-red-400 font-mono">{item.days_left} days</span>
        </div>
      ))}
    </div>
  </div>
)

const WIDGETS = {
  TRANSFER_CARD: (props, onAction) => <TransferCard props={props} onConfirm={onAction} />,
  INSIGHT_CARD: (props) => <InsightCard props={props} />,
  RESTOCK_ALERT: (props) => <InsightCard props={props} />,
}

export default function ChatBubble({ message, isUser, onWidgetAction }) {
  if (isUser) {
    return (
      <div className="flex justify-end mb-3">
        <div className="bg-blue-600 text-white rounded-2xl rounded-br-sm px-4 py-2 max-w-[80%] text-sm">
          {message.text}
        </div>
      </div>
    )
  }

  return (
    <div className="flex justify-start mb-3">
      <div className="max-w-[90%]">
        <div className="bg-gray-800 text-gray-200 rounded-2xl rounded-bl-sm px-4 py-2 text-sm leading-relaxed">
          {message.text}
        </div>
        {message.ui_widget && WIDGETS[message.ui_widget.type]?.(message.ui_widget.props, onWidgetAction)}
      </div>
    </div>
  )
}
