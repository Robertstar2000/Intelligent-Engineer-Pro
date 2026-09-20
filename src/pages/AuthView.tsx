
import React, { useState } from 'react';
import { useProject } from '../context/ProjectContext';
import { Button } from '../components/ui';
import { Shield, Zap, Layers, Cpu, Globe } from 'lucide-react';
import { RecoveryFlow } from '../components/auth/RecoveryFlow';

export const AuthView = () => {
    const { login, signup } = useProject();
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        geminiKey: ''
    });
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isWaitlistModalOpen, setIsWaitlistModalOpen] = useState(false);
    const [showKeyInfo, setShowKeyInfo] = useState(false);
    const [showRecovery, setShowRecovery] = useState(false);
    const [recoveryCodes, setRecoveryCodes] = useState<string[]>([]);
    const [waitlistData, setWaitlistData] = useState({
        name: '',
        profession: '',
        email: '',
        proposedUse: ''
    });

    const handleWaitlistSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const subject = encodeURIComponent('Vibe Engineer');
        const body = encodeURIComponent(
            `Name: ${waitlistData.name}\n` +
            `Profession: ${waitlistData.profession}\n` +
            `Email: ${waitlistData.email}\n` +
            `Proposed Use: ${waitlistData.proposedUse}`
        );
        window.location.href = `mailto:mifecoinc@gmail.com?subject=${subject}&body=${body}`;
        setIsWaitlistModalOpen(false);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            if (isLogin) {
                const success = await login(formData.email || formData.username, formData.password);
                if (!success) setError('Invalid credentials');
            } else {
                const codes = await signup(formData.username, formData.email, formData.password, formData.geminiKey);
                if (!codes) setError('User already exists or signup failed');
                else setRecoveryCodes(codes);
            }
        } catch (err) {
            setError('An error occurred');
        } finally {
            setIsLoading(false);
        }
    };

    const features = [
        { id: '01', title: 'HMAP LIFECYCLE', desc: 'Navigate through a rigorous 6-phase engineering framework—from initial Concept and Requirements to detailed Design, Implementation, and final Deployment protocols.', color: 'text-cyan-400' },
        { id: '02', title: 'AI GENERATION', desc: 'Leverage Gemini-powered synthesis to automatically generate technical documentation, phase deliverables, and versioned outputs tailored to your specific project constraints.', color: 'text-emerald-400' },
        { id: '03', title: 'RISK ANALYSIS', desc: 'Proactively identify technical, schedule, and budgetary risks with automated severity scoring and AI-driven mitigation strategies to ensure project stability.', color: 'text-amber-400' },
        { id: '04', title: 'TEAM SYNC', desc: 'Orchestrate complex workflows with role-based access control, integrated task tracking, and a centralized communication hub for seamless team collaboration.', color: 'text-pink-400' },
        { id: '05', title: 'INSIGHT ENGINE', desc: 'Monitor project health with real-time analytics, industry-standard performance benchmarking, and dynamic recommendations for process optimization.', color: 'text-red-400' },
    ];

    if (recoveryCodes.length) return <main className="min-h-screen bg-slate-950 text-white flex items-center justify-center p-6"><section className="max-w-lg w-full border border-amber-400 rounded-2xl p-6"><h1 className="text-xl font-bold">Save your recovery codes</h1><p className="text-slate-300 my-3">Shown once. Store them securely; each code works one time.</p><pre className="bg-black p-4 select-all overflow-auto">{recoveryCodes.join('\n')}</pre><button className="w-full p-3 border rounded-xl my-2" onClick={()=>{const b=new Blob([recoveryCodes.join('\n')+'\n']);const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='vibraengineer-recovery-codes.txt';a.click();URL.revokeObjectURL(a.href)}}>Download codes</button><button className="w-full p-3 bg-cyan-600 rounded-xl" onClick={()=>window.location.reload()}>I saved the codes</button></section></main>;

    return (
        <div className="min-h-screen bg-[#0f172a] text-slate-50 flex flex-col md:flex-row relative overflow-x-hidden">
            {/* Background Glows */}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-600/20 blur-[120px] rounded-full"></div>
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-cyan-600/20 blur-[120px] rounded-full"></div>

            {/* Left Side: Hero */}
            <div className="flex-1 p-8 md:p-16 flex flex-col justify-center relative z-10" style={{ background: 'linear-gradient(140deg, rgba(16,185,129,0.14) 0%, rgba(249,115,22,0.08) 50%, rgba(15,23,42,0) 85%)' }}>
                <div className="mb-10">
                    <div className="inline-flex items-center gap-2 px-3 py-1 mb-5 rounded-full" style={{ border: '1px solid rgba(16,185,129,0.45)', background: 'rgba(16,185,129,0.10)', fontSize: '11px', letterSpacing: '0.22em', fontWeight: 700, color: '#6ee7b7' }}>
                        <span style={{ width: 7, height: 7, borderRadius: '50%', background: '#10b981', display: 'inline-block' }}></span>
                        MIFECO ENGINEERING WORKSPACE
                    </div>
                    <h1 className="font-bold tracking-tighter mb-3 leading-tight" style={{ fontSize: 'clamp(2.4rem, 4.6vw, 4.2rem)' }}>
                        <span className="text-red-500">M</span>
                        <span className="text-cyan-400">I</span>
                        <span className="text-emerald-400">F</span>
                        <span className="text-amber-400">E</span>
                        <span className="text-indigo-400">C</span>
                        <span className="text-pink-500">O</span>
                    </h1>
                    <p className="font-mono text-sm tracking-[0.3em] uppercase mb-4" style={{ background: 'linear-gradient(90deg,#34d399,#fb923c)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                        Vibe Engineer — engineering, minus the busywork
                    </p>
                    <p className="text-slate-400 text-base leading-relaxed mb-8" style={{ maxWidth: '520px' }}>
                        Vibe Engineer gives small engineering teams a focused home for the HMAP lifecycle: sprints, risks, documentation, and team sync in one lean workspace — AI generates the drafts, you make the calls.
                    </p>
                </div>

                <div className="grid gap-4 max-w-2xl" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))' }}>
                    {features.map((f) => (
                        <div key={f.id} className="p-5 rounded-2xl transition-all hover:-translate-y-1" style={{ border: '1px solid rgba(255,255,255,0.08)', background: 'rgba(30,41,59,0.5)', backdropFilter: 'blur(12px)' }}>
                            <div className="flex items-start gap-3">
                                <span className={`font-mono text-lg font-bold ${f.color}`}>{f.id}</span>
                                <div>
                                    <h3 className="font-bold text-sm tracking-tight mb-1">{f.title}</h3>
                                    <p className="text-slate-400 text-xs leading-relaxed mb-0">{f.desc}</p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="flex flex-wrap gap-3 mt-6">
                    {[
                        { i: '🚀', l: 'Sprints live in minutes' },
                        { i: '🛡️', l: 'You review every output' },
                        { i: '🔑', l: 'Bring your own AI key' },
                    ].map((b) => (
                        <div key={b.l} className="inline-flex items-center gap-2 px-3 py-2 rounded-xl" style={{ border: '1px solid rgba(255,255,255,0.08)', background: 'rgba(15,23,42,0.6)', fontSize: '11px', color: '#94a3b8' }}>
                            <span>{b.i}</span> {b.l}
                        </div>
                    ))}
                </div>
            </div>

            {/* Right Side: Auth Form */}
            <div className="flex-1 flex items-center justify-center p-6 relative z-10">
                <div className="w-full max-w-md bg-slate-800/40 backdrop-blur-2xl border border-white/10 rounded-[2.5rem] p-8 md:p-12 shadow-2xl">
                    <div className="flex bg-slate-900/50 p-1 rounded-2xl mb-8 relative">
                        <div 
                            className={`absolute top-1 bottom-1 w-[calc(50%-4px)] bg-white rounded-xl transition-all duration-300 ease-out ${isLogin ? 'left-1' : 'left-[calc(50%+2px)]'}`}
                        ></div>
                        <button 
                            onClick={() => setIsLogin(true)}
                            className={`flex-1 py-3 text-sm font-bold relative z-10 transition-colors ${isLogin ? 'text-slate-900' : 'text-slate-400'}`}
                        >
                            SIGN IN
                        </button>
                        <button 
                            onClick={() => setIsLogin(false)}
                            className={`flex-1 py-3 text-sm font-bold relative z-10 transition-colors ${!isLogin ? 'text-slate-900' : 'text-slate-400'}`}
                        >
                            SIGN UP
                        </button>
                    </div>

                    {showRecovery ? <RecoveryFlow onClose={() => setShowRecovery(false)} /> : <form onSubmit={handleSubmit} className="space-y-6">
                        {!isLogin && (
                            <div className="space-y-2">
                                <label className="text-[10px] font-black tracking-[0.2em] text-slate-500 uppercase ml-2">Username</label>
                                <input 
                                    type="text"
                                    required
                                    value={formData.username}
                                    onChange={(e) => setFormData({...formData, username: e.target.value})}
                                    className="w-full bg-slate-900/50 border border-white/5 rounded-2xl px-5 py-4 text-sm focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/50 transition-all"
                                    placeholder="Enter username"
                                />
                            </div>
                        )}
                        <div className="space-y-2">
                            <label className="text-[10px] font-black tracking-[0.2em] text-slate-500 uppercase ml-2">
                                {isLogin ? 'Email or Username' : 'Email Address'}
                            </label>
                            <input 
                                type={isLogin ? "text" : "email"}
                                required
                                value={isLogin ? (formData.email || formData.username) : formData.email}
                                onChange={(e) => isLogin ? setFormData({...formData, username: e.target.value, email: e.target.value}) : setFormData({...formData, email: e.target.value})}
                                className="w-full bg-slate-900/50 border border-white/5 rounded-2xl px-5 py-4 text-sm focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/50 transition-all"
                                placeholder={isLogin ? "user@example.com" : "Enter email"}
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-[10px] font-black tracking-[0.2em] text-slate-500 uppercase ml-2">Password</label>
                            <input 
                                type="password"
                                required
                                minLength={isLogin ? undefined : 12}
                                maxLength={256}
                                value={formData.password}
                                onChange={(e) => setFormData({...formData, password: e.target.value})}
                                className="w-full bg-slate-900/50 border border-white/5 rounded-2xl px-5 py-4 text-sm focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/50 transition-all"
                                placeholder="••••••••"
                            />
                        </div>
                        {!isLogin && (
                            <div className="space-y-2">
                                <div className="flex justify-between items-center ml-2">
                                    <label className="text-[10px] font-black tracking-[0.2em] text-slate-500 uppercase">Gemini API Key (Optional)</label>
                                    <button 
                                        type="button"
                                        onClick={() => setShowKeyInfo(!showKeyInfo)}
                                        className="text-[10px] font-bold text-cyan-500 hover:text-cyan-400 uppercase tracking-wider"
                                    >
                                        {showKeyInfo ? 'Hide Info' : 'Get Key'}
                                    </button>
                                </div>
                                
                                {showKeyInfo && (
                                    <div className="bg-slate-900/80 border border-cyan-500/30 rounded-2xl p-4 mb-2 animate-in slide-in-from-top-2 duration-200">
                                        <p className="text-[11px] text-slate-400 leading-relaxed mb-2">
                                            To use your own AI capacity, get a free API key from Google AI Studio. 
                                            Sign in with your Google account and click "Create API key" to generate your credentials.
                                        </p>
                                        <a 
                                            href="https://aistudio.google.com/api-keys" 
                                            target="_blank" 
                                            rel="noopener noreferrer"
                                            className="text-[11px] font-bold text-cyan-400 hover:underline flex items-center gap-1"
                                        >
                                            Get Free Key at Google AI Studio <Globe className="w-3 h-3" />
                                        </a>
                                    </div>
                                )}

                                <input 
                                    type="password"
                                    value={formData.geminiKey}
                                    onChange={(e) => setFormData({...formData, geminiKey: e.target.value})}
                                    className="w-full bg-slate-900/50 border border-white/5 rounded-2xl px-5 py-4 text-sm focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/50 transition-all"
                                    placeholder="Enter your API key"
                                />
                            </div>
                        )}

                        {error && <p className="text-red-400 text-xs ml-2">{error}</p>}

                        <button 
                            type="submit"
                            disabled={isLoading}
                            className="w-full bg-white text-slate-900 font-black py-5 rounded-2xl uppercase tracking-widest hover:bg-cyan-400 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 disabled:hover:scale-100"
                        >
                            {isLoading ? 'Processing...' : (isLogin ? 'Sign in to use your own key' : 'Create Account')}
                        </button>
                        {isLogin && <button type="button" onClick={() => setShowRecovery(true)} className="w-full text-cyan-400 text-sm underline">Forgot password?</button>}
                    </form>}

                    <div className="mt-4 text-center">
                        <a
                            href="https://buy.stripe.com/bJe3cw72j5LM5DY5DS7Vm06"
                            target="_blank"
                            rel="noopener noreferrer"
                            data-test="open-source-support-link"
                            data-buy-button-id="buy_btn_1UEyKaLFWluMTxK7KJNimjix"
                            className="text-slate-500 text-[10px] font-bold uppercase tracking-widest hover:text-cyan-400 transition-colors"
                        >
                            Support Open-Source Development (optional)
                        </a>
                    </div>

                    {/* Subscribe CTA (LIVE Stripe Payment Link) */}
                    <div className="mt-8 flex flex-col items-center gap-3 p-6 rounded-[2rem]" style={{ border: '1px solid rgba(16,185,129,0.35)', background: 'linear-gradient(135deg, rgba(16,185,129,0.10), rgba(249,115,22,0.08))' }}>
                        <a
                            href="https://buy.stripe.com/5kQ5kEdqHb66giCaYc7Vm05"
                            target="_blank"
                            rel="noopener noreferrer"
                            data-test="stripe-payment-link-public"
                            data-buy-button-id="buy_btn_1UEyJALFWluMTxK7b31gagty"
                            className="w-full text-center py-4 rounded-xl text-sm font-black uppercase tracking-widest hover:opacity-90 transition-all"
                            style={{ background: 'linear-gradient(90deg,#10b981,#f97316)', color: '#052e1c', boxShadow: '0 12px 30px -12px rgba(16,185,129,0.6)' }}
                        >
                            Sign up for a paid subscription — $49/mo
                        </a>
                        <span className="text-slate-500 font-mono text-[10px] tracking-widest uppercase">Secure live monthly checkout</span>
                    </div>

                    <div className="mt-8 text-center">
                        <button 
                            onClick={() => setIsWaitlistModalOpen(true)}
                            className="text-slate-500 text-xs font-bold hover:text-slate-300 transition-colors uppercase tracking-widest"
                        >
                            Join waitlist for pro version
                        </button>
                    </div>
                </div>

                {isWaitlistModalOpen && (
                    <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-md flex items-center justify-center z-50 p-4 overflow-y-auto">
                        <div className="w-full max-w-md bg-slate-900 border border-white/10 rounded-[2rem] p-8 shadow-2xl animate-in fade-in zoom-in duration-300 my-auto">
                            <h2 className="text-2xl font-bold mb-6 text-white tracking-tight">Join Pro Waitlist</h2>
                            <form onSubmit={handleWaitlistSubmit} className="space-y-4">
                                <div className="space-y-1">
                                    <label className="text-[10px] font-black tracking-[0.2em] text-slate-500 uppercase ml-2">Full Name</label>
                                    <input 
                                        type="text"
                                        required
                                        value={waitlistData.name}
                                        onChange={(e) => setWaitlistData({...waitlistData, name: e.target.value})}
                                        className="w-full bg-slate-800/50 border border-white/5 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-cyan-500/50 transition-all"
                                        placeholder="John Doe"
                                    />
                                </div>
                                <div className="space-y-1">
                                    <label className="text-[10px] font-black tracking-[0.2em] text-slate-500 uppercase ml-2">Profession</label>
                                    <input 
                                        type="text"
                                        required
                                        value={waitlistData.profession}
                                        onChange={(e) => setWaitlistData({...waitlistData, profession: e.target.value})}
                                        className="w-full bg-slate-800/50 border border-white/5 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-cyan-500/50 transition-all"
                                        placeholder="Mechanical Engineer"
                                    />
                                </div>
                                <div className="space-y-1">
                                    <label className="text-[10px] font-black tracking-[0.2em] text-slate-500 uppercase ml-2">Email Address</label>
                                    <input 
                                        type="email"
                                        required
                                        value={waitlistData.email}
                                        onChange={(e) => setWaitlistData({...waitlistData, email: e.target.value})}
                                        className="w-full bg-slate-800/50 border border-white/5 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-cyan-500/50 transition-all"
                                        placeholder="john@example.com"
                                    />
                                </div>
                                <div className="space-y-1">
                                    <label className="text-[10px] font-black tracking-[0.2em] text-slate-500 uppercase ml-2">Proposed Use</label>
                                    <textarea 
                                        required
                                        value={waitlistData.proposedUse}
                                        onChange={(e) => setWaitlistData({...waitlistData, proposedUse: e.target.value})}
                                        className="w-full bg-slate-800/50 border border-white/5 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-cyan-500/50 transition-all min-h-[100px]"
                                        placeholder="How do you plan to use Vibe Engineer?"
                                    />
                                </div>
                                <div className="flex gap-3 pt-4">
                                    <button 
                                        type="button"
                                        onClick={() => setIsWaitlistModalOpen(false)}
                                        className="flex-1 bg-slate-800 text-slate-400 font-bold py-4 rounded-xl uppercase tracking-widest hover:bg-slate-700 transition-all"
                                    >
                                        Cancel
                                    </button>
                                    <button 
                                        type="submit"
                                        className="flex-2 bg-cyan-500 text-slate-900 font-black py-4 px-8 rounded-xl uppercase tracking-widest hover:bg-cyan-400 transition-all"
                                    >
                                        Submit
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}

                <div className="absolute bottom-8 right-8 font-mono text-[10px] text-slate-600 tracking-widest">
                    MIFECO © 2026 V4.03
                </div>
            </div>
        </div>
    );
};
