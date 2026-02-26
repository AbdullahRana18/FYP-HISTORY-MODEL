import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Brain, BookOpen, Award, ShieldCheck, Info, Sparkles, AlertTriangle, Menu, X } from 'lucide-react'

export default function HistoryExaminer() {
    const [query, setQuery] = useState('')
    const [selectedMarks, setSelectedMarks] = useState<number | null>(null)
    const [isAnalyzing, setIsAnalyzing] = useState(false)
    const [messages, setMessages] = useState<any[]>([])
    const [isSidebarOpen, setIsSidebarOpen] = useState(false)
    const chatEndRef = useRef<HTMLDivElement>(null)

    const scrollToBottom = () => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages, isAnalyzing])

    const handleAsk = async () => {
        if (!query.trim() || selectedMarks === null) return

        const userQuery = query
        setQuery('')
        setMessages(prev => [...prev, { role: 'user', content: userQuery, marks: selectedMarks }])
        setIsAnalyzing(true)

        const formData = new FormData()
        formData.append('query', userQuery)
        formData.append('marks', selectedMarks.toString())

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/ask-ai`, {
                method: 'POST',
                body: formData,
            })
            const data = await response.json()
            setMessages(prev => [...prev, { role: 'ai', content: data.answer, marks: selectedMarks }])
        } catch (error) {
            setMessages(prev => [...prev, { role: 'ai', content: "Error connecting to Examiner Engine. Please ensure the backend is running.", isError: true }])
        } finally {
            setIsAnalyzing(false)
        }
    }

    const renderAudit = (content: string) => {
        const auditIndex = content.indexOf('[EXAMINER AUDIT]')
        if (auditIndex === -1) return null

        const auditText = content.substring(auditIndex + 16).trim()
        return (
            <div className="mt-4 md:mt-6 p-3 md:p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl md:rounded-2xl flex items-start gap-3">
                <ShieldCheck className="text-emerald-400 mt-1 shrink-0" size={18} />
                <div>
                    <h4 className="text-emerald-400 text-[10px] md:text-xs font-black uppercase tracking-tighter mb-1">Examiner Audit Detail</h4>
                    <p className="text-xs md:text-sm text-emerald-100/80 leading-relaxed font-mono whitespace-pre-wrap">{auditText}</p>
                </div>
            </div>
        )
    }

    const renderContent = (content: string) => {
        const auditIndex = content.indexOf('[EXAMINER AUDIT]')
        const cleanContent = auditIndex !== -1 ? content.substring(0, auditIndex) : content

        return cleanContent.split('\n').map((line, i) => {
            if (line.match(/^REASON \d:|^POINT:|^INTRODUCTION:|^AGREE SECTION:|^DISAGREE SECTION:|^FINAL JUDGEMENT:/i)) {
                return (
                    <div key={i} className="mt-3 md:mt-4 mb-2 p-2 md:p-3 bg-indigo-500/10 border-l-4 border-indigo-500 rounded-r-lg group">
                        <span className="text-[10px] md:text-xs font-black text-indigo-400 uppercase tracking-widest">{line}</span>
                    </div>
                )
            }
            if (line.match(/^EVIDENCE:/i)) {
                return (
                    <div key={i} className="mt-2 pl-3 md:pl-4 py-1 border-l-2 border-amber-500/30 flex items-start gap-2">
                        <Award size={14} className="text-amber-400 mt-1 shrink-0" />
                        <span className="text-xs md:text-sm text-slate-300 font-medium"><span className="text-amber-400 font-bold">EVIDENCE:</span> {line.replace(/EVIDENCE:/i, '')}</span>
                    </div>
                )
            }
            if (line.match(/^EXPLANATION:/i)) {
                return (
                    <div key={i} className="mt-2 pl-3 md:pl-4 py-1 border-l-2 border-cyan-500/30 flex items-start gap-2 text-xs md:text-sm text-slate-400 italic">
                        <Brain size={14} className="text-cyan-400 mt-1 shrink-0" />
                        <span><span className="text-cyan-400 font-bold not-italic">EXPLANATION:</span> {line.replace(/EXPLANATION:/i, '')}</span>
                    </div>
                )
            }
            if (line.startsWith('###')) return <h4 key={i} className="text-base md:text-lg font-bold text-white mt-6 md:mt-8 mb-3 md:mb-4">{line.replace('###', '')}</h4>
            return line ? <p key={i} className="mb-2 md:mb-3 text-xs md:text-sm text-slate-300 leading-relaxed">{line}</p> : <div key={i} className="h-2" />
        })
    }

    return (
        <div className="h-screen bg-slate-950 flex flex-col lg:flex-row overflow-hidden font-sans text-white">
            
            {/* Sidebar Desktop / Overlay Mobile */}
            <AnimatePresence>
                {(isSidebarOpen || window.innerWidth > 1024) && (
                    <motion.aside 
                        initial={{ x: -320 }}
                        animate={{ x: 0 }}
                        exit={{ x: -320 }}
                        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                        className={`fixed lg:relative z-50 w-80 h-full bg-slate-900 border-r border-white/5 flex flex-col p-6 overflow-y-auto custom-scrollbar`}
                    >
                        <div className="flex items-center justify-between mb-8">
                            <div className="flex items-center gap-3">
                                <div className="p-2 bg-indigo-500 rounded-xl">
                                    <BookOpen className="text-white" size={20} />
                                </div>
                                <h1 className="text-lg font-black tracking-tight">EXAMINER</h1>
                            </div>
                            <button onClick={() => setIsSidebarOpen(false)} className="lg:hidden p-2 text-slate-400">
                                <X size={20} />
                            </button>
                        </div>

                        <div className="space-y-6">
                            <div>
                                <h3 className="text-[10px] font-black text-slate-500 uppercase tracking-[2px] mb-4">Marking Criteria</h3>
                                <div className="space-y-3">
                                    {[4, 7, 14].map(m => (
                                        <div key={m} className={`p-3 rounded-2xl border transition-all ${selectedMarks === m ? 'bg-indigo-500/10 border-indigo-500/50' : 'bg-white/5 border-white/5 opacity-50'}`}>
                                            <div className="flex justify-between items-center mb-1">
                                                <span className="text-xs font-bold">{m} Markers</span>
                                                <Award size={14} className={selectedMarks === m ? 'text-indigo-400' : 'text-slate-600'} />
                                            </div>
                                            <p className="text-[10px] text-slate-400 leading-normal">
                                                {m === 4 && "Requires 2 PEEL paragraphs. Factual depth is critical."}
                                                {m === 7 && "3 Analytical paragraphs. Focused on consequences."}
                                                {m === 14 && "Full evaluation essay. Balanced debate + judgement."}
                                            </p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </motion.aside>
                )}
            </AnimatePresence>

            {/* Main Chat Area */}
            <main className="flex-1 flex flex-col relative bg-slate-950/40 w-full overflow-hidden">
                {/* Header */}
                <header className="h-16 md:h-20 border-b border-white/5 flex items-center justify-between px-4 md:px-8 bg-slate-950/80 backdrop-blur-xl z-20">
                    <div className="flex items-center gap-3">
                        <button onClick={() => setIsSidebarOpen(true)} className="lg:hidden p-2 bg-white/5 rounded-lg text-slate-400">
                            <Menu size={20} />
                        </button>
                        <div>
                            <h2 className="text-[10px] md:text-sm font-black text-slate-400 uppercase tracking-[2px]">Pak History</h2>
                            <p className="text-[8px] md:text-[10px] font-medium text-emerald-500 flex items-center gap-1 uppercase">
                                <span className="w-1 h-1 bg-emerald-500 rounded-full animate-pulse" />
                                Examiner Online
                            </p>
                        </div>
                    </div>

                    <div className="flex bg-slate-900 border border-white/5 rounded-full p-1 scale-90 md:scale-100">
                        {[4, 7, 14].map(m => (
                            <button
                                key={m}
                                onClick={() => setSelectedMarks(m)}
                                className={`px-3 md:px-4 py-1 rounded-full text-[10px] md:text-xs font-black transition-all ${selectedMarks === m ? 'bg-indigo-600 text-white shadow-lg' : 'text-slate-500'}`}
                            >
                                {m}M
                            </button>
                        ))}
                    </div>
                </header>

                {/* Messages Container */}
                <div className="flex-1 overflow-y-auto p-4 md:p-10 space-y-6 md:space-y-8 custom-scrollbar">
                    {messages.length === 0 && (
                        <div className="h-full flex flex-col items-center justify-center opacity-20 text-center max-w-[280px] md:max-w-sm mx-auto">
                            <Sparkles size={48} className="mb-4 md:size-64" />
                            <h3 className="text-base md:text-xl font-black uppercase tracking-[4px]">History Engine</h3>
                            <p className="text-[10px] md:text-xs font-medium mt-2">Input your question to generate a professional Cambridge script.</p>
                        </div>
                    )}

                    <AnimatePresence>
                        {messages.map((msg, idx) => (
                            <motion.div
                                key={idx}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div className={`max-w-[92%] md:max-w-[75%] rounded-2xl md:rounded-3xl p-4 md:p-6 shadow-xl ${msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-slate-900/80 border border-white/5 text-slate-100'}`}>
                                    {msg.role === 'ai' && (
                                        <div className="flex items-center gap-2 mb-3 text-[9px] font-black uppercase tracking-widest text-indigo-400 border-b border-indigo-400/10 pb-2">
                                            <Brain size={12} /> Examiner (History 2059)
                                        </div>
                                    )}
                                    <div className="whitespace-pre-wrap break-words">
                                        {msg.role === 'ai' ? renderContent(msg.content) : msg.content}
                                    </div>
                                    {msg.role === 'ai' && renderAudit(msg.content)}
                                    {msg.role === 'user' && (
                                        <div className="mt-2 pt-2 border-t border-white/10 flex justify-end">
                                            <span className="text-[8px] font-black uppercase border border-white/20 px-2 py-0.5 rounded-full">{msg.marks}M Allocated</span>
                                        </div>
                                    )}
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                    {isAnalyzing && (
                        <div className="flex justify-start">
                            <div className="bg-slate-900 border border-white/5 rounded-2xl p-4 flex items-center gap-3">
                                <div className="flex gap-1">
                                    <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-bounce [animation-delay:-0.3s]" />
                                    <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-bounce [animation-delay:-0.15s]" />
                                    <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-bounce" />
                                </div>
                                <span className="text-[10px] font-black text-indigo-400 uppercase tracking-widest animate-pulse">Analyzing Sources...</span>
                            </div>
                        </div>
                    )}
                    <div ref={chatEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-4 md:p-6 bg-slate-950/80 backdrop-blur-xl border-t border-white/5">
                    {selectedMarks === null && (
                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mb-4 bg-amber-500/10 border border-amber-500/20 rounded-xl p-3 flex items-center gap-2 text-amber-400">
                            <AlertTriangle size={16} className="shrink-0" />
                            <p className="text-[9px] font-bold uppercase tracking-wider">Select marks above to start.</p>
                        </motion.div>
                    )}

                    <div className={`relative transition-opacity ${selectedMarks === null ? 'opacity-40 grayscale pointer-events-none' : 'opacity-100'}`}>
                        <textarea
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleAsk(); } }}
                            placeholder={selectedMarks ? `Your ${selectedMarks}M question...` : "Select marks..."}
                            className="w-full bg-slate-900/50 border border-white/5 rounded-2xl md:rounded-[2rem] p-4 md:p-6 pr-14 md:pr-16 h-16 md:h-20 text-sm focus:outline-none focus:border-indigo-500/50 transition-all resize-none font-medium"
                        />
                        <button
                            onClick={handleAsk}
                            disabled={isAnalyzing || !query.trim() || selectedMarks === null}
                            className="absolute right-3 bottom-3 md:right-4 md:bottom-4 p-2.5 md:p-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg active:scale-95 disabled:opacity-0"
                        >
                            <Send size={18} />
                        </button>
                    </div>
                </div>
            </main>
        </div>
    )
}