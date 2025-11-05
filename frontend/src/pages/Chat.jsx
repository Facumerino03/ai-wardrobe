import { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Trash2 } from 'lucide-react';
import { chatAPI } from '../services/api';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState('default_session');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    loadHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadHistory = async () => {
    try {
      const response = await chatAPI.getHistory(sessionId);
      if (response.history && response.history.length > 0) {
        setMessages(response.history);
      } else {
        // Add welcome message if no history
        setMessages([{
          role: 'assistant',
          content: "Hi! I'm your personal AI fashion stylist. I can help you with outfit suggestions, styling advice, fashion trends, and more. What would you like to know?"
        }]);
      }
    } catch (error) {
      console.error('Error loading chat history:', error);
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');

    // Add user message to chat
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);

    setLoading(true);
    try {
      const response = await chatAPI.sendMessage(userMessage, 'default_user', sessionId);

      // Add assistant response
      setMessages(prev => [...prev, { role: 'assistant', content: response.message }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = async () => {
    if (!confirm('Clear all conversation history?')) return;

    try {
      await chatAPI.clear(sessionId);
      setMessages([{
        role: 'assistant',
        content: "Conversation cleared! How can I help you today?"
      }]);
    } catch (error) {
      console.error('Error clearing chat:', error);
    }
  };

  const quickQuestions = [
    "What should I wear to a wedding?",
    "How do I style a white shirt?",
    "What colors go well with navy blue?",
    "Casual Friday outfit ideas?",
  ];

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-12rem)] flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Fashion Assistant</h1>
          <p className="text-gray-600">Chat with your AI stylist</p>
        </div>
        <button
          onClick={handleClear}
          className="btn btn-secondary"
        >
          <Trash2 className="w-4 h-4 mr-2 inline" />
          Clear Chat
        </button>
      </div>

      {/* Quick Questions (only show when chat is empty or just welcome message) */}
      {messages.length <= 1 && (
        <div className="card mb-4">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Try asking:</h3>
          <div className="flex flex-wrap gap-2">
            {quickQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => setInput(question)}
                className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700 transition-colors"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 card overflow-y-auto mb-4">
        <div className="space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`flex gap-3 max-w-[80%] ${
                  message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
                }`}
              >
                {/* Avatar */}
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                    message.role === 'user'
                      ? 'bg-primary-100 text-primary-700'
                      : 'bg-gray-200 text-gray-700'
                  }`}
                >
                  {message.role === 'user' ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
                </div>

                {/* Message Content */}
                <div
                  className={`px-4 py-2 rounded-lg ${
                    message.role === 'user'
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{message.content}</p>
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="flex gap-3 max-w-[80%]">
                <div className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 bg-gray-200 text-gray-700">
                  <Bot className="w-5 h-5" />
                </div>
                <div className="px-4 py-2 rounded-lg bg-gray-100">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Form */}
      <form onSubmit={handleSend} className="card">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask me anything about fashion..."
            className="input flex-1"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="btn btn-primary disabled:opacity-50"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  );
};

export default Chat;
