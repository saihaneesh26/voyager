import React, { useState, useRef, useEffect } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { v4 as uuidv4 } from "uuid"
import "./styles.css"

export default function App() {

  const [query, setQuery] = useState("")

  const [loading, setLoading] =
    useState(false)

  const [messages, setMessages] =
    useState([])

  const [selectedModel, setSelectedModel] =
    useState("gemini-2.5-flash")

  const [sessionId] =
    useState(uuidv4())

  const chatEndRef = useRef(null)

  const models = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
  ]

  // ============================================
  // AUTO SCROLL
  // ============================================

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    })
  }, [messages, loading])

  // ============================================
  // ASK AI
  // ============================================

  const askAI = async () => {

  if (!query.trim()) return

  const currentQuery = query

  // Add user message immediately
  setMessages((prev) => [
    ...prev,
    {
      role: "user",
      content: currentQuery,
    },
  ])

  setQuery("")

  setLoading(true)

  try {

    const res = await fetch(
      `${import.meta.env.VITE_API_URL}/query?query=${encodeURIComponent(
        currentQuery
      )}&model=${selectedModel}&session_id=${sessionId}`
    )

    const data = await res.text()

    console.log(data)

    // Add assistant response
    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: data,
      },
    ])

  } catch (err) {

    console.error(err)

    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content:
          "Something went wrong.",
      },
    ])

  } finally {

    setLoading(false)
  }
}
  // ============================================
  // ENTER KEY SUPPORT
  // ============================================

  const handleKeyDown = (e) => {

    if (
      e.key === "Enter" &&
      !e.shiftKey
    ) {
      e.preventDefault()
      askAI()
    }
  }

  return (
    <div className="chatApp">

      {/* SIDEBAR */}

      <div className="sidebar">

        <div>

          <h1 className="logo">
            Voyager AI
          </h1>

          <div className="poweredText">
            Powered by Gemini AI
          </div>

        </div>

        <div className="sidebarSection">

          <div className="sidebarTitle">
            Gemini AI Model
          </div>

          <select
            className="modelDropdown"
            value={selectedModel}
            onChange={(e) =>
              setSelectedModel(
                e.target.value
              )
            }
          >
            {models.map((model) => (
              <option
                key={model}
                value={model}
              >
                {model}
              </option>
            ))}
          </select>

        </div>

        <div className="sidebarSection">

          <div className="sidebarTitle">
            Stack
          </div>

          <div className="tagList">

            <div className="tag">
              FastAPI
            </div>

            <div className="tag">
              LangGraph
            </div>

            <div className="tag">
              OpenFlights
            </div>

            <div className="tag">
              OpenStreetMap
            </div>

          </div>
        </div>

      </div>

      {/* MAIN CHAT */}

      <div className="chatContainer">

        {/* CHAT MESSAGES */}

        <div className="chatMessages">

          {messages.length === 0 && (
            <div className="emptyState">

              <h1>
                Voyager AI
              </h1>

              <p>
                Ask anything about flights,
                destinations, attractions,
                travel planning and more.
              </p>

            </div>
          )}

          {messages.map(
            (message, index) => (

              <div
                key={index}
                className={`messageRow ${
                  message.role === "user"
                    ? "userRow"
                    : "assistantRow"
                }`}
              >

                <div
                  className={`messageBubble ${
                    message.role === "user"
                      ? "userBubble"
                      : "assistantBubble"
                  }`}
                >

                  {message.role ===
                  "assistant" ? (

                    <div className="markdownBody">

                      <ReactMarkdown
                        remarkPlugins={[
                          remarkGfm,
                        ]}
                      >
                        {message.content.replace(
                          /\\n/g,
                          "\n"
                        )}
                      </ReactMarkdown>

                    </div>

                  ) : (
                    message.content
                  )}

                </div>

              </div>
            )
          )}

          {loading && (

            <div className="messageRow assistantRow">

              <div className="messageBubble assistantBubble">

                <div className="typing">
                  Thinking...
                </div>

              </div>

            </div>
          )}

          <div ref={chatEndRef} />

        </div>

        {/* INPUT AREA */}

        <div className="inputArea">

          <div className="inputContainer">

            <textarea
              className="chatInput"
              value={query}
              onChange={(e) =>
                setQuery(e.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Ask Voyager AI..."
            />

            <button
              className="sendButton"
              onClick={askAI}
              disabled={loading}
            >
              ↑
            </button>

          </div>

        </div>

      </div>

    </div>
  )
}