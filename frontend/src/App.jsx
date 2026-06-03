import React, {
  useState,
  useRef,
  useEffect,
} from "react"

import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

import {
  GoogleLogin,
  googleLogout,
} from "@react-oauth/google"

import { jwtDecode } from "jwt-decode"

import {
  FaGithub,
  FaLinkedin,
} from "react-icons/fa"

import "./styles.css"

export default function App() {

  // =========================================================
  // SESSION
  // =========================================================

  const existingSession =
    localStorage.getItem(
      "voyager_session"
    )

  const sessionId =
    existingSession ||
    crypto.randomUUID()

  localStorage.setItem(
    "voyager_session",
    sessionId
  )

  // =========================================================
  // USER
  // =========================================================

  const [user, setUser] =
    useState(

      JSON.parse(
        localStorage.getItem(
          "voyager_user"
        )
      )
    )

  // =========================================================
  // CHAT STATE
  // =========================================================

  const [query, setQuery] =
    useState("")

  const [messages, setMessages] =
    useState([])

  const [loading, setLoading] =
    useState(false)

  // =========================================================
  // MODEL STATE
  // =========================================================

  const [selectedModel, setSelectedModel] =
    useState("gemini-2.5-flash")

  const models = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-1.5-flash",
  ]

  // =========================================================
  // REFS
  // =========================================================

  const chatEndRef = useRef(null)

  // =========================================================
  // AUTO SCROLL
  // =========================================================

  useEffect(() => {

    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    })

  }, [messages, loading])

  // =========================================================
  // GOOGLE LOGIN
  // =========================================================

  const handleLoginSuccess = (
    credentialResponse
  ) => {

    const decoded = jwtDecode(
      credentialResponse.credential
    )

    localStorage.setItem(

      "voyager_user",

      JSON.stringify(decoded)
    )

    setUser(decoded)
  }

  // =========================================================
  // LOGOUT
  // =========================================================

  const handleLogout = () => {

    googleLogout()

    localStorage.removeItem(
      "voyager_user"
    )

    setUser(null)

    setMessages([])

    setQuery("")
  }

  // =========================================================
  // NEW CHAT
  // =========================================================

  const createNewChat = () => {

    const newSession =
      crypto.randomUUID()

    localStorage.setItem(
      "voyager_session",
      newSession
    )

    window.location.reload()
  }

  // =========================================================
  // ASK AI
  // =========================================================

  const askAI = async () => {

    if (!user) {
      alert("Please login first")
      return
    }

    if (!query.trim()) return

    const currentQuery = query

    // USER MESSAGE

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

      const response = await fetch(

        `${import.meta.env.VITE_API_URL}/query` +

        `?query=${encodeURIComponent(
          currentQuery
        )}` +

        `&model=${selectedModel}` +

        `&session_id=${sessionId}` +

        `&email=${encodeURIComponent(
          user.email
        )}`

      )

      const data =
        await response.text()

      // ASSISTANT MESSAGE

      setMessages((prev) => [

        ...prev,

        {
          role: "assistant",
          content: data,
        },
      ])

    } catch (error) {

      console.error(error)

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

  // =========================================================
  // ENTER SUPPORT
  // =========================================================

  const handleKeyDown = (e) => {

    if (
      e.key === "Enter" &&
      !e.shiftKey
    ) {

      e.preventDefault()

      askAI()
    }
  }

  // =========================================================
  // UI
  // =========================================================

  return (

    <div className="chatApp">

      {/* =====================================================
          SIDEBAR
      ====================================================== */}

      <div className="sidebar">

        {/* HEADER */}

        <div>

          <h1 className="logo">
            Voyager AI
          </h1>

          <div className="poweredText">
            Powered by Gemini AI
          </div>

          <div className="poweredText">
            Developed by Haneesh
          </div>

          {/* SOCIALS */}

          <div className="creatorLinks">

            <a
              href="https://linkedin.com/in/imsaihaneesh26"
              target="_blank"
              rel="noreferrer"
              className="socialIcon"
            >
              <FaLinkedin />
            </a>

            <a
              href="https://github.com/saihaneesh26/voyager"
              target="_blank"
              rel="noreferrer"
              className="socialIcon"
            >
              <FaGithub />
            </a>

          </div>

          {/* AUTH */}

          <div className="authSection">

            {!user ? (

              <GoogleLogin

                onSuccess={
                  handleLoginSuccess
                }

                onError={() =>
                  console.log(
                    "Login Failed"
                  )
                }
              />

            ) : (

              <div className="userProfile">

                <img
                  src={user.picture}
                  alt={user.name}
                  className="profileImage"
                  referrerPolicy="no-referrer"
                />

                <div className="userName">
                  {user.name}
                </div>

                <div className="userEmail">
                  {user.email}
                </div>

                <button
                  onClick={handleLogout}
                  className="logoutButton"
                >
                  Logout
                </button>

              </div>
            )}

          </div>

        </div>

        {/* MODEL */}

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

        {/* STACK */}

        <div className="sidebarSection">

          <div className="sidebarTitle">
            Stack
          </div>

          <div className="tagList">

            <div className="tag">
              React
            </div>

            <div className="tag">
              FastAPI
            </div>

            <div className="tag">
              LangGraph
            </div>

            <div className="tag">
              Gemini AI
            </div>

            <div className="tag">
              OpenFlights
            </div>

            <div className="tag">
              OpenTripMap
            </div>

          </div>

        </div>

        {/* ACTIONS */}

        <div className="sidebarSection">

          <button
            className="newChatButton"
            onClick={createNewChat}
          >
            + New Chat
          </button>

        </div>

      </div>

      {/* =====================================================
          CHAT
      ====================================================== */}

      <div className="chatContainer">

        {/* MESSAGES */}

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

          {/* LOADING */}

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

        {/* INPUT */}

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